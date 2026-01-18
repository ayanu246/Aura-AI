import streamlit as st
from openai import OpenAI
import requests

# --- 1. BRANDING & CONFIG ---
ICON_URL = "https://github.com/ayanu246/Aura-AI/blob/main/Logo.png?raw=true" 

st.set_page_config(page_title="Aura AI", page_icon=ICON_URL)

# Home Screen Icon Support
st.markdown(f'<link rel="apple-touch-icon" href="{ICON_URL}">', unsafe_allow_html=True)
st.markdown(f'<link rel="icon" href="{ICON_URL}">', unsafe_allow_html=True)

# --- 2. SECURE CONNECTION ---
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
else:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

# --- 3. STATE MANAGEMENT ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

def get_remaining_credits():
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://openrouter.ai/api/v1/key", headers=headers, timeout=5)
        data = response.json()
        usage = data.get("data", {}).get("usage_daily", 0)
        return max(0, 50 - int(usage))
    except:
        return "50"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image(ICON_URL, width=80)
    st.title("Aura History")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_id = f"New Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    st.divider()

    for chat_name in list(st.session_state.all_chats.keys()):
        if st.button(chat_name, key=f"btn_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.divider()
    
    if st.button("🗑️ Reset Current Chat", use_container_width=True) and st.session_state.current_chat:
        st.session_state.all_chats[st.session_state.current_chat] = []
        st.rerun()

    st.write("---")
    remaining_count = get_remaining_credits()
    st.metric(label="Daily Credits Left", value=f"{remaining_count}/50")

# --- 5. MAIN CHAT AREA ---
if st.session_state.current_chat:
    # Fixed the line that caused the error
    st.subheader(f"Chat: {st.session_state.current_chat}")

    messages = st.session_state.all_chats[st.session_state.current_chat]

    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Message Aura..."):
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="google/gemma-3-27b-it:free",
                    messages=messages
                )
                answer = response.choices[0].message.
