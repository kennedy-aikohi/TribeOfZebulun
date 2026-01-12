from pathlib import Path

def load_file(path):
    p = Path(path)
    data = p.read_bytes()
    return data, p.suffix.lower()
