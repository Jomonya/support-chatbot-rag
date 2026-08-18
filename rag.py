"""
rag.py — Minimal retrieval-augmented generation pipeline.

Loads .txt files from knowledge_base/, splits them into chunks,
embeds them with a local sentence-transformer model, and stores
them in a persistent Chroma vector database. At query time it
retrieves the most relevant chunks for a user's question.

Run this file directly once to (re)build the index:
    python3 rag.py
"""

import os
import glob
import chromadb
from chromadb.utils import embedding_functions

KB_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "support_docs"

EMBED_MODEL = "all-MiniLM-L6-v2"


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 75) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def build_index() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=DB_DIR)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(name=COLLECTION_NAME, embedding_function=embed_fn)

    ids, documents, metadatas = [], [], []
    for filepath in glob.glob(os.path.join(KB_DIR, "*.txt")):
        source = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        for i, chunk in enumerate(chunk_text(text)):
            ids.append(f"{source}-{i}")
            documents.append(chunk)
            metadatas.append({"source": source})

    if documents:
        collection.add(ids=ids, documents=documents, metadatas=metadatas)
        print(f"Indexed {len(documents)} chunks from {len(glob.glob(os.path.join(KB_DIR, '*.txt')))} files.")
    else:
        print("No .txt files found in knowledge_base/ — add some documents first.")

    return collection


def get_collection() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=DB_DIR)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    return client.get_collection(name=COLLECTION_NAME, embedding_function=embed_fn)


def retrieve(query: str, n_results: int = 3) -> list[dict]:
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=n_results)
    hits = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        hits.append({"text": doc, "source": meta["source"]})
    return hits


if __name__ == "__main__":
    build_index()
