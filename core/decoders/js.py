import re
import base64

def js_peel(data: bytes):
    try:
        text = data.decode(errors="ignore")
    except Exception:
        return []

    results = []

    # atob("...")
    for match in re.findall(r'atob\(["\']([^"\']+)["\']\)', text):
        try:
            decoded = base64.b64decode(match)
            results.append((decoded, "js_atob"))
        except Exception:
            pass

    # String.fromCharCode(...)
    for match in re.findall(r'fromCharCode\(([^)]+)\)', text):
        try:
            nums = [int(x.strip()) for x in match.split(",")]
            decoded = bytes(nums)
            results.append((decoded, "js_charcode"))
        except Exception:
            pass

    return results
