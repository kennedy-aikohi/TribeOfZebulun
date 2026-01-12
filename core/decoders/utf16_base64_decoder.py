import base64
import re

UTF16_RE = re.compile(rb'([A-Za-z0-9+/]{40,}={0,2})')


def try_utf16_base64(data: bytes):
    results = []

    try:
        text = data.decode(errors="ignore")
    except Exception:
        return []

    for match in UTF16_RE.findall(text.encode()):
        try:
            raw = base64.b64decode(match)
            decoded = raw.decode("utf-16le", errors="ignore").encode()
            results.append((decoded, "utf16-base64"))
        except Exception:
            continue

    return results
