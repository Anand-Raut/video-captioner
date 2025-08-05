# 🎬 Video Captioner App

An end-to-end application that **automatically transcribes video speech to subtitles** using [OpenAI's Whisper model](https://github.com/openai/whisper), and **burns them into the video**. Built using FastAPI (backend) and React + Tailwind CSS (frontend).

---

## 🗂️ Project Structure

```
📁 client/           # React + Tailwind frontend
📁 server/           # FastAPI backend
 ┣ 📁 uploads/       # Uploaded video files
 ┣ 📁 outputs/       # Transcribed text, .srt, and output video files
 ┣ 📄 main.py        # FastAPI server entry
 ┣ 📄 transcribe.py  # Whisper + MoviePy + FFmpeg logic
📁 venv/             # Virtual environment (excluded from Git)
📄 requirements.txt  # Backend dependencies
📄 .gitignore
```

---

## 🚀 Features

- Upload any video file (MP4, MOV, etc.)
- Extract audio using MoviePy
- Transcribe speech using OpenAI Whisper
- Generate `.srt` subtitle files
- Burn subtitles into the video using FFmpeg
- Download the final video with hardcoded subtitles
- Web frontend for ease of use

---

## ⚙️ Backend Setup

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/your-username/video-captioner.git
cd video-captioner
python -m venv venv
venv\Scripts\activate  # Or `source venv/bin/activate` on Mac
```

### 2. Install dependencies

```bash
pip install -r server/requirements.txt
```

> Make sure FFmpeg is installed and added to PATH.

### 3. Run the server

```bash
cd server
uvicorn main:app --reload
```

---

## 💻 Frontend Setup

```bash
cd client
npm install
npm run dev
```

---

## 🧪 API Endpoint

**POST /transcribe/**  
Uploads a video and returns transcript + download link.

```bash
curl -X POST http://localhost:8000/transcribe/ \
  -F "file=@video.mp4"
```

Response:
```json
{
  "transcript": "Hello world...",
  "download_url": "/download/video?path=outputs/video_with_subs.mp4"
}
```

## 🪪 License

MIT © [Anand Raut](https://github.com/Anand-Raut)