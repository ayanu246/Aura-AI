import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Aura AI", page_icon="✨")

# 2. Connect to the Brain
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Using the FULL path to the model to avoid the 404 error
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.error("Wait! I need my API Key. Please add it to Streamlit Secrets.")
    st.stop()

# 3. Welcome Logic
if 'user_name' not in st.session_state:
    st.title("Welcome to Aura AI ✨")
    name = st.text_input("I can answer anything in the world. What is your name?")
    if st.button("Begin My Journey"):
        if name:
            st.session_state.user_name = name
            st.rerun()
else:
    # 4. The Interactive AI Chat
    st.title(f"Aura AI is active. ✨")
    st.write(f"Hello {st.session_state.user_name}, I am ready for your questions.")

    user_query = st.text_area("Ask me any question in the world:", placeholder="Type here...")

    if st.button("Ask Aura"):
        if user_query:
            with st.spinner("Searching the universe..."):
                try:
                    response = model.generate_content(user_query)
                    st.markdown("---")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Aura had a tiny glitch: {e}")
