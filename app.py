import streamlit as st
import requests
import json

# 1. Page Config
st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

# 2. Secure Connection Setup
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # WE HARD-CODE THE 'V1' STABLE PATH HERE TO STOP THE 404
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
else:
    st.error("Missing API Key in Secrets!")
    st.stop()

# 3. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Aura anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Direct JSON payload to Google's Stable V1 Server
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response_data = response.json()

            if response.status_code == 200:
                answer = response_data['candidates'][0]['content']['parts'][0]['text']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Google Server Error {response.status_code}: {response_data.get('error', {}).get('message', 'Unknown Error')}")
        except Exception as e:
            st.error(f"Aura Connection Glitch: {e}")
