import streamlit as st
from openai import OpenAI

# 1. SIMPLE CONFIG
st.set_page_config(page_title="Aura AI", page_icon="⭐")

# 2. LOGIC
if "credits" not in st.session_state: st.session_state.credits = 50
if "all_chats" not in st.session_state: st.session_state.all_chats = {}
if "current_chat" not in st.session_state: st.session_state.current_chat = None

api_key = st.secrets.get("OPENROUTER_API_KEY")
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

# 3. SIDEBAR
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
    st.write("---")
    st.metric("Free Chats Left", f"{st.session_state.credits}/50")

# 4. CHAT
if st.session_state.current_chat:
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
                st.rerun()
            except Exception: st.error("Error. Try again.")
else:
    st.info("👋 Start a New Chat!")
