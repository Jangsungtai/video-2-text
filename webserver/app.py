import streamlit as st
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
    print("Processing: " + youtube_url)
    yt = YouTube(youtube_url)
    directory = tempfile.gettempdir()
    file_path = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(directory)
    video_length = yt.length  # 비디오 길이(초 단위)
    print(f"VIDEO NAME: {yt.title}")
    print(f"Download complete: {file_path}")
    return {"name": yt.title, "thumbnail": yt.thumbnail_url, "path": file_path, "duration": video_length}



def on_progress(stream, chunk, bytes_remaining):
    #다운로드 진행현황 표시 콜백 함수"
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")




def main():
    st.title("Teaching2Text")

    # User input: YouTube URL
    url = st.text_input("Enter YouTube URL:")


    # User input: model
    models = ["tiny", "base", "small", "medium", "large"]
    model = st.selectbox("Select Model:", models)
    st.write(
        "If you take a smaller model it is faster but not as accurate, whereas a larger model is slower but more accurate.")
    
    # User input: model suffix(mode)
    models_mode = ["Normal mode", "English mode"]
    model_mode = st.selectbox("Select model_mode:", models_mode)
    st.write(
        "Normal mode is good for any language, English mode is optimized specifically for English .")

    # Result from User input : model + suffix
    if model_mode == "English mode" and model_mode in ["tiny", "base", "small", "medium"]:
        model = f"{model_mode}_en"


    
    if st.button("Transcribe"):
        
        #placeholder 선언
        video_info_placeholder = st.empty()
        transcription_placeholder = st.empty()

        if url:
            # 비디오 정보를 먼저 Placeholder에 표시
            video_info = downloadYoutubeVideo(url)
            video_info_placeholder.subheader("Video Information:")
            video_info_placeholder.write("Loading Videos")

            # Transcription 시작 *메인부분*
            transcript = transcribeVideoOrchestrator(url, model)

            if transcript:
                word_count = len(transcript.split())
                # 비디오 정보 Placeholder 업데이트
                video_info_placeholder.write(f"Video Name: {video_info['name']}") # 비디오 이름 예시
                # Update video information placeholder
                video_info_placeholder.write(f"Video Name: {video_info['name']}\nTotal Words: {word_count}\nVideo Length: {video_info['duration']} seconds")

                # Calculate word count from transcript



                # 전체 텍스트를 다른 Placeholder에 표시
                transcription_placeholder.subheader("Full Text Transcription:")
                transcription_placeholder.write(transcript)
            else:
                st.error("Error occurred while transcribing.")
                st.write("Please try again.")


if __name__ == "__main__":
    main()
