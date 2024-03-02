import tempfile
from pprint import pprint

import whisper
from pytube import YouTube

def transcribeVideoOrchestrator(youtube_url: str,  model_name: str):
    #url과 모델 변수를 받아서 동영상,텍스트 변환 함수 호출 
    video = downloadYoutubeVideo(youtube_url)
    transcription = transcribe(video, model_name)
    return transcription


def transcribe(video: dict, model_name="medium"):
    #STT 메인함수 : 지정된 모델으로 동영상의 오디오를 텍스트로 변환 
    print("Transcribing...", video['name'])
    print("Using model:", model_name)
    model = whisper.load_model(model_name)
    result = model.transcribe(video['path'], ) #***STT 모델 호출
    pprint(result)
    return result["text"]


def downloadYoutubeVideo(youtube_url: str) -> dict:
    #유튜브 동영상을 다운로드 하고 정보를 dic으로 반환
    print("Processing : " + youtube_url)
    yt = YouTube(youtube_url)
    directory = tempfile.gettempdir()
    file_path = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first().download(directory)
    print("VIDEO NAME " + yt._title)
    print("Download complete:" + file_path)
    return {"name": yt._title, "thumbnail": yt.thumbnail_url, "path": file_path}


def on_progress(stream, chunk, bytes_remaining):
    #다운로드 진행현황 표시 콜백 함수"
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")
