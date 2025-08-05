from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
from transcribe import transcriber

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/transcribe/")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded video
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process it
    try:
        result = transcriber(file_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return {
        "transcript": result["transcript"],
        "download_url": f"/download/video?path={result['output_video']}",
    }

@app.get("/download/video")
def download_video(path: str):
    if os.path.exists(path):
        return FileResponse(path, media_type="video/mp4", filename=os.path.basename(path))
    return JSONResponse(status_code=404, content={"error": "File not found"})
