# Support Chatbot Starter

A minimal, working RAG (retrieval-augmented generation) customer support
chatbot built on the Claude API. It answers questions grounded in a set
of your own documents so it doesn't make things up.

## How it works

1. `knowledge_base/` holds plain-text documents (FAQs, policies, etc.)
2. `rag.py` splits those documents into chunks and stores them in a local
   vector database (Chroma) using free, local embeddings — no API cost.
3. `chatbot.py` takes a user's question, retrieves the most relevant chunks,
   and sends them to Claude along with the question so the answer is
   grounded in your real content.
4. `app.py` is a simple Streamlit chat UI on top of that.

## Setup

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export ANTHROPIC_API_KEY="your-key-here"   # Windows: set ANTHROPIC_API_KEY=your-key-here

# 4. Build the knowledge base index
python rag.py

# 5a. Try it in the terminal
python chatbot.py

# 5b. Or launch the web UI
streamlit run app.py
```

## Customizing it for a real business

- **Replace the sample docs** in `knowledge_base/` with the business's actual
  FAQs, shipping/return policies, product info, etc. Plain `.txt` files work;
  you can extend `rag.py` to also read `.pdf` or `.docx` if needed.
- **Re-run `python rag.py`** any time you change the knowledge base — it
  rebuilds the index from scratch.
- **Edit the `SYSTEM_PROMPT`** in `chatbot.py` to match the business's tone
  and to define what the bot should and shouldn't handle on its own.
- **Escalation**: right now the bot just says it's escalating in its reply.
  In production you'd wire that up to actually notify a human (e.g., send
  a Slack message, create a support ticket, or flag the conversation in
  your CRM) whenever certain phrases appear in its response.

## Where to go from here

- Swap Streamlit for a proper embeddable chat widget (e.g., a small
  React/HTML widget that calls a FastAPI backend wrapping `chatbot.py`).
- Add authentication so each user's conversation history is private.
- Log every conversation so you can review where the bot struggles and
  improve the knowledge base over time.
- Add analytics: track common questions, escalation rate, resolution rate.
- Consider chunking by section/heading instead of fixed word counts once
  your documents get longer or more structured.
