import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

def render_chat_ui():
    st.markdown("### Patient Support Chat")
    st.markdown(
        "Ask discharge-related questions, medication advice, or symptoms."
    )

    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])


    user_input = st.chat_input("Type your message here...")

    if user_input:
        
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(API_URL, json={"message": user_input}, timeout=120)
                    if res.status_code == 200:
                        reply = res.json().get("response", "No response from backend.")
                    else:
                        reply = f"Server Error: {res.status_code}"
                except Exception as e:
                    reply = f"Connection Error: {str(e)}"

                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "text": reply})
