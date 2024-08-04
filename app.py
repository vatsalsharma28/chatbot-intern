from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import io
from pydub import AudioSegment
import speech_recognition as sr
import pytesseract

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load gemini pro model and get responses
model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(question) -> str:
    response = model.generate_content(question)
    return response.text

# Function to convert text to image
def text_to_image(text):
    img = Image.new('RGB', (800, 200), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((10,10), text, fill=(0,0,0), font=font)
    return img

# Function to convert text to audio
def text_to_audio(text):
    tts = gTTS(text)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp

# Function to process uploaded image
def process_image(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text

# Function to process uploaded audio
def process_audio(audio):
    recognizer = sr.Recognizer()
    audio_fp = io.BytesIO(audio.read())
    audio_segment = AudioSegment.from_file(audio_fp)
    audio_fp.seek(0)
    with sr.AudioFile(audio_fp) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

# Initialize our Streamlit application
st.set_page_config(page_title="Summer Internship Poorinma")
st.header("Your Personal Bot")

input = st.text_input("Input: ", key="input")
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
uploaded_audio = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
submit = st.button("Submit")

# When user submit is clicked
if submit:
    if input:
        response = get_gemini_response(input)
        st.subheader("The response is")
        st.write(response)
        
        # Display response as image
        img = text_to_image(response)
        st.image(img, caption="Response as Image")

        # Display response as audio
        audio_fp = text_to_audio(response)
        st.audio(audio_fp, format='audio/mp3')
    
    if uploaded_image:
        image_content = process_image(uploaded_image)
        st.subheader("Processed Image Content")
        st.write(image_content)
        image_question = st.text_input("Ask a question about the image:", key="image_question")
        if image_question:
            image_response = get_gemini_response(image_question + " " + image_content)
            st.write(image_response)
    
    if uploaded_audio:
        audio_content = process_audio(uploaded_audio)
        st.subheader("Processed Audio Content")
        st.write(audio_content)
        audio_question = st.text_input("Ask a question about the audio:", key="audio_question")
        if audio_question:
            audio_response = get_gemini_response(audio_question + " " + audio_content)
            st.write(audio_response)
