import streamlit as st
from openai import OpenAI
import json

# --- 1. BRANDING & IDENTITY FORCE ---
APP_NAME = "Aura AI"
ICON_URL = "https://github.com/ayanu246/Aura-AI/blob/main/Logo.png?raw=true"

st.set_page_config(page_title=APP_NAME, page_icon=ICON_URL)

# This tells the phone's "Install" popup what name to show
manifest_data = {
    "short_name": "Aura AI",
    "name": "Aura AI",
    "icons": [{"src": ICON_URL, "sizes": "512x512", "type": "image/png"}],
    "start_url": ".",
    "display": "standalone"
}

st.markdown(f"""
    <head>
        <link rel="apple-touch-icon" href="{ICON_URL}">
        <meta name="apple-mobile-web-app-title" content="Aura AI">
        <meta name="application-name" content="Aura AI">
        <link rel="manifest" href='data:application/json,{json.dumps(manifest_data)}'>
    </head>
""", unsafe_allow_html=True)

# --- 2. INSTANT COUNTER ---
if "credits" not in st.session_state:
    st.session_state.credits = 50

# --- 3. API SETUP ---
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
else:
    st.error("Missing API Key!"); st.stop()

# --- 4. MEMORY ---
if "all_chats" not in st.session_state: st.session_state.all_chats = {}
if "current_chat" not in st.session_state: st.session_state.current_chat = None

# --- 5. SIDEBAR ---
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
    st.metric(label="Free Chats Left", value=f"{st.session_state.credits}/50")

# --- 6. CHAT ---
if st.session_state.current_chat:
    st.subheader(f"Chat: {st.session_state.current_chat}")
    msgs = st.session_state.all_chats[st.session_state.current_chat]
    
    for m in msgs:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Ask Aura..."):
        st.session_state.credits = max(0, st.session_state.credits - 1)
        msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        with st.chat_message("assistant"):
            try:
                r = client.chat.completions.create(model="google/gemma-3-27b-it:free", messages=msgs)
                ans = r.choices[0].message.content
                st.markdown(ans); msgs.append({"role": "assistant", "content": ans})
                
                if len(msgs) <= 2:
                    sr = client.chat.completions.create(model="google/gemma-3-27b-it:free", 
                        messages=[{"role": "user", "content": f"Summarize to 2 words: {p}"}])
                    nn = sr.choices[0].message.content.strip().replace('"', '')
                    st.session_state.all_chats[nn] = st.session_state.all_chats.pop(st.session_state.current_chat)
                    st.session_state.current_chat = nn
                st.rerun()
            except Exception as e: st.error(f"Error: {e}")
else:
    st.info("👋 Welcome! Tap 'New Chat' to begin.")
