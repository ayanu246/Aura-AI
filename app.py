import streamlit as st
import google.generativeai as genai

st.title("Aura AI ✨")

# Connect to Google using the Secret Key
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # This specific line helps bypass the 404 error
    model = genai.GenerativeModel('gemini-pro') 
else:
    st.error("I can't find your API key in the Secrets box!")
    st.stop()

# The Chat Box
user_query = st.text_input("Ask me anything:")

if st.button("Send"):
    if user_query:
        try:
            # Get the answer from the brain
            response = model.generate_content(user_query)
            st.info(response.text)
        except Exception as e:
            # This will show us the EXACT error if it fails
            st.error(f"Error details: {e}")
