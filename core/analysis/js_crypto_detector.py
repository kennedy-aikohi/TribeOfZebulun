import re

def detect_js_crypto(text: str):
    hits = []

    if re.search(r"charCodeAt\s*\(.*\)\s*\^", text):
        hits.append("rc4")

    if re.search(r"CryptoJS\.AES", text):
        hits.append("aes")

    return hits
