import os
import moviepy as mp
import whisper
import subprocess

def transcriber(video_path: str) -> dict:
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = f"outputs/{base_name}.wav"
    srt_path = f"outputs/{base_name}.srt"
    transcript_path = f"outputs/{base_name}_transcript.txt"
    output_video = f"outputs/{base_name}_with_subs.mp4"

    os.makedirs("outputs", exist_ok=True)

    # Step 1: Extract audio
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    # Step 2: Transcribe
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path, verbose=True)

    # Step 3: Write .srt
    def write_srt(transcription, filename="video.srt", max_gap=2.0, max_display_time=5.0):
        segments = transcription["segments"]
        with open(filename, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments):
                start = segment["start"]
                end = segment["end"]

                # Cap subtitle display if there's a big gap to the next one
                if i + 1 < len(segments):
                    next_start = segments[i + 1]["start"]
                    gap = next_start - end
                    if gap > max_gap:
                        # cut this one shorter to avoid lingering
                        end = min(end, start + max_display_time)

                text = segment["text"].strip()

                def format_time(seconds):
                    hrs = int(seconds // 3600)
                    mins = int((seconds % 3600) // 60)
                    secs = int(seconds % 60)
                    millis = int((seconds - int(seconds)) * 1000)
                    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

                f.write(f"{i + 1}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{text}\n\n")



    write_srt(result, srt_path)

    # Save full transcript
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Step 4: Burn subtitles
    subprocess.run([
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}",
        "-c:a", "copy",
        output_video
    ])

    os.remove(audio_path)

    return {
        "transcript": result["text"],
        "output_video": output_video
    }
