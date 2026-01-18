import fitz  # PyMuPDF
from PIL import Image

def load_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def load_image(file):
    return "Image uploaded. OCR disabled on cloud."
