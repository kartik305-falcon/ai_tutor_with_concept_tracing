"""
Run this once to ingest all Python tutorial docs into the python_tutor ChromaDB collection.

Usage:
    python ingest_python_docs.py
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_DOCS_DIR = os.path.join(BASE_DIR, "docs", "python")
PERSIST_DIR = os.path.join(BASE_DIR, "vectordb")

# Load embedding model
print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB setup
client = chromadb.PersistentClient(path=PERSIST_DIR)
collection = client.get_or_create_collection(
    name="python_tutor",
    metadata={"hnsw:space": "cosine"}
)

print(f"Looking for Python docs in: {PYTHON_DOCS_DIR}")

md_files = [f for f in os.listdir(PYTHON_DOCS_DIR) if f.endswith(".md")]
print(f"Found {len(md_files)} markdown files.")

total_chunks = 0

for filename in sorted(md_files):
    filepath = os.path.join(PYTHON_DOCS_DIR, filename)

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        text = f.read().strip()

    if not text:
        print(f"  Skipping empty file: {filename}")
        continue

    # Chunk into 500-char segments
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    embeddings = embedder.encode(chunks).tolist()

    # Use filename as source ID prefix
    source_id = filename.replace(".md", "").replace(" ", "_")

    ids = [f"python_{source_id}_{i}" for i in range(len(chunks))]

    # Skip already-ingested chunks
    existing = collection.get(ids=ids)
    already_exists = set(existing["ids"])
    new_indices = [i for i, id_ in enumerate(ids) if id_ not in already_exists]

    if not new_indices:
        print(f"  Already ingested: {filename}")
        continue

    collection.add(
        documents=[chunks[i] for i in new_indices],
        embeddings=[embeddings[i] for i in new_indices],
        metadatas=[{"source": filename, "language": "python"}] * len(new_indices),
        ids=[ids[i] for i in new_indices]
    )

    total_chunks += len(new_indices)
    print(f"  ✅ Ingested {len(new_indices)} chunks from: {filename}")

print(f"\n🎉 Done! Total new chunks ingested: {total_chunks}")
