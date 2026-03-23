import os
import whisper
import srt
import subprocess
from datetime import timedelta
from moviepy.editor import VideoFileClip

# -------------------------------
# CONFIG
# -------------------------------
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  # CHANGE THIS

# -------------------------------
# LOAD MODEL (OPTIMIZED)
# -------------------------------
_model = None

def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model

# -------------------------------
# FUNCTIONS
# -------------------------------

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    if audio:
        audio.write_audiofile(audio_path)
    else:
        raise Exception("No audio found!")

def transcribe_audio(audio_path):
    model = get_model()
    result = model.transcribe(audio_path)
    return result

def convert_to_srt(result):
    segments = result['segments']
    subtitles = []

    for i, seg in enumerate(segments):
        subtitle = srt.Subtitle(
            index=i + 1,
            start=timedelta(seconds=seg['start']),
            end=timedelta(seconds=seg['end']),
            content=seg['text'].strip()
        )
        subtitles.append(subtitle)

    return srt.compose(subtitles)

def save_srt(content, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def burn_subtitles(video_path, srt_path, output_path):
    command = f'"{FFMPEG_PATH}" -i "{video_path}" -vf "subtitles={srt_path}" -c:a copy "{output_path}"'
    subprocess.run(command, shell=True, check=True)

# -------------------------------
# FULL PIPELINE FUNCTION
# -------------------------------

def process_video(video_path, work_dir="temp"):
    os.makedirs(work_dir, exist_ok=True)

    audio_path = os.path.join(work_dir, "audio.mp3")
    srt_path = os.path.join(work_dir, "subtitles.srt")
    output_video = os.path.join(work_dir, "output.mp4")

    # Step 1
    extract_audio(video_path, audio_path)

    # Step 2
    result = transcribe_audio(audio_path)

    # Step 3
    srt_content = convert_to_srt(result)
    save_srt(srt_content, srt_path)

    # Step 4
    burn_subtitles(video_path, srt_path, output_video)

    return output_video