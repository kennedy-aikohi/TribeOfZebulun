from core.decoders import base64, gzip, xor, regex
from core.extractors import shellcode, pe, urls

MAX_DEPTH = 12


def decode_engine(data: bytes, results: list, stop_cb, depth=0):
    if stop_cb and not stop_cb():
        return

    if depth >= MAX_DEPTH:
        return

    layer = {
        "depth": depth,
        "size": len(data),
        "hash": shellcode.sha256(data),
        "artifacts": []
    }

    # --- EXTRACT FIRST (PowerDecode style) ---
    layer["artifacts"] += urls.find(data)
    layer["artifacts"] += pe.find(data)
    layer["artifacts"] += shellcode.find(data)

    results.append(layer)

    # --- DECODERS (order matters) ---
    for decoder in (
        base64.try_decode,
        gzip.try_decode,
        xor.try_decode,
        regex.try_decode,
    ):
        decoded = decoder(data)
        if decoded and decoded != data:
            decode_engine(decoded, results, stop_cb, depth + 1)
