#!/usr/bin/env python3
"""
Inspect RAG embeddings and index state.

Run:
  py inspect_rag.py

Shows:
- ChromaDB collections, count, embedding dimension, sample vector slice
- Falls back to TF-IDF details if Chroma or embeddings are unavailable
"""
from __future__ import annotations

import textwrap
from pathlib import Path


def inspect_chroma() -> bool:
    try:
        import chromadb  # type: ignore
    except Exception as e:
        print("chromadb not available:", e)
        return False

    root = Path(__file__).resolve().parent
    db_path = root / "data" / "chroma_db"
    if not db_path.exists():
        print(f"Chroma path not found: {db_path}")
        return False

    client = chromadb.PersistentClient(path=str(db_path))
    cols = client.list_collections()
    names = [c.name for c in cols]
    print("Collections:", names)

    name = "swasthvedha_knowledge"
    if name not in names:
        print(f"Collection '{name}' not found in {names}")
        return False

    col = client.get_collection(name)
    try:
        count = col.count()
    except Exception:
        count = None
    print("Count:", count)

    try:
        peek = col.peek()  # small sample
        ids = peek.get("ids", [])[:3]
        if not ids:
            print("No documents to peek.")
            return count is not None and count > 0
        res = col.get(ids=ids, include=["embeddings", "documents", "metadatas"])  # type: ignore
        embs = res.get("embeddings", [])
        docs = res.get("documents", [])
        metas = res.get("metadatas", [])
        if embs:
            dim = len(embs[0])
            print("Embedding dim:", dim)
            print("first_vec[:8]:", [round(float(x), 4) for x in embs[0][:8]])
        for i in range(min(3, len(docs))):
            snippet = textwrap.shorten(docs[i], width=160, placeholder="…")
            print(f"Doc[{i}]:", snippet)
            print(f"Meta[{i}]:", metas[i])
        return True
    except Exception as e:
        print("Failed to fetch embeddings:", e)
        return False


def inspect_tfidf():
    try:
        from services.rag_service import get_rag_service  # local import
    except Exception as e:
        print("Cannot import RAG service:", e)
        return False

    rag = get_rag_service()
    print("Initialized:", rag.get_system_info())

    if rag.tfidf_vectorizer is None or rag.tfidf_matrix is None:
        print("TF-IDF not initialized.")
        return False

    vec = rag.tfidf_vectorizer
    try:
        feats = vec.get_feature_names_out()
        print("TF-IDF features:", len(feats))
        print("Top 20 tokens:", feats[:20])
    except Exception:
        print("Could not list feature names.")

    print("Total chunks:", len(rag.knowledge_chunks))
    if rag.knowledge_chunks:
        print("Sample chunk:", textwrap.shorten(rag.knowledge_chunks[0], width=160, placeholder="…"))
        print("Sample meta:", rag.chunk_metadata[0] if rag.chunk_metadata else None)
    return True


if __name__ == "__main__":
    print("--- Inspecting ChromaDB embeddings ---")
    ok = inspect_chroma()
    if not ok:
        print("\n--- Falling back to TF-IDF inspection ---")
        inspect_tfidf()
