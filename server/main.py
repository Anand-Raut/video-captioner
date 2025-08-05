# app.py
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
import shutil

from transcribe import transcriber

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/transcribe/")
async def upload_video(file: UploadFile = File(...)):
    unique_id = str(uuid.uuid4())
    filename = f"{unique_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        result = transcriber(file_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return {
        "transcript": result["transcript"],
        "download_url": f"/download/video/{os.path.basename(result['output_video'])}",
    }

@app.get("/download/video/{filename}")
def download_video(filename: str):
    path = os.path.join("outputs", filename)
    if os.path.exists(path):
        return FileResponse(path, media_type="video/mp4", filename=filename)
    return JSONResponse(status_code=404, content={"error": "File not found"})
