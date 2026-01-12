import re

def rc4(key, data):
    S = list(range(256))
    j = 0
    out = []

    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])

    return bytes(out)

def try_rc4(data: bytes):
    text = data.decode(errors="ignore")

    m = re.search(r"rc4\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*([a-zA-Z0-9_]+)\s*\)", text)
    if not m:
        return []

    key = m.group(1)

    b64 = re.search(r"decodeBase64\s*\(\s*([a-zA-Z0-9_]+)\s*\)", text)
    if not b64:
        return []

    block = re.search(r"var\s+" + b64.group(1) + r"\s*=\s*['\"]([^'\"]+)", text)
    if not block:
        return []

    try:
        import base64
        decoded = base64.b64decode(block.group(1))
        plain = rc4(key, decoded)
        return [(plain, "rc4")]
    except:
        return []
