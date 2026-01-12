import re
import base64

JS_ATOB = re.compile(r'atob\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)')
JS_CHARS = re.compile(r'fromCharCode\s*\(([^)]+)\)')
JS_EVAL = re.compile(r'eval\s*\(')


def try_js(data: bytes):
    results = []

    try:
        text = data.decode(errors="ignore")
    except Exception:
        return []

    changed = False

    for match in JS_ATOB.findall(text):
        try:
            decoded = base64.b64decode(match).decode(errors="ignore")
            text = text.replace(match, decoded)
            changed = True
        except Exception:
            pass

    for match in JS_CHARS.findall(text):
        try:
            chars = ''.join(chr(int(x.strip())) for x in match.split(","))
            text = text.replace(match, chars)
            changed = True
        except Exception:
            pass

    if changed or JS_EVAL.search(text):
        results.append((text.encode(), "js-deobfuscation"))

    return results
