import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Aura AI", page_icon="✨")

# This is the part that fixes the 404
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # We use 'gemini-pro' because it is the most stable for v1 connections
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("Missing API Key!")
    st.stop()

if 'user_name' not in st.session_state:
    st.title("Welcome to Aura AI ✨")
    name = st.text_input("What is your name?")
    if st.button("Start"):
        st.session_state.user_name = name
        st.rerun()
else:
    st.title("Aura AI is active. ✨")
    query = st.text_area("Ask me anything:")
    if st.button("Ask Aura"):
        with st.spinner("Thinking..."):
            try:
                # This is the line that actually gets the answer
                response = model.generate_content(query)
                st.write("---")
                st.write(response.text)
            except Exception as e:
                # If it fails, this will show us why
                st.error(f"Aura had a glitch: {e}")
