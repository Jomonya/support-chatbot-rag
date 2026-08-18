# 💬 RAG Customer Support Chatbot

A working retrieval-augmented generation (RAG) chatbot that answers customer
support questions grounded in a real knowledge base — built end-to-end with
a free-tier LLM API, so it costs nothing to run.

**Live demo:** _(add your Streamlit Cloud link here once deployed)_

## What it does

Ask it about shipping, returns, or account/payment policies and it answers
using only the information in `knowledge_base/` — no hallucinated policies,
prices, or timelines. If it doesn't know something, it says so honestly and
flags the question for a human agent instead of guessing.

## How it works

1. **`knowledge_base/`** — plain-text documents (FAQs, policies, etc.)
2. **`rag.py`** — chunks those documents and embeds them locally with
   `sentence-transformers`, storing everything in a persistent Chroma
   vector database (no embedding API cost).
3. **`chatbot.py`** — on each user question, retrieves the most relevant
   chunks and sends them to Gemini along with the question, so every
   answer is grounded in real content rather than the model's own
   assumptions.
4. **`app.py`** — a Streamlit chat interface on top of the whole pipeline.

## Skills demonstrated

- **RAG pipeline design** — chunking strategy, local embeddings, vector
  retrieval, and grounding LLM responses in a custom knowledge base
- **LLM API integration** — Google Gemini API, conversation state/memory
- **Prompt engineering** — a system prompt that constrains the model to
  cited context only, refuses to guess, and defines escalation behavior
  for sensitive requests (anger, fraud, legal issues)
- **Applied Python** — Chroma vector DB, sentence-transformers, clean
  separation of retrieval logic, chat logic, and UI
- **Product thinking** — designed for a real support use case, including
  what happens when the bot doesn't know the answer

## Setup

```bash
# 1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows PowerShell: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get a free API key from https://aistudio.google.com/apikey
#    (sign in with a Google account, click "Create API key" — no card needed)

# 4. Set your API key
export GEMINI_API_KEY="your-key-here"   # Windows PowerShell: $env:GEMINI_API_KEY="your-key-here"

# 5. Build the knowledge base index
python3 rag.py

# 6a. Try it in the terminal
python3 chatbot.py

# 6b. Or launch the web UI
streamlit run app.py
```

## Free tier limits

Gemini's free tier is rate-limited (requests per minute/day) — fine for
demos and testing, not production traffic. Current limits:
https://ai.google.dev/gemini-api/docs/rate-limits

## Possible extensions

- Swap Streamlit for an embeddable chat widget on a real site
- Wire up escalation to actually notify a human (Slack, ticketing system)
- Log conversations to find where the bot struggles and improve the
  knowledge base over time
- Add usage analytics: common questions, escalation rate, resolution rate
