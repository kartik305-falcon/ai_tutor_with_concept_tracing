"""
image_debugger.py
-----------------
Feature 3: Image-based Error Debugging.
Accepts an image (screenshot of code / compiler error), uses Gemini's
multimodal capability to extract the error, then explains the **concept**
behind it — not just how to fix it.
"""

import os
import base64
import json
import re
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash-lite"


def _image_to_base64(image_path: str) -> tuple[str, str]:
    """Convert image file to base64 string. Returns (base64_data, mime_type)."""
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    mime_type = mime_map.get(ext, "image/jpeg")
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return data, mime_type


def debug_image(image_path: str, language: str = "c") -> dict:
    """
    Analyze an image of code/error and return a structured concept explanation.

    Returns:
        {
            "error_detected": str,     # The error/issue found in the image
            "concept": str,            # The programming concept this relates to
            "why_it_happens": str,     # Root cause explanation
            "how_to_avoid": str,       # Prevention strategy
            "example_fix": str,        # Short corrected code snippet
            "success": bool
        }
    """
    if not API_KEY:
        return {
            "success": False,
            "error_detected": "API key not configured",
            "concept": "", "why_it_happens": "", "how_to_avoid": "", "example_fix": ""
        }

    try:
        img_b64, mime_type = _image_to_base64(image_path)

        model = genai.GenerativeModel(MODEL_NAME)

        prompt = f"""You are an expert {language} programming tutor looking at a student's screenshot.
The screenshot may contain: compiler errors, runtime errors, wrong output, or code with a bug.

Your job is NOT just to fix the code. Your job is to TEACH the student the concept behind the error.

Analyze the image carefully and respond ONLY with a valid JSON object (no markdown, no backticks):
{{
  "error_detected": "One-sentence description of the specific error or issue you see",
  "concept": "The programming concept this error relates to (e.g. 'Null Pointer Dereference', 'Off-by-One Error', 'Stack Overflow', 'Undeclared Variable')",
  "why_it_happens": "2-3 sentences explaining WHY this error occurs at a fundamental level — explain the concept clearly for a beginner",
  "how_to_avoid": "2-3 sentences on how to write code that avoids this class of error in future",
  "example_fix": "A short corrected code snippet (5-10 lines max) that demonstrates the fix. Use actual {language} code."
}}
"""

        response = model.generate_content([
            {
                "role": "user",
                "parts": [
                    {"inline_data": {"mime_type": mime_type, "data": img_b64}},
                    {"text": prompt}
                ]
            }
        ])

        raw = response.text.strip()
        # Strip any markdown fences if present
        raw = re.sub(r"```(?:json)?", "", raw).strip().strip("```").strip()

        result = json.loads(raw)
        result["success"] = True
        return result

    except json.JSONDecodeError:
        # Try to extract JSON from the response
        try:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                result = json.loads(match.group())
                result["success"] = True
                return result
        except Exception:
            pass
        return {
            "success": False,
            "error_detected": "Could not parse AI response",
            "concept": "", "why_it_happens": raw, "how_to_avoid": "", "example_fix": ""
        }
    except Exception as e:
        return {
            "success": False,
            "error_detected": str(e),
            "concept": "", "why_it_happens": "", "how_to_avoid": "", "example_fix": ""
        }
