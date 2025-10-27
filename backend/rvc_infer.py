import os
import subprocess
from pydub import AudioSegment

def convert_vocals_with_rvc(input_vocal_path, model_path, output_dir):
    """
    Converts vocals using the RVC model (.pth file) via infer-web.py script.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_vocal_path = os.path.join(output_dir, "converted_vocals.wav")

    # Call infer-web.py script
    cmd = [
        "python",
        os.path.join(os.getcwd(), "rvc_repo", "infer-web.py"),
        "--input", input_vocal_path,
        "--model", model_path,
        "--output", output_vocal_path
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"RVC conversion failed: {e}")

    return output_vocal_path


def combine_vocals_and_background(vocal_path, background_path, output_dir):
    """
    Combine converted vocals and background into a single audio file.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "final_output.wav")

    vocal = AudioSegment.from_file(vocal_path)
    background = AudioSegment.from_file(background_path)

    # Ensure both audio files are the same length
    if len(vocal) < len(background):
        vocal = vocal + AudioSegment.silent(duration=len(background) - len(vocal))
    else:
        background = background + AudioSegment.silent(duration=len(vocal) - len(background))

    combined = vocal.overlay(background)
    combined.export(output_path, format="wav")

    return output_path
