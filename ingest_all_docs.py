"""
Run this ONCE after setting up the project to load all documentation
(C, Python, Java) into the vector database.

Usage:
    cd newai
    python ingest_all_docs.py

You only need to re-run this if you add new docs.
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(BASE_DIR, "vectordb")

LANGUAGE_DOCS = {
    "c":      os.path.join(BASE_DIR, "docs"),          # C docs live directly in docs/
    "python": os.path.join(BASE_DIR, "docs", "python"),
    "java":   os.path.join(BASE_DIR, "docs", "java"),
}

COLLECTION_NAMES = {
    "c":      "c_tutor",
    "python": "python_tutor",
    "java":   "java_tutor",
}

print("Loading embedding model (all-MiniLM-L6-v2)...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=PERSIST_DIR)
print(f"Vector DB: {PERSIST_DIR}\n")

grand_total = 0

for language, docs_dir in LANGUAGE_DOCS.items():
    print(f"{'='*50}")
    print(f"  Language: {language.upper()}")
    print(f"  Docs dir: {docs_dir}")

    if not os.path.exists(docs_dir):
        print(f"  ⚠️  Directory not found, skipping.\n")
        continue

    # For C, only pick up .md files directly in docs/ (not subfolders)
    if language == "c":
        md_files = [
            f for f in os.listdir(docs_dir)
            if f.endswith(".md") and os.path.isfile(os.path.join(docs_dir, f))
        ]
    else:
        md_files = [f for f in os.listdir(docs_dir) if f.endswith(".md")]

    print(f"  Found {len(md_files)} markdown files.")

    if not md_files:
        print(f"  ⚠️  No .md files found, skipping.\n")
        continue

    collection = client.get_or_create_collection(
        name=COLLECTION_NAMES[language],
        metadata={"hnsw:space": "cosine"}
    )

    lang_total = 0

    for filename in sorted(md_files):
        filepath = os.path.join(docs_dir, filename)

        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            text = f.read().strip()

        if not text:
            print(f"  ⚠️  Skipping empty: {filename}")
            continue

        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        embeddings = embedder.encode(chunks).tolist()

        source_id = filename.replace(".md", "").replace(" ", "_")
        ids = [f"{language}_{source_id}_{i}" for i in range(len(chunks))]

        # Avoid re-ingesting
        try:
            existing = collection.get(ids=ids)
            already = set(existing["ids"])
            new_idx = [i for i, id_ in enumerate(ids) if id_ not in already]
        except Exception:
            new_idx = list(range(len(chunks)))

        if not new_idx:
            print(f"  ✓  Already ingested: {filename}")
            continue

        collection.add(
            documents=[chunks[i] for i in new_idx],
            embeddings=[embeddings[i] for i in new_idx],
            metadatas=[{"source": filename, "language": language}] * len(new_idx),
            ids=[ids[i] for i in new_idx]
        )

        lang_total += len(new_idx)
        print(f"  ✅ {filename}  ({len(new_idx)} chunks)")

    print(f"\n  {language.upper()} total new chunks: {lang_total}")
    grand_total += lang_total

print(f"\n{'='*50}")
print(f"🎉 All done! Grand total new chunks ingested: {grand_total}")
print(f"\nYou can now start the app:")
print(f"    streamlit run app.py")
