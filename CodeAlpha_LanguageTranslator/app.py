import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# --------------------------------------------------
# Load API key from .env
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Check if API key exists
if not api_key:
    st.error("❌ GEMINI_API_KEY is missing. Please add it to your .env file.")
    st.stop()


# --------------------------------------------------
# Connect to Gemini
# --------------------------------------------------

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# Available languages
# --------------------------------------------------

LANGUAGES = [
    "English",
    "Urdu",
    "Spanish",
    "French",
    "German",
    "Arabic",
    "Chinese",
    "Hindi"
]


# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------

st.title("🌍 AI Language Translator")

st.write(
    "Type something below, choose your languages, "
    "and click Translate!"
)


# --------------------------------------------------
# Text input
# --------------------------------------------------

text_input = st.text_area(
    "Enter text to translate:",
    height=150
)


# --------------------------------------------------
# Language selection
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "From:",
        LANGUAGES
    )

with col2:
    target_lang = st.selectbox(
        "To:",
        LANGUAGES,
        index=1
    )


# --------------------------------------------------
# Buttons
# --------------------------------------------------

btn1, btn2 = st.columns(2)

with btn1:
    translate_clicked = st.button(
        "🌐 Translate",
        use_container_width=True
    )

with btn2:
    clear_clicked = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


# --------------------------------------------------
# Clear button
# --------------------------------------------------

if clear_clicked:
    st.rerun()


# --------------------------------------------------
# Translation
# --------------------------------------------------

if translate_clicked:

    # Make sure the user entered something
    if not text_input.strip():

        st.warning("⚠️ Please type something first!")

    # Same language
    elif source_lang == target_lang:

        st.info(
            "The source and target languages are the same."
        )

        st.code(
            text_input,
            language=None
        )

    else:

        try:

            # Create translation prompt
            prompt = f"""
Translate the following text from {source_lang} to {target_lang}.

Rules:
- Return only the translation.
- Do not explain the translation.
- Do not add quotation marks.
- Preserve the original meaning.
- Preserve the original formatting when possible.

Text to translate:

{text_input}
"""

            # --------------------------------------------------
            # Gemini API request
            # --------------------------------------------------
            #
            # IMPORTANT:
            # We changed the old model:
            #
            # gemini-2.5-flash
            #
            # to:
            #
            # gemini-3.6-flash
            #
            # --------------------------------------------------

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            # Get Gemini's response
            translated_text = response.text

            # Make sure response isn't empty
            if translated_text:

                st.success("✅ Translation complete!")

                st.code(
                    translated_text.strip(),
                    language=None
                )

            else:

                st.error(
                    "❌ Gemini returned an empty response."
                )

        except Exception as e:

            st.error(
                f"❌ Something went wrong:\n\n{e}"
            )
