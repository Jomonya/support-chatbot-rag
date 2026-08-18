"""
app.py — Streamlit chat interface for the support bot.

Run with:
    streamlit run app.py
"""

import streamlit as st
from chatbot import SupportChatbot
import os

st.set_page_config(page_title="Support Chatbot", page_icon="💬")
st.title("💬 Customer Support Chatbot")

if not os.environ.get("GEMINI_API_KEY"):
    st.error("GEMINI_API_KEY is not set. Set it in your environment before running this app.")
    st.stop()

if "bot" not in st.session_state:
    st.session_state.bot = SupportChatbot()
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about your order, shipping, returns..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = st.session_state.bot.ask(prompt)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

with st.sidebar:
    st.header("About")
    st.write(
        "This bot answers questions using the documents in `knowledge_base/`. "
        "Edit those files and re-run `python3 rag.py` to update what it knows."
    )
    if st.button("Reset conversation"):
        st.session_state.bot.reset()
        st.session_state.messages = []
        st.rerun()
