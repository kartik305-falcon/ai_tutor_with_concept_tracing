"""
github_fetcher.py
-----------------
Feature 9: GitHub Code Reviewer (Local).
Fetches a public GitHub file and generates an AI code review using Gemini.
No GitHub API token needed for public repos.
"""

import os
import re
import json
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash-lite"


def _github_to_raw_url(url: str) -> str:
    """
    Convert a GitHub blob URL to a raw content URL.
    e.g. https://github.com/user/repo/blob/main/file.c
      -> https://raw.githubusercontent.com/user/repo/main/file.c
    """
    url = url.strip()

    # Already a raw URL
    if "raw.githubusercontent.com" in url:
        return url

    # Standard GitHub blob URL
    # https://github.com/{user}/{repo}/blob/{branch}/{path}
    match = re.match(
        r"https?://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.*)",
        url
    )
    if match:
        user, repo, branch, path = match.groups()
        return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"

    raise ValueError(
        "Invalid GitHub URL. Please use a full file URL like:\n"
        "https://github.com/username/repo/blob/main/file.py"
    )


def fetch_github_code(url: str) -> tuple[str, str]:
    """
    Fetch code from a public GitHub file URL.
    Returns (filename, code_text).
    Raises ValueError on bad URL, RuntimeError on fetch failure.
    """
    try:
        import httpx
    except ImportError:
        raise RuntimeError("httpx is not installed. Run: pip install httpx")

    raw_url = _github_to_raw_url(url)
    filename = raw_url.split("/")[-1]

    try:
        response = httpx.get(raw_url, timeout=15, follow_redirects=True)
        response.raise_for_status()
        return filename, response.text
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ValueError("File not found. Is this a public repository and correct file path?")
        raise RuntimeError(f"HTTP error {e.response.status_code}: {e.response.text[:200]}")
    except httpx.RequestError as e:
        raise RuntimeError(f"Network error: {e}")


def review_github_code(code: str, language: str, filename: str) -> dict:
    """
    AI-powered code review using Gemini.

    Returns:
        {
            "overall_rating": str (e.g. "7/10"),
            "summary": str,
            "bugs": [str],
            "style_tips": [str],
            "optimizations": [str],
            "positive_highlights": [str]
        }
    """
    if not API_KEY:
        return {"error": "API key not configured"}

    if len(code) > 8000:
        code = code[:8000] + "\n\n... [truncated for review]"

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""You are a senior {language} code reviewer. Review the following code from '{filename}'.

Be constructive, specific, and beginner-friendly. Focus on:
1. Correctness & potential bugs
2. Code style & readability
3. Performance & optimization opportunities
4. What the student did well

Code:
```{language}
{code}
```

Respond ONLY with valid JSON (no markdown, no backticks):
{{
  "overall_rating": "X/10",
  "summary": "1-2 sentence overall impression",
  "bugs": ["List of actual bugs or potential runtime issues. Empty array if none."],
  "style_tips": ["Code style / readability improvements"],
  "optimizations": ["Performance or algorithmic improvements"],
  "positive_highlights": ["What was done well — be specific and genuine"]
}}
"""
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.3, "max_output_tokens": 1500}
        )
        raw = response.text.strip()
        raw = re.sub(r"```(?:json)?", "", raw).strip().strip("```").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise ValueError("Could not parse review JSON")

    except Exception as e:
        return {"error": str(e)}
