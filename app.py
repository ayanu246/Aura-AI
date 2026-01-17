import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Aura AI", page_icon="✨", layout="centered")
st.title("Aura AI ✨")

# 2. THE STABLE FIX (This stops the 404 error)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        # We force 'transport=rest' to avoid the v1beta bug
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
        
        # We use 'gemini-1.5-flash' - the most stable 2026 model
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.caption("🟢 Aura System: Online & Stable")
    except Exception as e:
        st.error(f"Connection failed: {e}")
else:
    st.error("Please add your GOOGLE_API_KEY to Streamlit Secrets!")
    st.stop()

# 3. Chat Layout Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Input (Bottom of screen)
if prompt := st.chat_input("Ask Aura anything..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Aura's response
    with st.chat_message("assistant"):
        try:
            # The stable generate call
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # If a glitch happens, this shows exactly why
            st.error(f"Aura glitch: {e}")

# 5. Sidebar Reset
with st.sidebar:
    st.header("Aura Controls")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
