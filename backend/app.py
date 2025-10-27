import os
import subprocess
import torch
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from torch.serialization import add_safe_globals
from fairseq.data.dictionary import Dictionary
import librosa
import soundfile as sf
import numpy as np
from rvc_python.infer import RVCInference
from flask_cors import CORS

# ------------------------------------------
# ⚙️ SETUP
# ------------------------------------------
app = Flask(__name__)
CORS(app)  # ✅ enable CORS for all routes


UPLOAD_FOLDER = 'uploads'
SEPARATED_FOLDER = 'separated'
CONVERTED_FOLDER = 'converted'
MODEL_FOLDER = 'models'  # folder containing .pth RVC models

for folder in [UPLOAD_FOLDER, SEPARATED_FOLDER, CONVERTED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

add_safe_globals([Dictionary])

# Initialize RVCInference globally
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
rvc = RVCInference(device=device)
print(f"✅ RVC backend initialized on device: {device}")

# ------------------------------------------
# 🧠 API: List available voice models
# ------------------------------------------
@app.route('/api/voices', methods=['GET'])
def list_voices():
    models = []
    for f in os.listdir(MODEL_FOLDER):
        if f.endswith('.pth'):
            models.append(os.path.splitext(f)[0])
    return jsonify(sorted(models))

# ------------------------------------------
# 🎧 API: Upload + Separate Vocals
# ------------------------------------------
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    try:
        # Run spleeter from its environment
        subprocess.run([
            r"C:/ProgramData/miniconda3/Scripts/conda.exe", "run", "-n", "spleeter",
            "spleeter", "separate",
            input_path,
            "-p", "spleeter:2stems",
            "-o", SEPARATED_FOLDER
        ], check=True)

        track_name = os.path.splitext(filename)[0]
        vocal_path = os.path.join(SEPARATED_FOLDER, track_name, 'vocals.wav')
        instrumental_path = os.path.join(SEPARATED_FOLDER, track_name, 'accompaniment.wav')

        if not os.path.exists(vocal_path) or not os.path.exists(instrumental_path):
            return jsonify({'error': 'Separation failed — missing files'}), 500

        return jsonify({
            'message': 'Separation complete',
            'vocal_path': vocal_path.replace("\\", "/"),
            'instrumental_path': instrumental_path.replace("\\", "/")
        })
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Spleeter failed: {e}'}), 500

# ------------------------------------------
# 🎙️ API: Convert + Merge with Instrumental
# ------------------------------------------
@app.route('/api/convert', methods=['POST'])
def convert_voice():
    voice_model = request.form.get('voice_model')
    vocal_path = request.form.get('vocal_path')
    instrumental_path = request.form.get('instrumental_path')

    if not voice_model or not vocal_path or not instrumental_path:
        return jsonify({'error': 'Missing parameters: voice_model, vocal_path, instrumental_path'}), 400

    model_path = os.path.join(MODEL_FOLDER, f"{voice_model}.pth")
    if not os.path.exists(model_path):
        return jsonify({'error': f'Model {voice_model}.pth not found'}), 404
    if not os.path.exists(vocal_path):
        return jsonify({'error': f'Vocal file not found at {vocal_path}'}), 404
    if not os.path.exists(instrumental_path):
        return jsonify({'error': f'Instrumental file not found at {instrumental_path}'}), 404

    try:
        # Step 1: Resample input vocals to 48kHz mono
        y, sr = librosa.load(vocal_path, sr=48000, mono=True)
        resampled_vocal_path = os.path.join(SEPARATED_FOLDER, "temp_resampled.wav")
        sf.write(resampled_vocal_path, y, 48000)

        # Step 2: Load chosen RVC model
        rvc.load_model(model_path)

        # Step 3: Perform voice conversion
        wav_opt = rvc.vc.vc_single(
            sid=0,
            input_audio_path=resampled_vocal_path,
            f0_up_key=0,
            f0_method="rmvpe",     # best quality pitch extraction
            file_index=None,
            file_index2=None,
            f0_file=None,
            index_rate=0.9,
            filter_radius=5,
            resample_sr=0,
            rms_mix_rate=0.4,
            protect=0.5
        )

        audio_out = wav_opt[0] if isinstance(wav_opt, tuple) else wav_opt
        audio_out = audio_out / max(abs(audio_out).max(), 1e-8)  # normalize

        # Step 4: Save converted vocals
        converted_vocal_path = os.path.join(CONVERTED_FOLDER, f"converted_{os.path.basename(vocal_path)}")
        sf.write(converted_vocal_path, audio_out, rvc.vc.tgt_sr)

        # Step 5: Remix with instrumental
        instrumental, sr_inst = librosa.load(instrumental_path, sr=rvc.vc.tgt_sr, mono=True)
        min_len = min(len(instrumental), len(audio_out))
        instrumental = instrumental[:min_len]
        vocals = audio_out[:min_len]

        # Blend: final remix
        remix = vocals + 0.8 * instrumental
        remix = remix / max(abs(remix).max(), 1e-8)

        # Step 6: Save final remix
        remix_path = os.path.join(CONVERTED_FOLDER, f"remix_{os.path.basename(vocal_path)}")
        sf.write(remix_path, remix, rvc.vc.tgt_sr)

        return send_file(remix_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------------------------------
# 🏠 Root
# ------------------------------------------
@app.route('/')
def home():
    return "🎶 Flask RVC Backend Running Successfully"

@app.route('/api/up', methods=['GET'])
def up():
    return "UP"

# ------------------------------------------
# 🚀 Run Server
# ------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
