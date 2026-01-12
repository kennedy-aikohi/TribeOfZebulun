import re

def extract_strings(data, min_len=4):
    ascii_re = rb"[ -~]{%d,}" % min_len
    unicode_re = rb"(?:[ -~]\x00){%d,}" % min_len

    strings = set()

    for m in re.findall(ascii_re, data):
        strings.add(m.decode(errors="ignore"))

    for m in re.findall(unicode_re, data):
        try:
            strings.add(m.decode("utf-16le", errors="ignore"))
        except Exception:
            pass

    return sorted(strings)
