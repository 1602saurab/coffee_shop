import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini AI key
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.error("❌ GEMINI_API_KEY not found. Please check your .env file.")
    st.stop()

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

# Set up the Streamlit UI
st.set_page_config(page_title="🔮 Coffee Cup Fortune Teller", page_icon="☕")
st.title("🔮 Coffee Cup Fortune Teller")
st.markdown("Upload coffee cup image URLs from different angles and discover your mystical fortune!")

# Input URLs from user
left_url = st.text_input("📷 Left view image URL")
right_url = st.text_input("📷 Right view image URL")
up_url = st.text_input("📷 Up view image URL")
down_url = st.text_input("📷 Down view image URL")
top_url = st.text_input("📷 Top view image URL")

# Generate button
if st.button("🔍 Reveal My Fortune"):
    if all([left_url, right_url, up_url, down_url, top_url]):
        with st.spinner("Reading the mystical grounds... 🔮"):

            prompt = """
You are a mystical coffee cup fortune teller. Analyze the uploaded images of coffee cup grounds from 5 different angles and provide an imaginative yet structured fortune.

Please return your response **strictly in the following JSON format**:

{{
    "readings": [
        {{
            "Observation": "symbol name (e.g., Tree, Fish, Mountain)",
            "Location": "specific position in the image (e.g., bottom-right, top-center)",
            "Strength": numeric strength (1-10),
            "Meaning": "spiritual or mystical meaning",
            "Image": "image_[position].png"
        }},
        ...
    ],
    "final_reading": "A detailed narrative fortune based on the symbols above."
}}

Make the `final_reading` poetic and reflective. Only output valid JSON.

Here are the images:

- Left view: {left}
- Right view: {right}
- Up view: {up}
- Down view: {down}
- Top view: {top}
""".format(
    left=left_url,
    right=right_url,
    up=up_url,
    down=down_url,
    top=top_url
)

            try:
                response = model.generate_content(prompt)
                result = response.text
                st.subheader("🔮 Your Fortune Reading:")
                st.code(result, language='json')
            except Exception as e:
                st.error(f"❌ Error generating reading: {e}")
    else:
        st.warning("⚠️ Please enter all five image URLs.")
