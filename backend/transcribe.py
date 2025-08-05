def process_video_with_subs(video_path: str) -> dict:
    import os
    import moviepy.editor as mp
    import whisper
    import subprocess

    base_filename = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = f"{base_filename}.wav"
    srt_path = f"{base_filename}.srt"
    transcript_path = f"{base_filename}_transcript.txt"
    output_path = f"{base_filename}_with_subs.mp4"

    # Step 1: Extract audio
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    # Step 2: Transcribe using Whisper
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path, verbose=True)

    # Step 3: Write .srt subtitles and raw transcript
    def write_srt(transcription, filename=srt_path):
        with open(filename, "w", encoding="utf-8") as f:
            for i, segment in enumerate(transcription["segments"]):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()

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

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Step 4: Burn subtitles into video
    subprocess.run([
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}",
        "-c:a", "copy",
        output_path
    ])

    os.remove(audio_path)

    return {
        "transcript_text": result["text"],
        "transcript_path": transcript_path,
        "subtitle_file": srt_path,
        "output_video": output_path
    }
