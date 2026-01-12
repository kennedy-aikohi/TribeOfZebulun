def try_bin(data):
    results = []

    # Ignore PE files
    if data.startswith(b"MZ"):
        return results

    # Try XOR key detection (single-byte)
    for key in range(1, 256):
        decoded = bytes(b ^ key for b in data[:256])

        if b"MZ" in decoded or b"powershell" in decoded.lower():
            full = bytes(b ^ key for b in data)
            results.append((full, f"bin-xor-key-{key}"))

    return results
