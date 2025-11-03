import streamlit as st
from components.chat_ui import render_chat_ui
from PIL import Image
import os

# Streamlit page configuration
st.set_page_config(
    page_title="Post-Discharge Medical AI Assistant",
    page_icon="💊",
    layout="centered"
)
# Display logo
logo_path = os.path.join("frontend", "assets", "images.png")
if os.path.exists(logo_path):
    st.image(Image.open(logo_path), width=120)
else:
    st.warning("Logo not found — add it at frontend/assets/images.png")
# Title and description
st.title("Post-Discharge Medical AI Assistant")
st.markdown(
    """
    Welcome to your **Post-Discharge AI Assistant** —  
    helping patients manage recovery after discharge through:
    - **Receptionist Agent** for patient lookup  
    - **Clinical Agent (RAG + Web Search)** for medical responses  
    'This is an AI assistant for educational purposes only' and
'   Always consult healthcare professionals for medical advice'
    """
)

# Divider
st.divider()
# Render chat UI
render_chat_ui()
