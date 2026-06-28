import streamlit as st
import requests
import os

# 1. Page Configuration
st.set_page_config(page_title="EcoDispose AI UI", page_icon="♻️", layout="centered")

# 2. Inject Max-Flashy Animated CSS Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* 1. Animated Mesh Background */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: linear-gradient(-45deg, #090d16, #111726, #05070f, #141c30) !important;
        background-size: 400% 400% !important;
        animation: gradient 15s ease infinite !important;
        color: #f3f4f6 !important;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Hide standard header elements */
    [data-testid="stHeader"], footer {
        visibility: hidden;
    }

    /* 2. Header Container with Status Badge */
    .header-container {
        text-align: center;
        margin-top: -30px;
        margin-bottom: 30px;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 12px;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.1);
    }
    
    .badge::before {
        content: '';
        display: inline-block;
        width: 6px;
        height: 6px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }

    /* 3. Pulsing Glow Text Effect */
    .main-title {
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding-bottom: 5px;
        animation: titleGlow 4s ease-in-out infinite alternate;
    }
    
    .subtitle {
        color: #9ca3af;
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 8px;
    }

    @keyframes titleGlow {
        0% { filter: drop-shadow(0 2px 8px rgba(79, 172, 254, 0.2)); }
        100% { filter: drop-shadow(0 4px 20px rgba(0, 242, 254, 0.5)); }
    }
    
    @keyframes pulse {
        0% { transform: scale(0.9); opacity: 0.6; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.6; }
    }

    /* 4. Entry Fade Animation for Chat Boxes */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stChatMessage"] {
        background: rgba(22, 30, 49, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
        border-radius: 16px !important;
        padding: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        margin-bottom: 16px !important;
        animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        transition: all 0.25s ease;
    }
    
    [data-testid="stChatMessage"]:hover {
        border-color: rgba(79, 172, 254, 0.3) !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(79, 172, 254, 0.08) !important;
    }

    [data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.15), rgba(0, 242, 254, 0.05)) !important;
        border: 1px solid rgba(79, 172, 254, 0.3) !important;
    }

    /* 5. Sleek Neon Floating Input Box */
    [data-testid="stChatInput"] {
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        background-color: rgba(21, 28, 44, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 -10px 35px rgba(0, 0, 0, 0.2), 0 15px 35px rgba(0, 0, 0, 0.4) !important;
        transition: border-color 0.3s ease;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(0, 242, 254, 0.5) !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Render Custom Dash Structure
st.markdown("""
    <div class="header-container">
        <span class="badge">Engine Status: Active</span>
        <h1 class="main-title">♻️ EcoDispose AI</h1>
        <p class="subtitle">Intelligent Urban Directory for E-Waste Logistics & Compliance</p>
    </div>
""", unsafe_allow_html=True)

# 4. Networking Architecture Configuration
BASE_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
BACKEND_URL = f"{BASE_URL}/api/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messaging Matrix
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Search Intercept Entry
user_input = st.chat_input("Query directories, collection hubs, or corporate data handles...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("Parsing target metadata repositories..."):
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