import pefile, hashlib

def analyze(data):
    findings = []

    if data.startswith(b"MZ"):
        findings.append("Embedded PE")

    if b"\xfc\xe8" in data:
        findings.append("Shellcode")

    return findings
