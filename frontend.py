import streamlit as st
import requests
import os

st.set_page_config(page_title="EcoDispose AI UI", page_icon="♻️", layout="centered")

st.title("♻️ EcoDispose AI: Urban E-Waste Assistant")
st.write("Navigate complex municipal recycling rules instantly via our verified AI knowledge engine.")

# Dynamic URL router: If hosted on Render, it communicates with the Render backend web service. 
# Locally, it falls back seamlessly to localhost.
if "RENDER" in os.environ:
    # Replace this string with your actual backend service URL once Render deploys it
    BACKEND_URL = "https://ecodispose-backend.onrender.com/api/chat"
else:
    BACKEND_URL = "http://127.0.0.1:8000/api/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask a recycling question (e.g., 'Where do I drop off old laptop batteries?')")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("Retrieving local environmental policies..."):
            try:
                api_response = requests.post(BACKEND_URL, json={"question": user_input})
                if api_response.status_code == 200:
                    bot_answer = api_response.json().get("answer", "No payload content.")
                    st.write(bot_answer)
                    st.session_state.messages.append({"role": "assistant", "content": bot_answer})
                else:
                    st.error(f"Backend Returned Error: {api_response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Is your FastAPI backend API service actively running?")