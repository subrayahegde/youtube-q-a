
# import dependencies
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi


# configure API by loading key from .env file
# load environment variables
load_dotenv()
# configure key
genai.configure(api_key=st.secrets["gemini_api_key"])


# initialize gemini pro model
def initialize_model(model_name="gemini-1.5-flash"):
    model = genai.GenerativeModel(model_name)
    return model

def get_response(model, prompt):
    response = model.generate_content(prompt)
    return response.text

def get_video_transcripts(video_id):
    try:
        transcription_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcription = " ".join([transcript["text"] for transcript in transcription_list])
        return transcription

    except Exception as e:
        raise e


def get_video_id(url):
    video_id = url.split("=")[1]
    if "&" in video_id:
        video_id = video_id.split("&")[0]

    return video_id


st.title("Question Answering in YouTube video")
st.markdown("<br>", unsafe_allow_html=True)
youtube_url = st.text_input("Enter youtube video link:")
if youtube_url:
    video_id = get_video_id(youtube_url)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    
user_prompt = st.text_area("Your Prompt on above video", key="user_prompt")
submit = st.button("submit")


model_behavior = """ You are expert in summarization of youtube videos from transcription of videos.
            So, input is transcriptions of videos along with prompt which have the user query. Please make sure that you have
             understand all the information present in the video from transcription and respond user query. 
             Please don't add extra information that doesn't make sense but fix typos and return `Couldn't transcribe the video` 
             if transcription of video is empty otherwise respond accordingly!.
    """
if user_prompt or submit:
    # transcribe the video
    video_transcriptions = get_video_transcripts(video_id)
    # initialize the gemini-pro model
    gemini_model = initialize_model(model_name="gemini-1.5-flash")
    # add transcription and prompt to main prompt
    model_behavior = model_behavior + f"\nvideo transcription: {video_transcriptions} \nprompt: {user_prompt}"

    response = get_response(model=gemini_model, prompt=model_behavior)
    st.write(response)
