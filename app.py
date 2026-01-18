import streamlit as st
from openai import OpenAI

# 1. Page Config & Title
st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

# 2. Connection
if "OPENROUTER_API_KEY" in st.secrets:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
else:
    st.error("Add your OPENROUTER_API_KEY to Streamlit Secrets!")
    st.stop()

# 3. Memory Structure
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} # Stores { "Chat Name": [messages] }
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# 4. SIDEBAR
with st.sidebar:
    st.title("Aura History")
    
    if st.button("➕ New Chat", use_container_width=True):
        # Create a temp name; it will be renamed after the first message
        new_id = f"New Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    st.divider()

    # List chats and let user select them
    for chat_name in list(st.session_state.all_chats.keys()):
        if st.button(chat_name, key=chat_name, use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.divider()
    if st.button("🗑️ Reset Current Chat", use_container_width=True) and st.session_state.current_chat:
        st.session_state.all_chats[st.session_state.current_chat] = []
        st.rerun()

# 5. MAIN CHAT LOGIC
if st.session_state.current_chat:
    messages = st.session_state.all_chats[st.session_state.current_chat]

    # Show past messages
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Types Here
    if prompt := st.chat_input("Ask Aura..."):
        # 1. Add User Message
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Get AI Response
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="google/gemma-3-27b-it:free",
                    messages=messages
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                messages.append({"role": "assistant", "content": answer})

                # 3. AUTO-RENAME (Only if it's the first message)
                if len(messages) <= 2: # 1 user msg + 1 AI msg
                    title_request = client.chat.completions.create(
                        model="google/gemma-3-27b-it:free",
                        messages=[{"role": "user", "content": f"Summarize this into a 2-word title: {prompt}"}]
                    )
                    new_title = title_request.choices[0].message.content.replace('"', '').strip()
                    
                    # Update the dictionary key
                    st.session_state.all_chats[new_title] = st.session_state.all_chats.pop(st.session_state.current_chat)
                    st.session_state.current_chat = new_title
                    st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Click 'New Chat' in the sidebar to start talking to Aura!")
