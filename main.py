# import streamlit as st
# import requests
# import os
# from dotenv import load_dotenv

# # Load the GEMINI_API_KEY from the .env file
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# if GEMINI_API_KEY is None:
#     st.error("❌ GEMINI_API_KEY not found. Please check your .env file.")
#     st.stop()

# # Gemini Pro endpoint and headers
# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
# HEADERS = {"Content-Type": "application/json"}

# # Prompt template
# PROMPT_TEMPLATE = {
#     "language": "English",
#     "images": [],
#     "instruction": (
#         "From the provided images of a coffee cup taken from different angles, "
#         "analyze and return a detailed horoscope-style reading. Format your response as JSON in this structure: "
#         "{ 'readings': [...], 'final_reading': '...full fortune text...' }. "
#         "Ensure observations like objects, their locations, and associated meanings are clearly mentioned and "
#         "output is in beautiful narrative style."
#     )
# }

# # Helper function to build prompt with image positions
# def build_prompt(image_urls):
#     prompt = PROMPT_TEMPLATE.copy()
#     prompt["images"] = [
#         {"url": url, "position": position} for url, position in image_urls
#     ]
#     return prompt

# # Streamlit UI
# st.set_page_config(page_title="☕ AI Coffee Cup Fortune Teller", layout="centered")
# st.title("🔮 Coffee Cup Fortune Teller")
# st.markdown("Upload coffee cup image URLs from different angles and discover your mystical fortune!")

# # Input Form
# with st.form("fortune_form"):
#     st.markdown("### 📷 Enter image URLs from various angles")
#     left = st.text_input("Left view image URL")
#     right = st.text_input("Right view image URL")
#     up = st.text_input("Up view image URL")
#     down = st.text_input("Down view image URL")
#     top = st.text_input("Top view image URL")
#     submitted = st.form_submit_button("✨ Get My Fortune")

# # On Submit
# if submitted:
#     image_inputs = [
#         (left, "left"),
#         (right, "right"),
#         (up, "up"),
#         (down, "down"),
#         (top, "top")
#     ]

#     # Filter valid URLs
#     valid_inputs = [(url, pos) for url, pos in image_inputs if url.strip() != ""]

#     if len(valid_inputs) < 1:
#         st.warning("⚠️ Please enter at least one image URL.")
#     else:
#         st.info("🔍 Analyzing your cup images... please wait...")

#         # Build the prompt
#         prompt_data = build_prompt(valid_inputs)

#         # Send request to Gemini
#         payload = {
#             "contents": [
#                 {
#                     "parts": [
#                         {
#                             "text": str(prompt_data)
#                         }
#                     ]
#                 }
#             ]
#         }

#         try:
#             response = requests.post(GEMINI_URL, headers=HEADERS, json=payload)
#             if response.status_code == 200:
#                 gemini_reply = response.json()
#                 text = gemini_reply['candidates'][0]['content']['parts'][0]['text']
#                 st.success("🌟 Your Coffee Cup Reading is Ready!")
#                 st.markdown("### 📜 Reading Output")
#                 st.code(text, language='json')
#             else:
#                 st.error(f"❌ Gemini API Error {response.status_code}")
#                 st.error(response.text)
#         except Exception as e:
#             st.error("❌ Failed to connect to Gemini API.")
#             st.error(str(e))


# ------------------------------------------------------------------------
#### For testing image url 
# View	Image URL
# Left	https://i.imgur.com/FLeS2Gp.jpg
# Right	https://i.imgur.com/mRNHXPa.jpg
# Up	https://i.imgur.com/VNKQkJ4.jpg
# Down	https://i.imgur.com/fX3tERz.jpg
# Top	https://i.imgur.com/Gzcf0AU.jpg

# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------


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
