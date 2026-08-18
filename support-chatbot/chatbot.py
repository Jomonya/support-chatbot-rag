"""
chatbot.py — Core support-chatbot logic.

Combines retrieval (rag.py) with a call to the Gemini API to answer
customer questions grounded in your knowledge base, with conversation
memory. Gemini has a free tier, so this runs at no cost for
low-volume personal/portfolio use.
"""

import os
import google.generativeai as genai
from rag import retrieve

MODEL = "gemini-2.0-flash"  # fast, free-tier friendly model

SYSTEM_PROMPT = """You are a customer support assistant for an online store.

Rules:
- Only answer using the information provided in the CONTEXT section below. Do not invent policies, prices, or timelines that aren't in the context.
- If the context doesn't contain the answer, say so honestly and tell the user you'll flag this for a human agent — do not guess.
- Keep answers short, friendly, and to the point. Use plain language, not corporate jargon.
- If the user seems angry, is asking for a refund exception, or raises anything about fraud, legal issues, or safety, say you're escalating to a human agent rather than trying to resolve it yourself.
"""


class SupportChatbot:
    def __init__(self):
        # Reads GEMINI_API_KEY from the environment.
        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=MODEL, system_instruction=SYSTEM_PROMPT)
        self.chat = self.model.start_chat(history=[])

    def _build_context(self, user_message: str) -> str:
        hits = retrieve(user_message, n_results=3)
        if not hits:
            return "No relevant information found in the knowledge base."
        context_blocks = [f"[Source: {h['source']}]\n{h['text']}" for h in hits]
        return "\n\n---\n\n".join(context_blocks)

    def ask(self, user_message: str) -> str:
        context = self._build_context(user_message)

        prompt_with_context = (
            f"CONTEXT:\n{context}\n\n---\n\nCustomer question: {user_message}"
        )

        response = self.chat.send_message(prompt_with_context)
        return response.text

    def reset(self):
        self.chat = self.model.start_chat(history=[])


if __name__ == "__main__":
    # Quick command-line test loop
    if not os.environ.get("GEMINI_API_KEY"):
        print("Set your GEMINI_API_KEY environment variable first:")
        print('  export GEMINI_API_KEY="your-key-here"')
        raise SystemExit(1)

    bot = SupportChatbot()
    print("Support chatbot ready. Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit"):
            break
        answer = bot.ask(user_input)
        print(f"\nBot: {answer}\n")
