# app.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os

from transcribe import process_video_with_subs

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/transcribe/")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Run transcription + subtitle pipeline
    result = process_video_with_subs(file_path)

    return JSONResponse(content={
        "transcript": result["transcript_text"],
        "transcript_file": result["transcript_path"],
        "subtitle_file": result["subtitle_file"],
        "output_video": result["output_video"]
    })
