MITRE_MAP = {
    "amsi": "T1562.001 – Disable Security Tools",
    "powershell": "T1059.001 – PowerShell",
    "frombase64string": "T1140 – Deobfuscate",
    "invoke-expression": "T1059 – Command Execution",
    "reflection": "T1620 – Reflective Code Loading",
    "shellcode": "T1055 – Process Injection",
}


def map_mitre(text: str):
    hits = []
    t = text.lower()

    for key, technique in MITRE_MAP.items():
        if key in t:
            hits.append(technique)

    return list(set(hits))
