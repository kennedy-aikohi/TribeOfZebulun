import os
import hashlib
from core.utils.entropy import shannon_entropy

COMMON_OPCODES = [
    b"\x90",  # NOP
    b"\xE8",  # CALL
    b"\xE9",  # JMP
    b"\xEB",  # JMP SHORT
    b"\xCC",  # INT3
]

SHELLCODE_DIR = "extracted/shellcode"
os.makedirs(SHELLCODE_DIR, exist_ok=True)


def looks_like_shellcode(data: bytes) -> bool:
    if len(data) < 64 or len(data) > 500_000:
        return False

    entropy = shannon_entropy(data)
    if entropy < 6.2 or entropy > 8.0:
        return False

    opcode_hits = sum(data.count(op) for op in COMMON_OPCODES)
    return opcode_hits > 10


def detect_shellcode(data: bytes):
    results = []

    if not looks_like_shellcode(data):
        return results

    sha1 = hashlib.sha1(data).hexdigest()
    filename = f"shellcode_{sha1[:12]}.bin"
    path = os.path.join(SHELLCODE_DIR, filename)

    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(data)

    results.append((data, f"shellcode:{filename}"))
    return results
