# Support Chatbot Starter (Gemini free tier)

A minimal, working RAG (retrieval-augmented generation) customer support
chatbot built on Google's Gemini API, which has a free tier — no billing
required for low-volume personal/portfolio use.

## How it works

1. `knowledge_base/` holds plain-text documents (FAQs, policies, etc.)
2. `rag.py` splits those documents into chunks and stores them in a local
   vector database (Chroma) using free, local embeddings — no API cost.
3. `chatbot.py` takes a user's question, retrieves the most relevant chunks,
   and sends them to Gemini along with the question so the answer is
   grounded in your real content.
4. `app.py` is a simple Streamlit chat UI on top of that.

## Setup

```bash
# 1. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows PowerShell: venv\Scripts\activate

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

## Free tier limits to know

Gemini's free tier is rate-limited (requests per minute/day), which is
fine for testing and demos but not for production traffic. Check current
limits at https://ai.google.dev/gemini-api/docs/rate-limits — if you
outgrow them later, the same code works with a paid Gemini key, or you
can swap back to Claude/OpenAI by changing only `chatbot.py`.

## Customizing it for a real business

- **Replace the sample docs** in `knowledge_base/` with the business's actual
  FAQs, shipping/return policies, product info, etc. Plain `.txt` files work;
  you can extend `rag.py` to also read `.pdf` or `.docx` if needed.
- **Re-run `python3 rag.py`** any time you change the knowledge base — it
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
