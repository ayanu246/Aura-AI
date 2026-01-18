import streamlit as st
from openai import OpenAI

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Aura AI", 
    page_icon="⭐", 
    initial_sidebar_state="expanded"
)

# 2. THE "GLOWING ARROW" CSS
st.markdown("""
    <style>
        /* This makes the sidebar toggle button HUGE and Blue */
        [data-testid="stSidebarCollapseIcon"] {
            color: #007BFF !important;
            background-color: #f0f2f6 !important;
            border-radius: 10px !important;
            padding: 5px !important;
            border: 2px solid #007BFF !important;
            width: 45px !important;
            height: 45px !important;
        }
        
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
        }

        #MainMenu, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. SETUP
if "credits" not in st.session_state: st.session_state.credits = 50
if "all_chats" not in st.session_state: st.session_state.all_chats = {}
if "current_chat" not in st.session_state: st.session_state.current_chat = None

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

# 4. SIDEBAR
with st.sidebar:
    st.title("Aura AI")
    st.metric("Credits Left", f"{st.session_state.credits}/50")
    
    if st.button("➕ New Chat", use_container_width=True):
        cid = f"Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[cid] = []
        st.session_state.current_chat = cid
        st.rerun()
    
    st.divider()
    for n in list(st.session_state.all_chats.keys()):
        if st.button(n, key=f"sidebar_{n}", use_container_width=True):
            st.session_state.current_chat = n
            st.rerun()

# 5. MAIN CHAT AREA
if st.session_state.current_chat:
    msgs = st.session_state.all_chats[st.session_state.current_chat]
    for m in msgs:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("Ask Aura..."):
        st.session_state.credits = max(0, st.session_state.credits - 1)
        msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        with st.chat_message("assistant"):
            # FIXED THE BRACKET ON THE LINE BELOW
            r = client.chat.completions.create(model="google/gemma-3-27b-it:free", messages=msgs)
            ans = r.choices[0].message.content
            st.markdown(ans)
            msgs.append({"role": "assistant", "content": ans})
            st.rerun()
else:
    st.info("👈 Tap that Blue Arrow in the corner to start a New Chat!")
