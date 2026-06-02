"""
curriculum_planner.py
---------------------
Feature 14: Personalized Learning Path.
Uses the student's mastery data to generate a tailored 7-day study plan.
"""

import os
import re
import json
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash-lite"


def generate_learning_path(mastery_data: dict, language: str = "C") -> list[dict]:
    """
    Generate a personalized 7-day learning path based on mastery data.

    Args:
        mastery_data: { "concept": { "attempts": int, "avg_confidence": float } }
        language: programming language (C, Python, Java, JavaScript)

    Returns:
        List of 7 day objects:
        [
            {
                "day": 1,
                "topic": str,
                "why": str,        # Why this topic was chosen
                "goal": str,       # What the student should be able to do after
                "mini_task": str,  # A small coding exercise
                "tip": str         # Pro tip for learning this topic
            },
            ...
        ]
    """
    if not API_KEY:
        return _fallback_plan(language)

    # Separate weak, medium, and strong concepts
    weak = [(c, d) for c, d in mastery_data.items() if d["avg_confidence"] < 0.5]
    medium = [(c, d) for c, d in mastery_data.items() if 0.5 <= d["avg_confidence"] < 0.8]
    strong = [(c, d) for c, d in mastery_data.items() if d["avg_confidence"] >= 0.8]

    weak_str = ", ".join([c for c, _ in weak[:5]]) if weak else "none identified yet"
    medium_str = ", ".join([c for c, _ in medium[:3]]) if medium else "none"
    strong_str = ", ".join([c for c, _ in strong[:3]]) if strong else "none"

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""You are a {language} programming curriculum designer.
Create a personalized 7-day study plan for a student based on their current knowledge profile.

Student's {language} Knowledge Profile:
- Weak concepts (needs focus): {weak_str}
- Moderate concepts (needs reinforcement): {medium_str}
- Strong concepts (mastered): {strong_str}

Design a progressive 7-day plan that:
1. Starts with fixing the weakest foundational concepts
2. Builds up to moderately difficult topics
3. Ends with an integration challenge that combines multiple concepts
4. Each day is achievable in 1-2 hours of study

Respond ONLY with a valid JSON array (no markdown, no backticks):
[
  {{
    "day": 1,
    "topic": "Topic name (e.g. 'Pointers & Memory Addresses')",
    "why": "One sentence: why this topic is important for their current level",
    "goal": "What the student will be able to do after completing this day",
    "mini_task": "A specific, concrete coding exercise (e.g. 'Write a swap() function using pointers')",
    "tip": "One practical pro tip for learning this topic effectively"
  }}
]

Return exactly 7 day objects.
"""
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.4, "max_output_tokens": 2500}
        )
        raw = response.text.strip()
        raw = re.sub(r"```(?:json)?", "", raw).strip().strip("```").strip()

        try:
            plan = json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\[.*\]", raw, re.DOTALL)
            if match:
                plan = json.loads(match.group())
            else:
                raise ValueError("Could not parse plan JSON")

        # Ensure exactly 7 days with correct day numbers
        for i, day in enumerate(plan[:7], 1):
            day["day"] = i

        return plan[:7]

    except Exception as e:
        print(f"Curriculum planner error: {e}")
        return _fallback_plan(language)


def _fallback_plan(language: str) -> list[dict]:
    """Fallback plan when LLM is unavailable."""
    topics = {
        "C": [
            ("Variables & Data Types", "Write a program that computes BMI from weight and height"),
            ("Control Flow (if/else, switch)", "Build a grade calculator using if/else chains"),
            ("Loops (for, while, do-while)", "Print a multiplication table using nested loops"),
            ("Functions", "Write a function to calculate factorial recursively"),
            ("Arrays & Strings", "Sort an array of 10 integers using bubble sort"),
            ("Pointers", "Write a swap() function using pointer parameters"),
            ("Structs & Memory", "Create a Student struct and read/print 3 student records"),
        ],
        "Python": [
            ("Variables & Types", "Write a temperature converter (Celsius ↔ Fahrenheit)"),
            ("Control Flow", "Build a simple number guessing game"),
            ("Loops & Comprehensions", "Generate a list of prime numbers up to 100"),
            ("Functions", "Write a memoized fibonacci function"),
            ("Lists & Dicts", "Count word frequency in a sentence"),
            ("Classes & OOP", "Build a BankAccount class with deposit/withdraw methods"),
            ("File I/O & Modules", "Read a CSV and print a summary report"),
        ],
        "Java": [
            ("Variables & Types", "Write a unit converter for length"),
            ("Control Flow", "Build a simple calculator with switch"),
            ("Loops & Arrays", "Reverse an array without built-in methods"),
            ("Methods & Scope", "Write a method to check if a number is prime"),
            ("OOP: Classes", "Create an Animal class with subclasses Dog and Cat"),
            ("Collections", "Use ArrayList to store and sort student names"),
            ("Exception Handling", "Build a safe division method that handles exceptions"),
        ],
        "JavaScript": [
            ("Variables & Types", "Write a currency formatter function"),
            ("Control Flow", "Build a FizzBuzz with 3 different conditions"),
            ("Functions & Scope", "Write a closure-based counter"),
            ("Arrays & Methods", "Filter and map an array of products by price"),
            ("Objects & Classes", "Create a Car class with properties and methods"),
            ("Async / Promises", "Fetch data from a public API and display the result"),
            ("DOM Manipulation", "Build a live character counter for a text area"),
        ],
    }

    lang_topics = topics.get(language, topics["C"])
    return [
        {
            "day": i + 1,
            "topic": topic,
            "why": f"Foundational {language} concept every developer must master",
            "goal": f"Understand and apply {topic.split('(')[0].strip()} in real programs",
            "mini_task": task,
            "tip": "Type out the code manually — don't copy-paste. Muscle memory is key!"
        }
        for i, (topic, task) in enumerate(lang_topics)
    ]
