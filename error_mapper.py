"""
error_mapper.py  (updated)
--------------------------
Maps execution errors to programming concepts.
Adds JavaScript support + an LLM-powered plain-English explanation fallback.
"""

import os
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash-lite"


def _llm_explain_error(error_text: str, language: str) -> str:
    """Use Gemini to produce a 1-sentence beginner-friendly error explanation."""
    if not API_KEY or not error_text:
        return ""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = (
            f"You are a {language} tutor. A student got this error:\n\n"
            f"{error_text[:500]}\n\n"
            "In ONE plain English sentence, explain what this error means for a beginner student. "
            "Do NOT give the fix — just explain what went wrong in simple terms."
        )
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.2, "max_output_tokens": 150}
        )
        return response.text.strip()
    except Exception:
        return ""


def map_error_to_concepts(exec_result: dict, language: str = "c") -> list:
    status = exec_result["status"]
    error_text = exec_result.get("error", exec_result.get("stderr", ""))

    concepts = _map_concepts(exec_result, language)

    # Attach a plain explanation for non-passing statuses
    if status not in ("success", "passed") and error_text:
        plain = _llm_explain_error(error_text, language)
        exec_result["_plain_explanation"] = plain

    return concepts


def _map_concepts(exec_result: dict, language: str) -> list:
    status = exec_result["status"]
    error_text = exec_result.get("error", exec_result.get("stderr", ""))

    if language == "python":
        if status == "runtime_error":
            if "SyntaxError" in error_text:    return ["syntax", "indentation"]
            if "NameError" in error_text:      return ["variables", "scope"]
            if "TypeError" in error_text:      return ["data types", "functions"]
            if "IndexError" in error_text or "KeyError" in error_text: return ["lists", "dictionaries"]
            if "ImportError" in error_text or "ModuleNotFoundError" in error_text: return ["modules", "imports"]
            if "ZeroDivisionError" in error_text: return ["arithmetic", "operators"]
            if "AttributeError" in error_text: return ["classes", "objects"]
            if "RecursionError" in error_text: return ["recursion", "base case"]
            return ["exceptions", "runtime"]
        if status == "timeout":      return ["loops", "recursion"]
        if status == "wrong_answer": return ["logic", "output formatting"]
        return []

    if language == "java":
        if status == "compile_error":
            if "cannot find symbol" in error_text:    return ["variables", "scope", "imports"]
            if "incompatible types" in error_text:    return ["data types", "type casting"]
            if "missing return" in error_text:        return ["methods", "return statements"]
            if "reached end of file" in error_text or "';' expected" in error_text: return ["syntax", "braces"]
            if "class" in error_text and "public" in error_text: return ["class naming", "file structure"]
            return ["syntax", "declarations"]
        if status == "runtime_error":
            if "NullPointerException" in error_text:               return ["null checks", "object initialization"]
            if "ArrayIndexOutOfBoundsException" in error_text:     return ["arrays", "index bounds"]
            if "ClassCastException" in error_text:                 return ["type casting", "polymorphism"]
            if "StackOverflowError" in error_text:                 return ["recursion", "base case"]
            if "NumberFormatException" in error_text:              return ["type conversion", "input parsing"]
            if "ArithmeticException" in error_text:                return ["arithmetic", "division by zero"]
            return ["exceptions", "runtime"]
        if status == "timeout":      return ["loops", "recursion", "algorithm efficiency"]
        if status == "wrong_answer": return ["logic", "output formatting", "operators"]
        return []

    if language == "javascript":
        if status in ("error", "compile_error", "runtime_error"):
            if "ReferenceError" in error_text:  return ["variables", "scope", "hoisting"]
            if "TypeError" in error_text:       return ["data types", "undefined", "functions"]
            if "SyntaxError" in error_text:     return ["syntax", "brackets"]
            if "RangeError" in error_text:      return ["recursion", "array bounds"]
            if "undefined" in error_text:       return ["variables", "initialization"]
            return ["runtime", "exceptions"]
        if status == "timeout":      return ["loops", "recursion", "async"]
        if status == "wrong_answer": return ["logic", "output formatting"]
        return []

    # Default: C
    if status == "compile_error": return ["syntax", "declarations"]
    if status == "timeout":       return ["loops", "conditions"]
    if status == "runtime_error": return ["pointers", "memory"]
    if status == "wrong_answer":  return ["logic", "operators"]
    return []
