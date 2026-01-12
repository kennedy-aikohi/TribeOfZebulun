import json, hashlib

def create(payloads):
    return [{
        "sha256": hashlib.sha256(p).hexdigest(),
        "size": len(p),
        "preview": p[:200].hex()
    } for p in payloads]
