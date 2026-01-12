from core.utils.entropy import shannon_entropy

def score_payload(old: bytes, new: bytes):
    return shannon_entropy(old) - shannon_entropy(new)
