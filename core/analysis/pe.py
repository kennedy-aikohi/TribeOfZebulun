def extract_pe(data: bytes):
    """
    Extract embedded PE files (MZ header) from memory blobs
    """
    results = []

    mz = b"MZ"
    offset = 0

    while True:
        idx = data.find(mz, offset)
        if idx == -1:
            break

        pe = data[idx:]
        if b"PE\x00\x00" in pe[:1024]:
            results.append(pe)

        offset = idx + 2

    return results
