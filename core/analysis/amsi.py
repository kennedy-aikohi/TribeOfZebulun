AMSI_STRINGS = [
    "amsiInitFailed",
    "AmsiUtils",
    "System.Management.Automation",
    "cachedGroupPolicySettings",
    "ScriptBlockLogging"
]

def detect_amsi(text: str):
    hits = [s for s in AMSI_STRINGS if s.lower() in text.lower()]
    return hits
