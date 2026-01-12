import base64
import re

BASE64_RE = re.compile(rb'(?:[A-Za-z0-9+/]{20,}={0,2})')


def try_base64(data: bytes):
    results = []

    for match in BASE64_RE.findall(data):
        try:
            decoded = base64.b64decode(match)
            if decoded and decoded != data:
                results.append((decoded, "base64"))
        except Exception:
            pass

    return results
