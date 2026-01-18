import streamlit as st
from google import genai
import qrcode
from io import BytesIO

# 1. PAGE SETUP (Aura's Face)
st.set_page_config(page_title="Aura AI", page_icon="✨", layout="centered")
st.title("Aura AI ✨")

# 2. CONNECTION (The API Key)
if "GOOGLE_API_KEY" in st.secrets:
    # Uses the brand new 2026 Client you found!
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# 3. MEMORY (Remembering the chat)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. CHAT LOGIC (Aura's Brain)
if prompt := st.chat_input("Ask Aura..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We use 'gemini-1.5-flash' because it has a real free limit in 2026
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            
            # Show the answer
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            # If Google blocks you, this tells us exactly why
            st.error(f"Aura is currently over capacity. Please wait 60 seconds. Error: {e}")

# 5. SHARE SECTION (Jotform style QR Code)
with st.sidebar:
    st.header("Install Aura")
    st.write("Scan to put Aura on your phone home screen!")
    
    # Your specific app link
    url = "https://aura-ai-official246810.streamlit.app"
    
    # Make the QR code
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf)
    
    st.image(buf)
    st.caption("Open your camera to scan")
