import streamlit as st
import google.generativeai as genai

# 1. Page Config & Layout
st.set_page_config(page_title="Aura AI", page_icon="✨", layout="centered")
st.title("Aura AI ✨")

# 2. THE FINAL 404 FIX
if "GOOGLE_API_KEY" in st.secrets:
    try:
        # This line forces the connection to the Official Stable Server
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
        
        # We use 'gemini-pro' because it is the most stable name across all versions
        model = genai.GenerativeModel('gemini-pro')
        st.caption("🟢 Aura System: Stable Connection Established")
    except Exception as e:
        st.error(f"Connection failed: {e}")
else:
    st.error("Missing GOOGLE_API_KEY in Streamlit Secrets!")
    st.stop()

# 3. Chat System
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input Bar
if prompt := st.chat_input("Ask Aura..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Generate content using the stable path
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # This will catch if the API key itself has an issue
            st.error(f"Aura glitch: {e}")

# 5. Sidebar
with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
