import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Aura AI", page_icon="✨")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # This is the most compatible name for new API keys
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key missing in Secrets!")
    st.stop()

if 'user_name' not in st.session_state:
    st.title("Welcome to Aura AI ✨")
    name = st.text_input("What is your name?")
    if st.button("Begin"):
        if name:
            st.session_state.user_name = name
            st.rerun()
else:
    st.title("Aura AI is active. ✨")
    user_query = st.text_area("Ask me anything in the world:")

    if st.button("Ask Aura"):
        if user_query:
            with st.spinner("Thinking..."):
                try:
                    # The 'stream=False' forces a standard, non-beta connection
                    response = model.generate_content(user_query, stream=False)
                    st.markdown("---")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Aura had a tiny glitch: {e}")
