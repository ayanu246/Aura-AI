import streamlit as st

# 1. Page Setup
st.set_page_config(page_title="Aura AI", page_icon="✨")

# 2. Ask for the user's name
if 'user_name' not in st.session_state:
    st.title("Welcome to Aura AI")
    name = st.text_input("Before we begin, what is your name?")
    if st.button("Start Chatting"):
        if name:
            st.session_state.user_name = name
            st.rerun()
else:
    # 3. The Actual AI Chat Interface
    st.title(f"Hello, {st.session_state.user_name}! ✨")
    st.subheader("How can Aura AI help you today?")

    # Create a text box for questions
    user_query = st.text_input("Ask Aura a question:", placeholder="Type here...")

    if user_query:
        # This is where the "AI" response happens
        st.write(f"**Aura AI says:** That is a great question, {st.session_state.user_name}! I am currently being updated to provide even smarter answers. You asked: '{user_query}'")
        
    # Option to sign out/reset name
    if st.sidebar.button("Reset Name"):
        del st.session_state.user_name
        st.rerun()
