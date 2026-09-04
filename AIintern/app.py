import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Load our secret key from the .env file into memory
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Set up our connection to Gemini, using that key
client = genai.Client(api_key=api_key)

# A simple list of languages the user can choose from
LANGUAGES = ["English", "Urdu", "Spanish", "French", "German", "Arabic", "Chinese", "Hindi"]

st.title("🌍 AI Language Translator")
st.write("Type something below, choose your languages, and hit Translate!")

# A box where the user types their sentence
text_input = st.text_area("Enter text to translate:")

# Two dropdown menus, side by side
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From:", LANGUAGES)
with col2:
    target_lang = st.selectbox("To:", LANGUAGES, index=1)

# Two buttons, side by side
btn1, btn2 = st.columns(2)
translate_clicked = btn1.button("Translate")
clear_clicked = btn2.button("Clear")

if clear_clicked:
    st.rerun()  # refreshes the page, which empties the text box

if translate_clicked:
    if text_input.strip() == "":
        st.warning("Please type something first!")
    else:
        try:
            # This is the "instruction" we send to Gemini
            prompt = (
                f"Translate the following text from {source_lang} to {target_lang}. "
                f"Only return the translated text, nothing else:\n\n{text_input}"
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            translated_text = response.text
            st.success("Here's your translation:")
            st.code(translated_text, language=None)  # shows a built-in copy icon
        except Exception as e:
            st.error(f"Something went wrong: {e}")