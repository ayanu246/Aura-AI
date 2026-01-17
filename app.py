import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Aura AI", page_icon="✨")

# FORCE THE CONNECTION TO STABLE V1
if "GOOGLE_API_KEY" in st.secrets:
    # This line tells Google: "Don't use v1beta, use the stable version!"
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
    # Using the name exactly as it appears in the stable library
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing API Key in Streamlit Secrets!")
    st.stop()

if 'user_name' not in st.session_state:
    st.title("Welcome to Aura AI ✨")
    name = st.text_input("What is your name?")
    if st.button("Start"):
        st.session_state.user_name = name
        st.rerun()
else:
    st.title(f"Aura AI is active. ✨")
    query = st.text_area("Ask me anything:")
    if st.button("Ask Aura"):
        with st.spinner("Thinking..."):
            try:
                # We do not use stream=True to keep it simple and stable
                response = model.generate_content(query)
                st.write("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"Aura had a glitch: {e}")
