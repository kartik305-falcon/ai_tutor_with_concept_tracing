import os
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(BASE_DIR, "vectordb")

embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=PERSIST_DIR)

# Language → collection name mapping
LANG_COLLECTIONS = {
    "c":      "c_tutor",
    "python": "python_tutor",
    "java":   "java_tutor",
}

def _get_collection(language: str):
    name = LANG_COLLECTIONS.get(language.lower(), "c_tutor")
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )

def ingest_raw_text(text: str, source: str = "uploaded_file", language: str = "c") -> int:
    """Ingest uploaded text into the correct language collection."""
    if not text or not text.strip():
        return 0

    collection = _get_collection(language)
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    embeddings = embedder.encode(chunks).tolist()

    safe_source = source.replace("/", "_").replace("\\", "_")
    ids = [f"{safe_source}_{i}" for i in range(len(chunks))]

    # Skip already-ingested chunks
    try:
        existing = collection.get(ids=ids)
        already_exists = set(existing["ids"])
        new_indices = [i for i, id_ in enumerate(ids) if id_ not in already_exists]
    except Exception:
        new_indices = list(range(len(chunks)))

    if not new_indices:
        return 0

    collection.add(
        documents=[chunks[i] for i in new_indices],
        embeddings=[embeddings[i] for i in new_indices],
        metadatas=[{"source": source, "language": language}] * len(new_indices),
        ids=[ids[i] for i in new_indices]
    )

    return len(new_indices)
