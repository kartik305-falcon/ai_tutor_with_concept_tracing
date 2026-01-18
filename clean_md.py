import os
import re

DOCS_DIR = "docs"


def clean_text(text):
    # remove weird spaces
    text = text.replace("\xa0", " ")

    # join broken lines
    text = re.sub(r'\n(?=[a-z])', ' ', text)

    # collapse multiple newlines
    text = re.sub(r'\n{2,}', '\n\n', text)

    return text.strip()


for file in os.listdir(DOCS_DIR):
    if file.endswith(".md"):
        path = os.path.join(DOCS_DIR, file)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()

        cleaned = clean_text(raw)

        with open(path, "w", encoding="utf-8") as f:
            f.write(cleaned)

        print(f"Cleaned {file}, chars={len(cleaned)}")
