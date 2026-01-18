import streamlit as st
from openai import OpenAI
import requests

# 1. Page Config
st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

# 2. Connection Logic
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
else:
    st.error("Add your OPENROUTER_API_KEY to Streamlit Secrets!")
    st.stop()

# 3. Memory Setup
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# Function to get your 2026 Free Credit Count
def get_remaining_credits():
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://openrouter.ai/api/v1/key", headers=headers)
        data = response.json()
        usage = data.get("data", {}).get("usage_daily", 0)
        return max(0, 50 - int(usage))
    except:
        return "50"

# 4. SIDEBAR
with st.sidebar:
    st.title("Aura History")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_id = f"New Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    st.divider()

    # Show History
    for chat_name in list(st.session_state.all_chats.keys()):
        if st.button(chat_name, key=f"btn_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.divider()
    if st.button("🗑️ Reset Chat", use_container_width=True) and st.session_state.current_chat:
        st.session_state.all_chats[st.session_state.current_chat] = []
        st.rerun()

    # Credit Tracker at bottom
    st.write("---")
    remaining = get_remaining_credits()
    st.metric(label="Free Chats Left", value=
