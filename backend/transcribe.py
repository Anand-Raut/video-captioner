# import sys
# print("Python executable:", sys.executable)


import os
from moviepy import VideoFileClip
from whisper import load_model
import subprocess
import uuid

def transcriber(video_path: str) -> dict:
    os.makedirs("outputs", exist_ok=True)

    # Use UUID to avoid filename collisions
    base_id = str(uuid.uuid4())
    audio_path = f"outputs/{base_id}.wav"
    srt_path = f"outputs/{base_id}.srt"
    transcript_path = f"outputs/{base_id}.txt"
    output_video_path = f"outputs/{base_id}_with_subs.mp4"

    # Step 1: Extract audio
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    # Step 2: Transcribe with Whisper
    model = load_model("tiny")
    result = model.transcribe(audio_path, verbose=True)

    # Step 3: Write subtitles
    def write_srt(transcription, filename=srt_path):
        with open(filename, "w", encoding="utf-8") as f:
            for i, segment in enumerate(transcription["segments"]):
                start, end, text = segment["start"], segment["end"], segment["text"].strip()

                def format_time(seconds):
                    hrs = int(seconds // 3600)
                    mins = int((seconds % 3600) // 60)
                    secs = int(seconds % 60)
                    millis = int((seconds - int(seconds)) * 1000)
                    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

                f.write(f"{i+1}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n{text}\n\n")

    write_srt(result)

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Step 4: Burn subtitles
    subprocess.run([
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}",
        "-c:a", "copy",
        output_video_path
    ], check=True)

    # Step 5: Cleanup audio
    os.remove(audio_path)

    return {
        "transcript": result["text"],
        "transcript_file": transcript_path,
        "subtitle_file": srt_path,
        "output_video": output_video_path
    }
