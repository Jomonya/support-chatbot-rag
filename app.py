"""
app.py — Streamlit chat interface for the support bot.

Run with:
    streamlit run app.py
"""

import streamlit as st
from chatbot import SupportChatbot
from rag import build_index, get_collection
import os

st.set_page_config(page_title="Support Chatbot", page_icon="💬")
st.title("💬 Customer Support Chatbot")

if not os.environ.get("GEMINI_API_KEY"):
    st.error("GEMINI_API_KEY is not set. Set it in your environment before running this app.")
    st.stop()

# Build the vector index on first run (e.g. fresh deploy with no chroma_db/ yet).
if "index_ready" not in st.session_state:
    with st.spinner("Setting up knowledge base..."):
        try:
            get_collection()  # raises if the collection doesn't exist yet
        except Exception:
            build_index()
    st.session_state.index_ready = True

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
        "**RAG-powered customer support chatbot**, built to demonstrate "
        "retrieval-augmented generation end-to-end.\n\n"
        "**Stack:** Google Gemini API · ChromaDB (vector search) · "
        "sentence-transformers (local embeddings) · Streamlit\n\n"
        "Answers are grounded strictly in a custom knowledge base — no "
        "hallucinated policies, and it flags anything it doesn't know for "
        "human follow-up.\n\n"
        "[View source on GitHub](https://github.com/Jomonya/support-chatbot-rag)"
    )
    if st.button("Reset conversation"):
        st.session_state.bot.reset()
        st.session_state.messages = []
        st.rerun()
