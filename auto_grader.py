from c_executor import run_c_code
from python_executor import run_python_code
from java_executor import run_java_code
from js_executor import run_js_code
from error_mapper import map_error_to_concepts
from mastery_updater import update_mastery

import os
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash-lite"

def get_ai_hint(code, test_case_input, test_case_expected, error_or_got, language="c"):
    if not API_KEY:
        return "Hint generation unavailable because GOOGLE_API_KEY is not set."
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""You are a {language} tutor. The student wrote some code that failed a test case.
Provide a short, 1-2 sentence hint to help them figure out the issue WITHOUT giving away the exact code answer.
Format the hint with simple markdown.

Student Code:
{code}

Test Case Input:
{test_case_input}

Expected Output:
{test_case_expected}

What they got (or error):
{error_or_got}
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Hint generation failed: {str(e)}"

def generate_pro_tip(code, language="c"):
    if not API_KEY:
        return None
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""You are a {language} expert. The student's code passed all test cases!
If the code can be improved (e.g. better time/space complexity, cleaner syntax, more idiomatic), provide a short "Pro Tip" (1-3 sentences).
If the code is already perfect and simple, return exactly the string "PERFECT".

Student Code:
{code}
"""
        response = model.generate_content(prompt)
        tip = response.text.strip()
        if tip == "PERFECT":
            return None
        return tip
    except:
        return None


def grade_code(source_code, test_cases, language="c"):
    results = []
    passed = 0

    for idx, tc in enumerate(test_cases, start=1):
        if language == "python":
            result = run_python_code(source_code, tc.get("input", ""))
        elif language == "java":
            result = run_java_code(source_code, tc.get("input", ""))
        elif language == "javascript":
            result = run_js_code(source_code, tc.get("input", ""))
        else:
            result = run_c_code(source_code, tc.get("input", ""))

        # ❌ Runtime / compile / timeout errors
        if result["status"] != "success":
            concepts = map_error_to_concepts(result, language=language)

            results.append({
                "test": idx,
                "status": result["status"],
                "input": tc.get("input", ""),
                "expected": tc.get("expected", ""),
                "error": result.get("error", result.get("stderr")),
                "weak_concepts": concepts,
                "plain_explanation": result.get("_plain_explanation", "")
            })

            if concepts:
                update_mastery(concepts, success=False)

            continue

        # ✅ Program ran — check output
        output = result["output"].strip()
        expected = tc["expected"].strip()

        if output == expected:
            passed += 1
            results.append({
                "test": idx,
                "status": "passed"
            })
        else:
            concepts = map_error_to_concepts(
                {"status": "wrong_answer"}, language=language
            )

            results.append({
                "test": idx,
                "status": "failed",
                "input": tc.get("input", ""),
                "expected": expected,
                "got": output,
                "weak_concepts": concepts,
                "plain_explanation": result.get("_plain_explanation", "")
            })

            update_mastery(concepts, success=False)

    # Reinforce logic if ALL tests passed
    pro_tip = None
    if passed == len(test_cases) and passed > 0:
        update_mastery(["logic"], success=True)
        pro_tip = generate_pro_tip(source_code, language=language)

    score = passed / len(test_cases) if test_cases else 0.0

    return {
        "passed": passed,
        "total": len(test_cases),
        "score": round(score, 2),
        "details": results,
        "pro_tip": pro_tip
    }
