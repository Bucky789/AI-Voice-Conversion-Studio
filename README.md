# 🎙️ AI Voice Conversion Studio

An end-to-end **AI-powered Voice Conversion** web app built using **Flask (backend)** and **React (frontend)**.  
This project uses **Retrieval-based Voice Conversion (RVC)** models to transform voices in real time or from recordings — ideal for creative projects, music production, or experimentation with voice synthesis.

---

## 🚀 Features

- 🎤 Convert your voice into a trained target voice using **RVC models**
- ⚡ Real-time inference with **Flask API backend**
- 🧠 Uses **pre-trained models** for fast and accurate voice conversion
- 🎚️ Adjustable parameters for cleaner and more natural results
- 🖥️ Modern and responsive **React frontend**
- 🎧 Preview and download converted audio
- 🌐 CORS-enabled backend for smooth communication with frontend

---

## 🏗️ Tech Stack

### **Frontend**
- React + Vite  
- Tailwind CSS (UI Styling)
- Axios (API Calls)

### **Backend**
- Flask (Python)
- Torch / PyTorch
- NumPy, SciPy, and Librosa (audio processing)
- Flask-CORS (for cross-origin requests)
- RVC Model Files (`.pth`, `.index`)

---

## 📁 Project Structure

```
rvc-fullstack-app/
│
├── backend/
│   ├── app.py                # Main Flask server
│   ├── rvc_converter.py      # Voice conversion logic
│   ├── requirements.txt      # Backend dependencies
│   ├── models/               # RVC model files (.pth)
│   ├── voices/               # Indexed voice embeddings
│   ├── pretrained_models/    # Base models
│   └── static/outputs/       # Converted audio output
│
├── frontend/
│   ├── src/
│   │   ├── components/       # UI components
│   │   ├── pages/            # App pages
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## ⚙️ Setup Instructions

### 🧩 1. Clone the Repository
```bash
git clone https://github.com/Bucky789/AI-Voice-Conversion-Studio.git
cd AI-Voice-Conversion-Studio
```

---

### 🖥️ 2. Backend Setup

1. Navigate to backend folder:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   # or
   source venv/bin/activate  # On Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run Flask server:
   ```bash
   python app.py
   ```
   Flask should start on **http://127.0.0.1:5000**

---

### 💻 3. Frontend Setup

1. Navigate to frontend folder:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React app:
   ```bash
   npm run dev
   ```

4. Open the local URL (e.g., `http://localhost:5173`) to use the app.

---

## 🎧 Using the App

1. Select or upload your **input audio**  
2. Choose a **target voice/model**
3. Adjust conversion parameters (pitch, filter, etc.)
4. Click **Convert**  
5. Download or play your **converted audio** directly in the browser!

---

## 🧠 Model Files

The main voice model files (e.g., `.pth`, `.index`, `.data`) are **too large for GitHub**.  
To run this app properly:

- Download or place your RVC models in:
  ```
  backend/models/
  backend/voices/
  backend/pretrained_models/
  ```
- Make sure model paths match what’s used in your `app.py`.

For GitHub storage limits (>100MB), use **Git LFS (Large File Storage)** if you want to host models online:
👉 https://git-lfs.github.com/

---

## 🛠️ Troubleshooting

### 🧩 CORS Error
If the frontend cannot fetch voices or conversions:
```python
# app.py
from flask_cors import CORS
CORS(app)
```

### ⚠️ Large File Push Error
If you see errors like:
```
error: GH001: Large files detected
```
Use Git LFS for `.pth` or `.index` files:
```bash
git lfs install
git lfs track "*.pth"
git lfs track "*.index"
git add .gitattributes
git add .
git commit -m "Add large model files with LFS"
git push origin main
```

---

## 🧑‍💻 Author

**Manthan Sumbhe**  
🎓 Master’s in Computer Science — Boston, USA  
💼 Full Stack Developer | AI/ML Enthusiast  
🌐 www.linkedin.com/in/manthan-sumbhe

---

## 🪪 License

This project is open-source under the **MIT License**.  
Feel free to fork and modify for your own use!
