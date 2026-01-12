import pefile


def detect(data: bytes):
    """
    Detect raw shellcode or embedded PE
    Returns metadata dictionary or None
    """

    # --- PE Detection (MZ carving) ---
    if data.startswith(b"MZ"):
        try:
            pe = pefile.PE(data=data, fast_load=True)
            return {
                "type": "PE",
                "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
                "sections": len(pe.sections),
            }
        except Exception:
            pass

    # --- Shellcode heuristic ---
    entropy = _entropy(data)

    if entropy > 6.5 and len(data) > 100:
        return {
            "type": "Shellcode",
            "entropy": round(entropy, 2),
            "size": len(data),
        }

    return None


def _entropy(data: bytes) -> float:
    from math import log2
    if not data:
        return 0.0

    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1

    ent = 0.0
    for count in freq.values():
        p = count / len(data)
        ent -= p * log2(p)

    return ent
