import streamlit as st
from google import genai
import qrcode
from io import BytesIO

# 1. Setup
st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing Key!")
    st.stop()

# 2. Chat Logic
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
        try:
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

# 3. JOTFORM-STYLE DOWNLOAD SECTION
with st.sidebar:
    st.header("Download Aura")
    st.write("Scan this code to install Aura on your phone for free!")
    
    # This creates the link to your specific app
    app_link = "https://aura-ai-official246810.streamlit.app"
    
    # This generates the image
    qr_img = qrcode.make(app_link)
    buf = BytesIO()
    qr_img.save(buf)
    
    # This shows it on the screen
    st.image(buf)
    st.caption("Scan with your phone camera")
