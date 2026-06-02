import os
import re
import json
import google.generativeai as genai
from concept_analytics import compute_mastery

# --------- CONFIG ----------
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("GOOGLE_API_KEY not set. Copy .env.example to .env and fill it in.")

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash-lite"   # Free tier stable model


def generate_adaptive_quiz(language="C", num_questions=5):

    model = genai.GenerativeModel(MODEL_NAME)

    mastery = compute_mastery()
    
    # Calculate overall mastery score
    total_confidence = sum(data.get("avg_confidence", 0) for data in mastery.values())
    avg_mastery_score = total_confidence / len(mastery) if mastery else 0.0

    # Determine quiz difficulty
    difficulty_context = "difficulty level: beginner-friendly, foundational concepts."
    if avg_mastery_score > 0.8:
        difficulty_context = "difficulty level: expert. Include tricky edge-cases, advanced optimization queries, and complex scenarios."
    elif avg_mastery_score > 0.5:
        difficulty_context = "difficulty level: intermediate. Include moderately challenging questions that test deep understanding."

    weak_concepts = [
        concept for concept, data in mastery.items()
        if data.get("avg_confidence", 1) < 0.6
    ]

    if not weak_concepts:
        weak_concepts = ["variables", "loops", "conditions"]

    # Strict schema in prompt prevents malformed JSON
    prompt = f"""Generate {num_questions} multiple choice quiz questions for {language} programming.

Focus on these weak concepts: {', '.join(weak_concepts)}
Constraint: {difficulty_context}

Return ONLY valid JSON — no markdown, no extra text, no backticks.
Use this exact format:
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A"
  }}
]

The "answer" value MUST exactly match one of the strings in "options".
"""

    quiz = []
    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.4, "max_output_tokens": 1500}
        )
        text = response.text.strip()

        # Strip markdown code fences if model adds them
        text = re.sub(r"```(?:json)?", "", text).strip()

        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            quiz = json.loads(match.group())

    except Exception as e:
        print("Quiz generation error:", e)

    # Fallback quiz if generation fails
    if not quiz:
        quiz = [
            {
                "question": f"What is a variable in {language}?",
                "options": ["A storage location in memory", "A loop construct", "A function call", "A pointer"],
                "answer": "A storage location in memory"
            },
            {
                "question": f"Which of the following is a loop in {language}?",
                "options": ["if/else", "for", "switch", "return"],
                "answer": "for"
            }
        ]

    return quiz, weak_concepts

def generate_practice_scenario(language="C"):
    model = genai.GenerativeModel(MODEL_NAME)
    mastery = compute_mastery()
    
    total_confidence = sum(data.get("avg_confidence", 0) for data in mastery.values())
    avg_mastery_score = total_confidence / len(mastery) if mastery else 0.0

    difficulty = "beginner"
    if avg_mastery_score > 0.8:
        difficulty = "expert"
    elif avg_mastery_score > 0.5:
        difficulty = "intermediate"

    weak_concepts = [
        concept for concept, data in mastery.items()
        if data.get("avg_confidence", 1) < 0.6
    ]

    focus = "variables and loops"
    if weak_concepts:
        focus = ", ".join(weak_concepts[:3])

    prompt = f"""Generate a {difficulty}-level coding practice problem for {language} programming.
The problem should focus on reinforcing these concepts: {focus}.

Return ONLY valid JSON — no extra markdown. Use this schema:
{{
  "description": "A short, engaging problem description and instructions.",
  "default_code": "The starting code template for the student.",
  "test_cases": "Input => Expected Output\\nInput => Expected Output"
}}

The test_cases string MUST be formatted exactly like this example (lines separated by exactly `\\n`, and input/output separated by ` => `):
"3 4 => 7\\n10 20 => 30"
"""
    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.5, "max_output_tokens": 1500}
        )
        text = response.text.strip()
        text = re.sub(r"```(?:json)?", "", text).strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print("Scenario generation error:", e)

    return None
