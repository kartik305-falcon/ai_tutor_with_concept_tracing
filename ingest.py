import os
import chromadb
from sentence_transformers import SentenceTransformer

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(BASE_DIR, "vectordb")

print("CWD =", os.getcwd())
print("Persist dir =", PERSIST_DIR)

# -------------------------
# Load embedding model (LOCAL)
# -------------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------
# ChromaDB setup
# -------------------------
client = chromadb.PersistentClient(path=PERSIST_DIR)

collection = client.get_or_create_collection(
    name="c_tutor",
    metadata={"hnsw:space": "cosine"}
)

# -------------------------
# Ingest uploaded text
# -------------------------
def ingest_raw_text(text, source="uploaded_file"):
    if not text or not text.strip():
        return 0

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    embeddings = embedder.encode(chunks).tolist()

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"source": source}] * len(chunks),
        ids=[f"{source}_{i}" for i in range(len(chunks))]
    )

    return len(chunks)
