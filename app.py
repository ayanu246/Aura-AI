import streamlit as st
import google.generativeai as genai

st.title("Aura AI ✨")

# Simple Setup
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Key is missing in Secrets!")

# Input
prompt = st.text_input("Say something to Aura:")
if st.button("Send"):
    try:
        response = model.generate_content(prompt)
        st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
