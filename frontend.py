import streamlit as st
import requests
import os

# 1. Page Configuration
st.set_page_config(page_title="EcoDispose AI UI", page_icon="♻️", layout="centered")

# 2. Inject Premium Flashy CSS Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;600;700&display=swap');
    
    /* Global Background and Typography */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: radial-gradient(circle at 50% 50%, #111622 0%, #070a10 100%) !important;
        color: #f3f4f6 !important;
    }

    /* Hide default Streamlit decoration and header links */
    [data-testid="stHeader"], footer {
        visibility: hidden;
    }

    /* Flashy Gradient Title & Glowing Effects */
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: -40px;
        margin-bottom: 2px;
        filter: drop-shadow(0px 4px 15px rgba(79, 172, 254, 0.4));
    }
    
    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 1.05rem;
        margin-bottom: 35px;
    }

    /* Glassmorphic Chat Message Container Overrides */
    [data-testid="stChatMessage"] {
        background: rgba(22, 30, 47, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        margin-bottom: 12px !important;
        transition: all 0.2s ease-in-out;
    }
    
    [data-testid="stChatMessage"]:hover {
        border-color: rgba(79, 172, 254, 0.2) !important;
        box-shadow: 0 8px 32px rgba(79, 172, 254, 0.05) !important;
    }

    /* Specific highlights for the User Message Bubble */
    [data-testid="stChatMessageUser"] {
        background: rgba(79, 172, 254, 0.12) !important;
        border: 1px solid rgba(79, 172, 254, 0.25) !important;
    }

    /* Custom Chat Input Adjustments */
    [data-testid="stChatInput"] {
        border-radius: 12px !important;
        border: 1px solid #232d42 !important;
        background-color: #151c2c !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Render Flashy Visual Header
st.markdown('<h1 class="main-title">♻️ EcoDispose AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Navigate complex municipal recycling directories and verified vendor networks instantly.</p>', unsafe_allow_html=True)

# 4. Environment and Endpoint Management
BASE_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
BACKEND_URL = f"{BASE_URL}/api/chat"

# Initialize Session Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages with Premium Custom Container Designs
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Engagement Interface Input
user_input = st.chat_input("Ask a recycling question (e.g., 'Where do I drop off old laptop batteries?')")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("Retrieving local environmental policies & vendor directories..."):
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