import struct

MAX_PE_SIZE = 5_000_000  # 5MB safety cap


def is_valid_pe(data: bytes, offset: int) -> bool:
    """
    Validate PE header at given offset
    """
    try:
        if data[offset:offset + 2] != b"MZ":
            return False

        e_lfanew = struct.unpack_from("<I", data, offset + 0x3C)[0]
        pe_offset = offset + e_lfanew

        if data[pe_offset:pe_offset + 4] != b"PE\x00\x00":
            return False

        return True
    except Exception:
        return False


def carve_pes(data: bytes):
    """
    Carve embedded PE files from arbitrary data
    """
    results = []
    seen = set()

    idx = 0
    while True:
        idx = data.find(b"MZ", idx)
        if idx == -1:
            break

        if idx in seen:
            idx += 2
            continue

        seen.add(idx)

        if is_valid_pe(data, idx):
            chunk = data[idx: idx + MAX_PE_SIZE]
            results.append((chunk, f"embedded-pe@{idx}"))

        idx += 2

    return results
