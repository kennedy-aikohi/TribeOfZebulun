INTENT_MAP = {
    "NETWORK": ["http://", "https://", "WinHttp", "InternetOpen"],
    "POWERSHELL": ["Invoke-", "IEX", "DownloadString", "Add-Type"],
    "AMSI": ["amsi", "AmsiScanBuffer", "amsiInitFailed"],
    "EXECUTION": ["CreateProcess", "ShellExecute", "cmd.exe", "powershell.exe"],
    "PERSISTENCE": ["Run\\", "Startup", "ScheduledTask"],
}

def classify_strings(strings):
    hits = {}

    for s in strings:
        lower = s.lower()
        for category, keys in INTENT_MAP.items():
            for k in keys:
                if k.lower() in lower:
                    hits.setdefault(category, set()).add(k)

    return {k: sorted(v) for k, v in hits.items()}
