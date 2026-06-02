import os
import re
import json
import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from store_trace import store_trace

# --------- CONFIG ----------
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("GOOGLE_API_KEY not set. Copy .env.example to .env and fill it in.")

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash-lite"   # Free tier stable model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DIR = os.path.join(BASE_DIR, "vectordb")

# --------- EMBEDDING MODEL ----------
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# --------- VECTOR DB ----------
_chroma_client = chromadb.PersistentClient(path=VECTOR_DIR)

COLLECTION_NAMES = {
    "c":          "c_tutor",
    "python":     "python_tutor",
    "java":       "java_tutor",
    "javascript": "javascript_tutor",
}

# --------- LANGUAGE PERSONAS ----------
LANGUAGE_PERSONA = {
    "c": {
        "name": "C programming",
        "rules": [
            "If code is required, provide valid C code.",
            "Mention memory management where relevant.",
            "Explain pointers clearly for beginners.",
        ],
    },
    "python": {
        "name": "Python programming",
        "rules": [
            "If code is required, provide valid Python 3 code.",
            "Prefer Pythonic solutions (list comprehensions, built-ins, etc.).",
            "Mention relevant standard library modules where helpful.",
        ],
    },
    "java": {
        "name": "Java programming",
        "rules": [
            "If code is required, provide valid Java code with proper class structure.",
            "Follow OOP principles — classes, encapsulation, inheritance, polymorphism.",
            "Mention relevant Java standard library classes where helpful.",
            "Remind learners to handle checked exceptions when relevant.",
        ],
    },
    "javascript": {
        "name": "JavaScript programming",
        "rules": [
            "If code is required, provide valid modern JavaScript (ES6+).",
            "Prefer const/let over var. Use arrow functions, template literals, destructuring.",
            "Mention browser APIs or Node.js APIs where relevant.",
            "Highlight async/await and Promises when dealing with asynchronous code.",
        ],
    },
}


def _get_collection(language: str):
    name = COLLECTION_NAMES.get(language.lower(), "c_tutor")
    try:
        col = _chroma_client.get_collection(name=name)
        return col if col.count() > 0 else None
    except Exception:
        return None


def retrieve_context(question: str, language: str = "c", k: int = 4) -> str:
    collection = _get_collection(language)
    if collection is None:
        persona_name = LANGUAGE_PERSONA.get(language.lower(), LANGUAGE_PERSONA["c"])["name"]
        return (
            f"No local documentation found for {persona_name}. "
            f"Use your standard {persona_name} knowledge."
        )

    query_embedding = embedder.encode([question]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(k, collection.count()),
        include=["documents", "metadatas"]
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    if not docs:
        return f"No relevant context found. Use standard {language} knowledge."

    context_parts = []
    for doc, meta in zip(docs, metas):
        source = meta.get("source", "unknown") if meta else "unknown"
        context_parts.append(f"[Source: {source}]\n{doc.strip()}")

    return "\n\n---\n\n".join(context_parts)


def build_prompt(context: str, question: str, language: str = "c", history: list = None, mode: str = "tutor") -> str:
    lang = language.lower()
    persona = LANGUAGE_PERSONA.get(lang, LANGUAGE_PERSONA["c"])
    rules_text = "\n".join(f"- {r}" for r in persona["rules"])

    history_text = ""
    if history:
        history_text = "\nPrevious Conversation:\n"
        for msg in history:
            role = "Student" if msg.get("role") == "user" else "Tutor"
            history_text += f"{role}: {msg.get('content', '')}\n"
        history_text += "\n"

    if mode == "socratic":
        teaching_instruction = """IMPORTANT — Socratic Mode is ON:
- Do NOT give the student the direct answer or the complete code solution.
- Instead, guide them with thoughtful questions that help them discover the answer themselves.
- Ask 1-2 probing questions to prompt their thinking.
- If they are close, give a small nudge or hint, not the answer.
- Example: If asked 'what is a pointer?', respond with questions like 'What do you think a memory address represents?' and 'If every variable lives somewhere in memory, how might you refer to that location?'"""
    else:
        teaching_instruction = """- Explain step by step.
- Be beginner friendly.
- Format your response beautifully using rich Markdown (bolding, italics, bullet lists, and syntax-highlighted code blocks) to make it highly readable and premium."""

    return f"""You are a {persona['name']} tutor.

Rules:
{teaching_instruction}
{rules_text}
- Base your answer on the provided context when relevant.
- Do NOT hallucinate.
{history_text}
Context from documentation:
{context}

Student Question:
{question}

Answer the question clearly and thoroughly.

Then output ONLY valid JSON inside <json></json> tags with this schema:
{{
  "concepts": [string],
  "intent": "explain | debug | practice | ask",
  "confidence": number (0.0 to 1.0)
}}
"""


def ask_llm(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.2, "max_output_tokens": 2048}
        )
        return response.text
    except Exception as e:
        print("Gemini error:", e)
        return "Error: Could not reach Gemini API. Please check your GOOGLE_API_KEY."


def extract_json(text: str) -> dict:
    start = text.find("<json>")
    end = text.find("</json>")
    if start == -1 or end == -1:
        raise ValueError("No JSON block found")
    return json.loads(text[start + 6:end].strip())


def ask_tutor(question: str, language: str = "c", history: list = None, mode: str = "tutor") -> str:
    context = retrieve_context(question, language=language)
    prompt = build_prompt(context, question, language=language, history=history, mode=mode)
    output = ask_llm(prompt)

    try:
        concept_trace = extract_json(output)
        store_trace(question, concept_trace)
    except Exception:
        pass

    # Strip internal <json>...</json> block — never show it to the user
    clean_output = re.sub(r"<json>.*?</json>", "", output, flags=re.DOTALL).strip()
    return clean_output


if __name__ == "__main__":
    print(ask_tutor("Explain lists in Python", language="python"))
