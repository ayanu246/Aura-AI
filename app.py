import streamlit as st
from google import genai

st.set_page_config(page_title="Aura AI")
st.title("Aura AI ✨")

# NEW 2026 CONNECTION METHOD
if "GOOGLE_API_KEY" in st.secrets:
    # We create a 'Client' now, which is much more stable
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing Key in Secrets!")
    st.stop()

# Simple UI
user_query = st.text_input("Ask Aura anything:")

if st.button("Send"):
    if user_query:
        with st.spinner("Aura is thinking..."):
            try:
                # The new way to generate content
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=user_query
                )
                st.write("---")
                st.success(response.text)
            except Exception as e:
                st.error(f"Aura had a glitch: {e}")
    else:
        st.warning("Please type something first!")
