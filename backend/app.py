import os
import moviepy as mp
import whisper
import subprocess

# Step 1: Extract audio
video = mp.VideoFileClip("video.mp4")
video.audio.write_audiofile("audio.wav")

# Step 2: Transcribe using Whisper
model = whisper.load_model("tiny")
result = model.transcribe("audio.wav", verbose=True)

# Step 3: Write .srt subtitles
def write_srt(transcription, filename="video.srt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcription["segments"]):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            # Format time to SRT time
            def format_time(seconds):
                hrs = int(seconds // 3600)
                mins = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                millis = int((seconds - int(seconds)) * 1000)
                return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

            f.write(f"{i+1}\n")
            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            f.write(f"{text}\n\n")

write_srt(result)

# Step 4: Burn subtitles into the video using FFmpeg
subprocess.run([
    "ffmpeg",
    "-i", "video.mp4",
    "-vf", "subtitles=video.srt",
    "-c:a", "copy",
    "output_with_subs.mp4"
])

# Step 5: Clean up (optional)
os.remove("audio.wav")
print("✅ Done: Subtitles burned into 'output_with_subs.mp4'")
