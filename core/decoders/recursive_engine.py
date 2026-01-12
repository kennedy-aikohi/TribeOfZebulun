from core.decoders import DECODERS
from core.utils.entropy import shannon_entropy
from core.utils.tree import simple_strings
from core.unpackers.archive_unpacker import unpack_archives
from core.carvers.pe_carver import carve_pes
from core.carvers.shellcode_detector import detect_shellcode
from core.yara import scan_with_yara

import base64
import re
import hashlib

MAX_DEPTH = 10
MAX_SIZE = 2_000_000


INTENT_KEYWORDS = {
    "Execution": ["powershell", "cmd.exe", "wscript", "cscript"],
    "Network": ["http", "https", "tcp", "dns", "download"],
    "Persistence": ["registry", "runkey", "schtask", "startup"],
    "Evasion": ["amsi", "etw", "bypass"],
    "Payload": ["mz", "shellcode", "reflective", "dll"],
}

BASE64_RE = re.compile(r"^[A-Za-z0-9+/=]{40,}$")
PS_ENC_RE = re.compile(r"(?:-enc|-encodedcommand)\s+([A-Za-z0-9+/=]{40,})", re.I)


def classify_strings(strings):
    intent = {}
    for cat, keys in INTENT_KEYWORDS.items():
        hits = [s for s in strings if any(k in s.lower() for k in keys)]
        if hits:
            intent[cat] = list(set(hits))[:5]
    return intent


def promote_string_payloads(strings):
    for s in strings:
        s = s.strip()

        m = PS_ENC_RE.search(s)
        if m:
            try:
                yield base64.b64decode(m.group(1))
            except Exception:
                pass

        if BASE64_RE.match(s):
            try:
                raw = base64.b64decode(s)
                if len(raw) > 20:
                    yield raw
            except Exception:
                pass


def calculate_score(intent, yara_hits, entropy):
    score = 0
    score += len(yara_hits) * 15
    score += len(intent) * 10
    if entropy > 6.5:
        score += 15
    return min(score, 100)


def walk(data, results, running_cb, depth=0, parent_decoder="root", visited=None):
    if visited is None:
        visited = set()

    if not running_cb() or depth >= MAX_DEPTH or not data or len(data) > MAX_SIZE:
        return

    fingerprint = hashlib.sha256(data).hexdigest()
    if fingerprint in visited:
        return
    visited.add(fingerprint)

    entropy = shannon_entropy(data)
    strings = simple_strings(data)[:500]
    intent = classify_strings(strings)

    yara_hits, family, yara_desc = scan_with_yara(data)
    score = calculate_score(intent, yara_hits, entropy)

    try:
        preview = data[:1000].decode(errors="ignore")
    except Exception:
        preview = ""

    node = {
        "depth": depth,
        "decoder": parent_decoder,
        "size": len(data),
        "entropy": round(entropy, 2),
        "strings": strings,
        "intent": intent,
        "preview": preview,
        "raw": data,
        "is_binary": data[:2] == b"MZ" or entropy > 6.8,
        "yara": yara_hits,
        "family": family,
        "yara_desc": yara_desc,
        "score": score,
    }

    results.append(node)

    for extracted, name in unpack_archives(data):
        if not running_cb():
            return
        walk(extracted, results, running_cb, depth + 1, name, visited)

    for pe, name in carve_pes(data):
        if not running_cb():
            return
        walk(pe, results, running_cb, depth + 1, f"pe:{name}", visited)

    for sc, name in detect_shellcode(data):
        if not running_cb():
            return
        walk(sc, results, running_cb, depth + 1, f"shellcode:{name}", visited)

    for promoted in promote_string_payloads(strings):
        if not running_cb():
            return
        walk(promoted, results, running_cb, depth + 1, "string-promotion", visited)

    for decoder in DECODERS:
        if not running_cb():
            return
        try:
            for out, name in decoder(data):
                walk(out, results, running_cb, depth + 1, name, visited)
        except Exception:
            continue
