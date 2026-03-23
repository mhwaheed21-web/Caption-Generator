import streamlit as st
import os
import sys

# Import backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import process_video

# -------------------------------
# CONFIG
# -------------------------------
UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(
    page_title="Video Caption Generator",
    layout="centered"
)

# -------------------------------
# UI
# -------------------------------
st.title("🎬 AI Video Caption Generator")
st.markdown("Upload a video → Generate captions → Watch output")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

if uploaded_file:
    video_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    # Save file
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.subheader("📥 Input Video")
    st.video(video_path)

    if st.button("Generate Captions 🚀"):
        try:
            with st.spinner("Processing... This may take time ⏳"):
                output_video = process_video(video_path, UPLOAD_DIR)

            st.success("✅ Captions Generated!")

            st.subheader("🎥 Output Video")
            st.video(output_video)

            # Download
            with open(output_video, "rb") as f:
                st.download_button(
                    label="📥 Download Video",
                    data=f,
                    file_name="captioned_video.mp4",
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(f"Error: {e}")