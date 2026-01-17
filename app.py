import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Aura AI")
st.title("Aura AI ✨")

# THE STABLE CONNECTION FIX
if "GOOGLE_API_KEY" in st.secrets:
    # We use 'rest' transport to bypass the v1beta bug
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
    # Use the stable model name
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("I can't find your API key in Secrets!")
    st.stop()

query = st.text_input("Ask Aura anything:")
if st.button("Send"):
    if query:
        try:
            # Simple direct call
            response = model.generate_content(query)
            st.success(response.text)
        except Exception as e:
            # If it still fails, this will show us the NEW error
            st.error(f"Aura had a glitch: {e}")
