import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

# 2. The Connection Fix (Bypasses the 404 v1beta error)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        # 'transport=rest' is the magic key that stops the v1beta glitch
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
        
        # We use the most stable model version available
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("✅ Aura is connected and online!")
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.error("API Key not found! Please check your Streamlit Secrets.")
    st.stop()

# 3. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask Aura anything..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display Aura's response
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Aura glitch: {e}")

# 4. Sidebar Tools
with st.sidebar:
    st.title("Settings")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
