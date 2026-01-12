import io
import zipfile
import struct

MAX_EMBED_SIZE = 2_000_000  # 2MB safety limit


def is_zip(data: bytes) -> bool:
    return data.startswith(b"PK\x03\x04")


def is_iso(data: bytes) -> bool:
    return b"CD001" in data[:0x8000]


def unpack_zip(data: bytes):
    """
    Unpack ZIP / DOCX content from memory
    """
    results = []

    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            for name in zf.namelist():
                try:
                    blob = zf.read(name)
                except Exception:
                    continue

                if not blob or len(blob) > MAX_EMBED_SIZE:
                    continue

                results.append((blob, f"zip:{name}"))
    except Exception:
        pass

    return results


def unpack_iso(data: bytes):
    """
    Very lightweight ISO carving (no mounting).
    Extracts files by scanning directory records.
    """
    results = []

    try:
        # ISO9660 volume descriptor offset
        offset = data.find(b"CD001")
        if offset == -1:
            return results

        # crude file carving: look for embedded PE / scripts
        signatures = {
            b"MZ": "embedded-pe",
            b"<script": "embedded-script",
            b"powershell": "embedded-powershell",
        }

        for sig, name in signatures.items():
            idx = data.lower().find(sig.lower())
            if idx != -1:
                chunk = data[idx: idx + MAX_EMBED_SIZE]
                results.append((chunk, f"iso:{name}"))

    except Exception:
        pass

    return results


def unpack_archives(data: bytes):
    """
    Unified unpacker entry point
    """
    results = []

    if is_zip(data):
        results.extend(unpack_zip(data))

    if is_iso(data):
        results.extend(unpack_iso(data))

    return results
