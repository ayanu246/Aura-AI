import streamlit as st
from openai import OpenAI
import time

# --- 1. BASIC PAGE CONFIG (No hidden app manifest) ---
st.set_page_config(
    page_title="Aura AI",
    page_icon="https://github.com/ayanu246/Aura-AI/blob/main/Logo.png?raw=true",
    layout="centered"
)

# --- 2. INSTANT CREDIT COUNTER ---
if "credits" not in st.session_state:
    st.session_state.credits = 50

# --- 3. API SETUP ---
# Make sure "OPENROUTER_API_KEY" is in your Streamlit Secrets!
if "OPENROUTER_API_KEY" in st.secrets:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
else:
    st.error("Please add OPENROUTER_API_KEY to your Streamlit Secrets.")
    st.stop()

# --- 4. CHAT HISTORY STORAGE ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# --- 5. SIDEBAR (History & Credits) ---
with st.sidebar:
    st.image("https://github.com/ayanu246/Aura-AI/blob/main/Logo.png?raw=true", width=100)
    st.title("Aura History")
    
    if st.button("➕ New Chat", use_container_width=True):
        chat_id = f"Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()

    st.divider()
    
    # List previous chats
    for chat_name in list(st.session_state.all_chats.keys()):
        if st.button(chat_name, key=f"btn_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.divider()
    
    if st.button("🗑️ Reset All Chats", use_container_width=True):
        st.session_state.all_chats = {}
        st.session_state.current_chat = None
        st.rerun()

    st.write("---")
    # THE INSTANT COUNTER
    st.metric(label="Free Chats Left", value=f"{st.session_state.credits}/50")

# --- 6. MAIN CHAT INTERFACE ---
if st.session_state.current_chat:
    st.subheader(f"Talking to {st.session_state.current_chat}")
    
    # Display message history
    messages = st.session_state.all_chats[st.session_state.current_chat]
    for m in messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # User Input
    if prompt := st.chat_input("Ask Aura..."):
        # 1. Update Credits Immediately
        st.session_state.credits = max(0, st.session_state.credits - 1)
        
        # 2. Add user message
        messages.append({"role
