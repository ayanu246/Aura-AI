import streamlit as st
from google import genai # Note the new way to import

st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

# 1. The 2026 Client Setup
if "GOOGLE_API_KEY" in st.secrets:
    # This matches the code you saw on the Google homepage!
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing Key in Secrets!")
    st.stop()

# 2. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. The "Gemini 3" Brain
if prompt := st.chat_input("Ask Aura..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We use 'gemini-3-flash-preview' or 'gemini-2.5-flash'
            # Based on your dashboard, these are the active 2026 brains
            response = client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Fallback for 2025/2026 transition
            try:
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error(f"Aura is updating to the 2026 server: {e}")
