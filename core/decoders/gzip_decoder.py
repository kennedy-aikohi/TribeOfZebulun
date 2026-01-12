import gzip
import io


def try_gzip(data: bytes):
    """
    Attempts to decompress GZIP-compressed payloads
    """

    try:
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as gz:
            decoded = gz.read()

        if decoded and len(decoded) > 10:
            return decoded

    except Exception:
        pass

    return None
