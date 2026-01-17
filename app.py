import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Aura AI", page_icon="✨")

# This looks in your Streamlit Safe (Secrets) for the key
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # This is the standard name for the brain
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("I'm missing my API Key! Add it to the Secrets tab in Streamlit.")
    st.stop()

if 'user_name' not in st.session_state:
    st.title("Welcome to Aura AI ✨")
    name = st.text_input("I can answer anything. What is your name?")
    if st.button("Start"):
        st.session_state.user_name = name
        st.rerun()
else:
    st.title(f"Aura AI is active. ✨")
    query = st.text_area("Ask me any question in the world:")
    if st.button("Ask Aura"):
        with st.spinner("Thinking..."):
            try:
                # We use the standard generation method here
                response = model.generate_content(query)
                st.write("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
