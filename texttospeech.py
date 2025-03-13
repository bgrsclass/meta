import streamlit as st
import pyttsx3
import PyPDF2
import tempfile
import os
from gtts import gTTS
from googletrans import Translator

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = "".join(page.extract_text() or "" for page in reader.pages).strip()
        return text if text else "No text found in the PDF."
    except Exception as e:
        return f"Error reading PDF: {e}"

# Function to translate text
def translate_text(text, target_language):
    try:
        translator = Translator()
        lang_codes = {"English": "en", "Hindi": "hi", "French": "fr"}
        translated_text = translator.translate(text, dest=lang_codes[target_language]).text
        return translated_text
    except Exception as e:
        return f"Error translating text: {e}"

# Function to convert text to speech with language and speed options
def text_to_speech(text, language, speed):
    if language == "Hindi":
        # Use gTTS for Hindi
        tts = gTTS(text=text, lang="hi")
        temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
        tts.save(temp_audio_path)
    else:
        # Use pyttsx3 for English and French
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")

        if language == "English":
            engine.setProperty("voice", voices[0].id)  # Adjust index as needed
        elif language == "French":
            engine.setProperty("voice", voices[1].id)  # Adjust index as needed

        engine.setProperty("rate", speed)
        temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
        engine.save_to_file(text, temp_audio_path)
        engine.runAndWait()

    return temp_audio_path

# Streamlit UI
st.title("📄 PDF to Speech Converter 🎙️")
st.markdown("Convert your PDF text into speech with **translation and adjustable speed**.")

uploaded_file = st.file_uploader("📂 Upload a PDF file", type=["pdf"])

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.text_area("📝 Extracted Text", pdf_text, height=200)

    language = st.selectbox("🌍 Select Language", ["English", "Hindi", "French"])
    speed = st.slider("🎚️ Adjust Speech Speed", min_value=100, max_value=250, value=150)

    if st.button("🔊 Convert to Speech"):
        if pdf_text and "Error" not in pdf_text:
            # Step 1: Translate text first
            translated_text = translate_text(pdf_text, language)
            st.text_area("📖 Translated Text", translated_text, height=200)

            # Step 2: Convert translated text to speech
            audio_file = text_to_speech(translated_text, language, speed)
            st.audio(audio_file)
            st.success("✅ Audio generated successfully! 🎵")
        else:
            st.warning("⚠️ No valid text found in the PDF!")

st.markdown("---")
st.markdown("📌 **Features:**")
st.markdown("✔️ Extracts text from PDFs")
st.markdown("✔️ Translates text before speech conversion")
st.markdown("✔️ Supports multiple languages (English, Hindi, French)")
st.markdown("✔️ Allows adjustable speech speed")
st.markdown("✔️ Provides a downloadable audio file")
