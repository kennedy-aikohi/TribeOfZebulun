import string


def try_xor(data: bytes):
    """
    Bruteforce single-byte XOR encoded payloads
    """

    if len(data) < 20:
        return None

    for key in range(1, 256):
        decoded = bytes(b ^ key for b in data)

        printable = sum(c in string.printable.encode() for c in decoded)
        if printable / len(decoded) > 0.9:
            return decoded

    return None
