import streamlit as st
from openai import OpenAI
import requests

# --- 1. BRANDING & MOBILE APP SETTINGS ---
APP_NAME = "Aura AI"
ICON_URL = "https://github.com/ayanu246/Aura-AI/blob/main/Logo.png?raw=true"

# This sets the browser tab title and icon
st.set_page_config(page_title=APP_NAME, page_icon=ICON_URL)

# This "forces" the phone to use your name and icon for the home screen
st.markdown(f"""
    <head>
        <title>{APP_NAME}</title>
        <link rel="apple-touch-icon" href="{ICON_URL}">
        <link rel="icon" href="{ICON_URL}">
        <meta name="apple-mobile-web-app-title" content="{APP_NAME}">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="mobile-web-app-capable" content="yes">
    </head>
""", unsafe_allow_html=True)

# --- 2. API CONNECTION ---
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
else:
    st.error("Missing OPENROUTER_API_KEY in Streamlit Secrets!")
    st.stop()

# --- 3. MEMORY & STORAGE ---
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

# --- 4. SIDEBAR (History, New Chat, Reset, Credits) ---
with st.sidebar:
    # Your Logo at the top
    st.image(ICON_URL, width=100)
    st.title("Aura History")
    
    # Create a new chat
    if st.button("➕ New Chat", use_container_width=True):
        new_id = f"New Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    st.divider()

    # List of saved chats
    for chat_name in list(st.session_state.all_chats.keys()):
        if st.button(chat_name, key=f"btn_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.divider()
    
    # Reset current chat
    if st.button("🗑️ Reset Current Chat", use_container_width=True) and st.session_state.current_chat:
        st.session_state.all_chats[st.session_state.current_chat] = []
        st.rerun()

    # Credit Tracker Meter
    st.write("---")
    remaining = get_remaining_credits()
    st.metric(label="Free Chats Left", value=f"{remaining}/50")
    st.caption("Resets daily at Midnight UTC")

# --- 5. MAIN CHAT INTERFACE ---
if st.session_state.current_chat:
    st.subheader(f"Chat: {st.session_state.current_chat}")
    messages = st.session_state.all_chats[st.session_state.current_chat]

    # Show past messages
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User chat input
    if prompt := st.chat_input("Ask Aura..."):
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Get response from Gemma 3 (Free)
                response = client.chat.completions.create(
                    model="google/gemma-3-27b-it:free",
                    messages=messages
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                messages.append({"role": "assistant", "content": answer})

                # Auto-rename the chat based on the first question
                if len(messages) <= 2:
                    name_res = client.chat.completions.create(
                        model="google/gemma-3-27b-it:free",
                        messages=[{"role": "user", "content": f"Summarize to 2 words: {prompt}"}]
                    )
                    new_name = name_res.choices[0].message.content.strip().replace('"', '')
                    st.session_state.all_chats[new_name] = st.session_state.all_chats.pop(st.session_state.current_
