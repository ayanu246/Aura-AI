import streamlit as st
from openai import OpenAI

# 1. Page Styling
st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

# 2. Connect to the Free Brain via OpenRouter
if "OPENROUTER_API_KEY" in st.secrets:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
else:
    st.error("Add your OPENROUTER_API_KEY to Streamlit Secrets!")
    st.stop()

# 3. Aura's Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chatting Logic
if prompt := st.chat_input("Ask Aura..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Aura's answer
    with st.chat_message("assistant"):
        try:
            # We use Gemma 3 27B Free - It's smart and $0 cost
            response = client.chat.completions.create(
                model="google/gemma-3-27b-it:free",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Aura is resting. Error: {e}")

# 5. Share Aura (Sidebar)
with st.sidebar:
    st.write("### Install Aura")
    st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://aura-ai-official246810.streamlit.app")
    st.caption("Scan to add to your home screen")
