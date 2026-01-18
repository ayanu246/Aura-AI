import streamlit as st
from google import genai

# 1. Page Config
st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

# 2. Setup the NEW 2026 Client
if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key!")
    st.stop()

# 3. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. THE 2026 MODEL FIX
if prompt := st.chat_input("Ask Aura..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We switch to the 'gemini-3-flash-preview' model 
            # This is the 3.0 model that usually has a FRESH quota.
            response = client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # If 3.0 is busy, we try the most stable backup
            try:
                response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Aura's 2026 brain is currently locked. Please check if you have 'Gemini 3' enabled in AI Studio.")
