import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import base64
import io

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY not found in .env file.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-pro-vision")

# Streamlit UI
st.set_page_config(page_title="Coffee Cup Fortune Teller ☕🔮", page_icon="☕")
st.title("🔮 Coffee Cup Fortune Teller")
st.markdown("Upload 5 coffee cup images from different angles to discover your mystical fortune.")

# Upload inputs
left = st.file_uploader("📷 Upload Left view image", type=["png", "jpg", "jpeg", "webp"])
right = st.file_uploader("📷 Upload Right view image", type=["png", "jpg", "jpeg", "webp"])
up = st.file_uploader("📷 Upload Up view image", type=["png", "jpg", "jpeg", "webp"])
down = st.file_uploader("📷 Upload Down view image", type=["png", "jpg", "jpeg", "webp"])
top = st.file_uploader("📷 Upload Top view image", type=["png", "jpg", "jpeg", "webp"])

def get_image_parts(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return {"mime_type": "image/jpeg", "data": buffered.getvalue()}
    return None

if st.button("🔍 Reveal My Fortune"):
    if all([left, right, up, down, top]):
        with st.spinner("Reading the coffee grounds..."):

            # Prepare image parts
            image_parts = {
                "left": get_image_parts(left),
                "right": get_image_parts(right),
                "up": get_image_parts(up),
                "down": get_image_parts(down),
                "top": get_image_parts(top),
            }

            prompt_text = """
You are a mystical coffee cup fortune teller. Based on the uploaded coffee cup images from five angles (left, right, up, down, top), interpret the coffee grounds and return a detailed JSON response in the following structure:

{
  "readings": [
    {
      "Observation": "symbol name (e.g., Tree, Fish, Mountain)",
      "Location": "e.g., bottom-left, center-right",
      "Strength": strength score (1-10),
      "Meaning": "spiritual or mystical meaning",
      "Image": "image_position.png"
    }
  ],
  "final_reading": "a poetic and insightful summary of the overall fortune based on the readings"
}

Be creative, but always stick to this JSON structure. Do not include any explanation outside of the JSON.
"""

            # Build parts list for Gemini input
            parts = [{"text": prompt_text}]
            for position, image_data in image_parts.items():
                parts.append({
                    "inline_data": image_data
                })

            try:
                response = model.generate_content(parts)
                result = response.text
                st.subheader("🌟 Your Fortune Reading:")
                st.code(result, language="json")
            except Exception as e:
                st.error(f"❌ Error generating reading: {e}")
    else:
        st.warning("⚠️ Please upload all five images.")
