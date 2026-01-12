import math
from collections import Counter

def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0

    freq = Counter(data)
    entropy = 0.0

    for c in freq.values():
        p = c / len(data)
        entropy -= p * math.log2(p)

    return entropy
