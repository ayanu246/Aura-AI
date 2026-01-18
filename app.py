import streamlit as st
import requests
import json

st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Missing API Key in Secrets!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Aura..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # We try the most likely 2026 stable names
        model_names = ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest", "gemini-pro"]
        success = False
        
        for model in model_names:
            if success: break
            
            # STABLE V1 PATH
            url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            try:
                response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
                data = response.json()
                
                if response.status_code == 200:
                    answer = data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    success = True
                else:
                    continue # Try the next model name if this one 404s
            except:
                continue

        if not success:
            st.error("Aura is having trouble reaching the brain. Please check your API Key in Streamlit Secrets.")
