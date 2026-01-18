import streamlit as st
from openai import OpenAI

# 1. FORCE THE NAME INTO THE BROWSER TAB
st.set_page_config(page_title="Aura AI", page_icon="⭐")

# 2. THE "KILL STREAMLIT" HACK
# This CSS and HTML tries to overwrite the app name at the root level
st.markdown("""
    <script>
        // This tries to rename the app in the phone's memory
        window.parent.document.title = "Aura AI";
        document.title = "Aura AI";
    </script>
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { name: "Aura AI"; }
    </style>
""", unsafe_allow_html=True)

if "credits" not in st.session_state: st.session_state.credits = 50
if "all_chats" not in st.session_state: st.session_state.all_chats = {}
if "current_chat" not in st.session_state: st.session_state.current_chat = None

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=st.secrets["OPENROUTER_API_KEY"])

with st.sidebar:
    st.title("Aura AI")
    if st.button("➕ New Chat", use_container_width=True):
        cid = f"Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[cid] = []
        st.session_state.current_chat = cid
        st.rerun()
    for n in list(st.session_state.all_chats.keys()):
        if st.button(n, key=f"b_{n}", use_container_width=True):
            st.session_state.current_chat = n
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
    st.info("👋 Welcome to Aura AI!")
