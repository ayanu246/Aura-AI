import streamlit as st
from openai import OpenAI
import requests, json, time

# 1. BRANDING
APP_NAME = "Aura AI"
ICON_URL = "https://github.com/ayanu246/Aura-AI/blob/main/Logo.png?raw=true"
st.set_page_config(page_title=APP_NAME, page_icon=ICON_URL)

# Mobile Identity Fix
m = {"name": APP_NAME, "short_name": APP_NAME, "display": "standalone"}
st.markdown(f"""
<head>
    <link rel="apple-touch-icon" href="{ICON_URL}"><link rel="icon" href="{ICON_URL}">
    <meta name="apple-mobile-web-app-title" content="{APP_NAME}">
    <link rel="manifest" href='data:application/json,{json.dumps(m)}'>
</head>""", unsafe_allow_html=True)

# 2. API
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
else:
    st.error("Add Key to Secrets!"); st.stop()

# 3. STATE
if "all_chats" not in st.session_state: st.session_state.all_chats = {}
if "current_chat" not in st.session_state: st.session_state.current_chat = None

# 4. FIXED CREDIT METER (Forced Update)
def get_credits():
    try:
        h = {"Authorization": f"Bearer {api_key}"}
        # The 't' parameter at the end forces a fresh count from the server
        url = f"https://openrouter.ai/api/v1/key?t={time.time()}"
        r = requests.get(url, headers=h, timeout=5)
        usage = r.json().get("data", {}).get("usage_daily", 0)
        return max(0, 50 - int(usage))
    except: return "50"

# 5. SIDEBAR
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
    # Fresh credits display
    st.metric(label="Free Chats Left", value=f"{get_credits()}/50")

# 6. CHAT
if st.session_state.current_chat:
    st.subheader(f"Chat: {st.session_state.current_chat}")
    msgs = st.session_state.all_chats[st.session_state.current_chat]
    for m in msgs:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Ask Aura..."):
        msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            try:
                r = client.chat.completions.create(model="google/gemma-3-27b-it:free", messages=msgs)
                ans = r.choices[0].message.content
                st.markdown(ans); msgs.append({"role": "assistant", "content": ans})
                if len(msgs) <= 2:
                    sr = client.chat.completions.create(model="google/gemma-3-27b-it:free", 
                        messages=[{"role": "user", "content": f"Summarize 2 words: {p}"}])
                    nn = sr.choices[0].message.content.strip().replace('"', '')
                    st.session_state.all_chats[nn] = st.session_state.all_chats.pop(st.session_state.current_chat)
                    st.session_state.current_chat = nn
                st.rerun()
            except Exception as e: st.error(f"Error: {e}")
else:
    st.info("👋 Tap 'New Chat' to start!")
