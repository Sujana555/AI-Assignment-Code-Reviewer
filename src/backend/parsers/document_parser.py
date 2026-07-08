import fitz

def extract_text(path):
    doc = fitz.open(path)
    text = "".join([page.get_text() for page in doc])
    return text