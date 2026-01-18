import streamlit as st
from openai import OpenAI
import json

# --- IDENTITY RESET ---
st.set_page_config(page_title="Aura AI", page_icon="⭐")

# We use a unique ID here to force the phone to think it's a new app
m = {"name": "Aura AI", "short_name": "Aura", "display": "standalone", "id": "aura_v2"}

st.markdown(f"""
<head>
    <link rel="manifest" href='data:application/json,{json.dumps(m)}'>
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-title" content="Aura AI">
</head>
""", unsafe_allow_html=True)

# --- WORKING LOGIC ---
if "credits" not in st.session_state: st.session_state.credits = 50
if "all_chats" not in st.session_state: st.session_state.all_chats = {}
if "current_chat" not in st.session_state: st.session_state.current_chat = None

api_key = st.secrets.get("OPENROUTER_API_KEY")
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

with st.sidebar:
    st.title("Aura AI")
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
    st.metric("Free Chats Left", f"{st.session_state.credits}/50")

if st.session_state.current_chat:
    msgs = st.session_state.all_chats[st.session_state.current_chat]
    for m in msgs:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Ask Aura..."):
        st.session_state.credits = max(0, st.session_state.credits - 1)
        msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            r = client.chat.completions.create(model="google/gemma-3-27b-it:free", messages=msgs)
            ans = r.choices[0].message.content
            st.markdown(ans); msgs.append({"role": "assistant", "content": ans})
            st.rerun()
else:
    st.info("👋 Start a New Chat!")
