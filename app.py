import streamlit as st
import google.generativeai as genai

# 1. Page Setup
st.set_page_config(page_title="Aura AI", page_icon="✨")
st.title("Aura AI ✨")

# 2. Connection Logic (Fixes the 404 error)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        # We use transport='rest' to ensure it doesn't use the broken v1beta version
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.caption("✅ System Online")
    except Exception as e:
        st.error(f"Connection failed: {e}")
else:
    st.error("Missing API Key! Please add GOOGLE_API_KEY to your Streamlit Secrets.")
    st.stop()

# 3. The User Interface
if 'user_name' not in st.session_state:
    name = st.text_input("I am Aura. What is your name?")
    if st.button("Initialize"):
        if name:
            st.session_state.user_name = name
            st.rerun()
else:
    st.write(f"Welcome back, **{st.session_state.user_name}**!")
    
    query = st.text_area("What would you like to ask me?", placeholder="Type here...")
    
    if st.button("Ask Aura"):
        if query:
            with st.spinner("Thinking..."):
                try:
                    response = model.generate_content(query)
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Aura had a glitch: {e}")
        else:
            st.warning("Please enter a question.")

# 4. Reset Button
if st.sidebar.button("Reset Chat"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
