import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Aura AI", page_icon="✨", layout="centered")

# 2. Connect to the Global Brain
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Using 'gemini-1.5-flash' - it's fast and knows everything!
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Wait! I need my API Key. Please add it to Streamlit Secrets.")
    st.stop()

# 3. Simple Welcome Logic
if 'user_name' not in st.session_state:
    st.title("Welcome to Aura AI ✨")
    name = st.text_input("I am ready to answer anything in the world. What is your name?")
    if st.button("Begin My Journey"):
        if name:
            st.session_state.user_name = name
            st.rerun()
else:
    # 4. The Interactive AI Chat
    st.title(f"Aura AI is active. ✨")
    st.write(f"Hello {st.session_state.user_name}, I have the world's knowledge ready for you.")

    # A bigger, better input box
    user_query = st.text_area("Ask me any question in the world:", placeholder="Type here (e.g., Explain space travel, write a poem, or solve a math problem...)")

    if st.button("Ask Aura"):
        if user_query:
            with st.spinner("Searching the universe for your answer..."):
                try:
                    # This sends the question to the real Google AI
                    response = model.generate_content(user_query)
                    st.markdown("---")
                    st.subheader("Aura's Answer:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Aura had a tiny glitch: {e}")
    
    # Sidebar options
    if st.sidebar.button("Reset Chat"):
        del st.session_state.user_name
        st.rerun()
