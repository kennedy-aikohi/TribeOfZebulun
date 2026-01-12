import re


def simple_strings(data, min_len=4):
    """
    Extract readable ASCII & UTF-16LE strings from binary data.
    Used as fallback when decoding fails.
    """
    results = set()

    # ASCII strings
    ascii_re = re.compile(rb"[ -~]{%d,}" % min_len)
    for match in ascii_re.findall(data):
        try:
            results.add(match.decode("ascii", errors="ignore"))
        except Exception:
            pass

    # UTF-16LE strings
    utf16_re = re.compile(rb"(?:[ -~]\x00){%d,}" % min_len)
    for match in utf16_re.findall(data):
        try:
            results.add(match.decode("utf-16le", errors="ignore"))
        except Exception:
            pass

    return sorted(results)


def render_tree(nodes):
    lines = []

    for n in nodes:
        indent = "  " * n["depth"]
        label = n.get("decoder", "root")

        intent_flag = ""
        if n.get("intent"):
            intent_flag = " ⚠"

        lines.append(
            f"{indent}└─ {label} | entropy={n['entropy']}{intent_flag}"
        )

    return "\n".join(lines)
