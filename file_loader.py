import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def load_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def load_image(file):
    img = Image.open(file)
    return pytesseract.image_to_string(img)
