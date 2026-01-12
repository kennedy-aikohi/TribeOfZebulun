import re

PS_CMD = re.compile(rb'powershell.*?-enc\s+([A-Za-z0-9+/=]+)', re.I)


def try_powershell(data: bytes):
    results = []

    for match in PS_CMD.findall(data):
        try:
            decoded = match
            results.append((decoded, "powershell-enc"))
        except Exception:
            pass

    return results
