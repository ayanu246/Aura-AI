import streamlit as st
from openai import OpenAI

# 1. Page Config
st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

# 2. OpenRouter Connection
if "OPENROUTER_API_KEY" in st.secrets:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
else:
    st.error("Missing API Key in Secrets!")
    st.stop()

# 3. Initialize "Multi-Chat" Memory
if "all_chats" not in st.session_state:
    # This stores multiple chat sessions
    st.session_state.all_chats = {"Chat 1": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

# 4. SIDEBAR - Chat Management
with st.sidebar:
    st.title("Aura History")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        new_id = f"Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    st.divider()

    # List of previous chats
    for chat_name in st.session_state.all_chats.keys():
        if st.button(chat_name, use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.divider()
    
    # Reset Current Chat Button
    if st.button("🗑️ Reset Current Chat", use_container_width=True):
        st.session_state.all_chats[st.session_state.current_chat] = []
        st.rerun()

# 5. MAIN CHAT AREA
current_messages = st.session_state.all_chats[st.session_state.current_chat]

# Display messages for the selected chat
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Logic
if prompt := st.chat_input(f"Message {st.session_state.current_chat}..."):
    # Save user message to the specific chat session
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Gemma 3 27B - The smartest free 2026 brain
            response = client.chat.completions.create(
                model="google/gemma-3-27b-it:free",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            # Save assistant message
            current_messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Aura is resting. Error: {e}")
