import os
import json
import chromadb
import google.generativeai as genai
from store_trace import store_trace

# --------- CONFIG ----------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "models/gemini-flash-latest"

# --------- VECTOR DB (DISABLED QUERY MODE) ----------
client = chromadb.PersistentClient(path="vectordb")

collection = client.get_or_create_collection(
    name="c_tutor",
    embedding_function=None
)

# --------- SAFE CONTEXT RETRIEVAL ----------
def retrieve_context(question, k=4):
    return "Use standard C programming knowledge."


# --------- PROMPT ----------
def build_prompt(context, question):
    return f"""
You are a C programming tutor.

Rules:
- Explain step by step.
- Be beginner friendly.
- If code is required, provide valid C code.
- Do NOT hallucinate.

Context:
{context}

Question:
{question}

Answer the question first.

Then output ONLY valid JSON inside <json></json> tags with this schema:
{{
  "concepts": [string],
  "intent": "explain | debug | practice | ask",
  "confidence": number (0.0 to 1.0)
}}
"""

# --------- CALL MODEL ----------
def ask_llm(prompt: str) -> str:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.2}
    )
    return response.text

# --------- PARSE JSON ----------
def extract_json(text):
    start = text.find("<json>")
    end = text.find("</json>")
    if start == -1 or end == -1:
        raise ValueError("No JSON block found")
    json_str = text[start + 6:end]
    return json.loads(json_str.strip())

# --------- UI-SAFE ENTRY POINT ----------
def ask_tutor(question: str) -> str:
    context = retrieve_context(question)
    prompt = build_prompt(context, question)

    output = ask_llm(prompt)

    try:
        concept_trace = extract_json(output)
        store_trace(question, concept_trace)
    except Exception:
        pass

    return output

# --------- CLI TEST ----------
if __name__ == "__main__":
    print(ask_tutor("Explain pointers in C"))
