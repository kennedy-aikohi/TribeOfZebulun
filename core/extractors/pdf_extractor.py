from pdfminer.high_level import extract_text

def extract(path):
    try:
        text = extract_text(path)
        return [text.encode()]
    except:
        return []
