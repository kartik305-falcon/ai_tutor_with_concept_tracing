import chromadb
import textwrap

# ---- Load Vector DB ----
client = chromadb.PersistentClient(path="vectordb")
collection = client.get_collection("c_tutor")


def retrieve_context(question, k=4):
    res = collection.query(
        query_texts=[question],
        n_results=k
    )
    return "\n\n".join(res["documents"][0])


def build_prompt(context, question):
    return f"""
You are a C programming tutor.

Use ONLY the context below to answer.
Explain step by step.
If code is required, give valid C code.

Context:
{context}

Question:
{question}

Answer:
"""


# ---- Test ----
if __name__ == "__main__":
    q = "Explain pointers in C"
    ctx = retrieve_context(q)

    prompt = build_prompt(ctx, q)

    print("======= PROMPT SENT TO MODEL =======\n")
    print(textwrap.shorten(prompt, width=1200))
