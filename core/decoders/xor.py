import string
from core.utils.entropy import shannon_entropy

PRINTABLE = set(bytes(string.printable, "ascii"))

def score_plaintext(data: bytes) -> float:
    if not data:
        return 0
    printable_ratio = sum(b in PRINTABLE for b in data) / len(data)
    entropy_score = 8 - shannon_entropy(data)
    return printable_ratio + entropy_score


def xor_bruteforce(data: bytes):
    results = []

    for key in range(1, 256):
        decoded = bytes(b ^ key for b in data)
        score = score_plaintext(decoded)

        if score > 3.5:  # threshold
            results.append((decoded, f"xor_key_{key:02x}"))

    return results
