#!/usr/bin/env python3
"""
Inspect ChromaDB (SQLite) used for RAG.
- Opens the DB in read-only mode to avoid locks
- Introspects actual schema (works across Chroma versions)

Run:
  py query_chroma_sqlite.py
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, List

ROOT = Path(__file__).resolve().parent
DB_DIR = ROOT / "data" / "chroma_db"

# Common filenames Chroma uses
CANDIDATES = [
    DB_DIR / "chroma.sqlite3",
    DB_DIR / "chroma.db",
]

def find_db() -> Path | None:
    for p in CANDIDATES:
        if p.exists():
            return p
    # fallback: search
    for p in DB_DIR.glob("*.sqlite*"):
        return p
    return None

DB_PATH = find_db()
if not DB_PATH:
    raise SystemExit(f"Chroma SQLite DB not found in: {DB_DIR}")

print(f"Using DB: {DB_PATH}")

conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Utilities

def list_tables() -> List[str]:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    return [r[0] for r in cur.fetchall()]

def table_cols(name: str) -> List[str]:
    cur.execute(f"PRAGMA table_info({name})")
    return [r[1] for r in cur.fetchall()]

def first_col(cols: List[str], candidates: List[str]) -> str | None:
    for c in candidates:
        if c in cols:
            return c
    return None

# 1) List tables
print("\n=== tables ===")
for t in list_tables():
    print(t)

# 2) collections
if "collections" in list_tables():
    cols = table_cols("collections")
    print("\n=== collections (columns) ===\n", cols)
    sel = [c for c in ["id", "name", "metadata", "created_at", "dimension"] if c in cols]
    sql = "SELECT " + ", ".join(sel) + " FROM collections LIMIT 10" if sel else "SELECT * FROM collections LIMIT 10"
    cur.execute(sql)
    rows = cur.fetchall()
    for r in rows:
        d = {k: r[k] for k in r.keys()}
        for k, v in list(d.items()):
            if isinstance(v, str) and len(v) > 200:
                d[k] = v[:200] + "…"
        print(d)
else:
    print("\n(no collections table)")

# 3) collection_metadata (if present)
if "collection_metadata" in list_tables():
    print("\n=== collection_metadata (sample) ===")
    cur.execute("SELECT * FROM collection_metadata LIMIT 10")
    for r in cur.fetchall():
        print(dict(r))

# 4) embeddings summary
if "embeddings" in list_tables():
    ecols = table_cols("embeddings")
    print("\n=== embeddings (columns) ===\n", ecols)
    cur.execute("SELECT COUNT(*) AS n FROM embeddings")
    print("embeddings total:", cur.fetchone()[0])

    # Count by collection if we can find the column name
    coll_col = first_col(ecols, ["collection_id", "collection_uuid", "collection", "collectionId"])
    if coll_col:
        cur.execute(f"SELECT {coll_col} AS collection, COUNT(*) AS n FROM embeddings GROUP BY {coll_col} ORDER BY n DESC")
        for r in cur.fetchall():
            print(dict(r))

    # Show sample docs if present
    doc_col = first_col(ecols, ["document", "doc", "text"]) or None
    id_col = first_col(ecols, ["id", "embedding_id"]) or "id"
    sel_cols = ", ".join([c for c in [id_col, doc_col] if c])
    try:
        if sel_cols:
            cur.execute(f"SELECT {sel_cols} FROM embeddings LIMIT 3")
            for r in cur.fetchall():
                d = dict(r)
                if doc_col and isinstance(d.get(doc_col), str) and len(d[doc_col]) > 160:
                    d[doc_col] = d[doc_col][:160] + "…"
                print(d)
    except sqlite3.Error:
        pass

# 5) embedding_fulltext_search sample
if "embedding_fulltext_search" in list_tables():
    fcols = table_cols("embedding_fulltext_search")
    print("\n=== embedding_fulltext_search (columns) ===\n", fcols)
    doc_col = first_col(fcols, ["document", "text", "content"]) or fcols[0]
    cur.execute(f"SELECT {doc_col} FROM embedding_fulltext_search LIMIT 5")
    for r in cur.fetchall():
        v = r[0]
        if isinstance(v, str) and len(v) > 160:
            v = v[:160] + "…"
        print({doc_col: v})

conn.close()
print("\nDone.")
