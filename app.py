import streamlit as st
from openai import OpenAI
import requests

# --- 1. BRANDING & MOBILE APP SETTINGS ---
APP_NAME = "Aura AI"
ICON_URL = "https://github.com/ayanu246/Aura-AI/blob/main/Logo.png?raw=true"

st.set_page_config(page_title=APP_NAME, page_icon=ICON_URL)

# Home Screen Icon Support
st.markdown(f"""
    <head>
        <link rel="apple-touch-icon" href="{ICON_URL}">
        <link rel="icon" href="{ICON_URL}">
        <meta name="apple-mobile-web-app-title" content="{APP_NAME}">
        <meta name="apple-mobile-web-app-capable" content="yes">
    </head>
""", unsafe_allow_html=True)

# --- 2. API CONNECTION ---
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
else:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

# --- 3. MEMORY & STORAGE ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

def get_remaining_credits():
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        res = requests.get("https://openrouter.ai/api/v1/key", headers=headers, timeout=5)
        usage = res.json().get("data", {}).get("usage_daily", 0)
        return max(0, 50 - int(usage))
    except:
        return "50"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image(ICON_URL, width=100)
    st.title("Aura History")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_id = f"Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    st.divider()

    for chat_name in list(st.session_state.all_chats.keys()):
        if st.button(chat_name, key=f"btn_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.divider()
    
    if st.button("🗑️ Reset Chat", use_container_width=True)
