import streamlit as st

st.title("Aura AI Platform")
st.write("Welcome to the official Aura AI. Sign in to begin.")

name = st.text_input("What is your name?")
if name:
    st.write(f"Hello {name}, how can Aura help you today?")