import streamlit as st
from openai import OpenAI
import requests
import json

# --- 1. BRANDING & MOBILE IDENTITY ---
APP_NAME = "Aura AI"
ICON_URL = "https://github.com/ayanu246/Aura-AI/blob/main/Logo.png?raw=true"

st.set_page_config(page_title=APP_NAME, page_icon=ICON_URL)

# This Manifest forces the phone to name the app "Aura AI"
manifest = {"name": APP_NAME, "short_name": APP_NAME, "display": "standalone"}
m_str = json.dumps(manifest)

st.markdown(f"""
<head>
    <link rel="apple-touch-icon" href="{ICON_URL}">
    <link rel="icon" href="{ICON_URL}">
    <meta name="apple-mobile-web-app-title" content="{APP_NAME}">
    <link rel="manifest" href='data:application/json,{m_str}'>
</head>
""", unsafe_allow_html=True)

# --- 2. API CONNECTION ---
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
else:
    st.error("Add Key to Secrets!")
    st.stop()

# --- 3. STORAGE & CREDITS ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

def get_credits():
    try:
        h = {"Authorization": f"Bearer {api_key}"}
        r = requests.get("https://openrouter.ai/api/v1/key", headers=h, timeout=5)
        usage = r.json().get("data", {}).get("usage_daily", 0)
        return max(0, 50 - int(usage))
    except:
        return "50"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image(ICON_URL, width=100)
    st.title("Aura History")
    
    if st.button("➕ New Chat", use_container_width=True):
        cid = f"Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[cid] = []
        st.session_state.current_chat = cid
        st.rerun()

    st.divider()
    for name in list(st.session_state.all_chats.keys()):
        if st.button(name, key=f"b_{name}", use_container_width=True):
            st.session_state.current_chat = name
            st.rerun()

    st.divider()
    if st.button("🗑️ Reset Chat", use_container_width=True):
        if st.session_state.current_chat:
            st.session_state.all_chats[st.session_state.current_chat] = []
            st.rerun()

    st.write("---")
    # This fetches fresh credits every time the sidebar loads
    rem = get_credits()
    st.metric(label="Free Chats Left Today", value=f"{rem}/50")

# --- 5. CHAT AREA ---
if st.session_state.current_chat:
    st.subheader(f"Chat: {st.session_state.current_chat}")
    msgs = st.session_state.all_chats[st.session_state.current_chat]

    for m in msgs:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if p := st.chat_input("Ask Aura..."):
        msgs.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)

        with st.chat_message("assistant"):
            try:
                # Main response
                r = client.chat.completions.create(
                    model="google/gemma-3-27b-it:free",
                    messages=msgs
                )
                ans = r.choices[0].message.content
                st.markdown(ans)
                msgs.append({"role": "assistant", "content": ans})

                # Rename logic
                if len(msgs) <= 2:
                    sr = client.chat.completions.create(
                        model="google/gemma-3-27b-it:free",
                        messages=[{"role": "user
