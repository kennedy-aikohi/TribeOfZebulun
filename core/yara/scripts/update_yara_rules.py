import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RULES_DIR = BASE_DIR / "core" / "yara" / "rules"

RULE_SOURCES = {
    "signature-base": "https://github.com/Neo23x0/signature-base.git",
    "malware-yara": "https://github.com/Yara-Rules/rules.git",
}


def update():
    RULES_DIR.mkdir(parents=True, exist_ok=True)

    for name, repo in RULE_SOURCES.items():
        dest = RULES_DIR / name
        if dest.exists():
            subprocess.run(["git", "-C", str(dest), "pull"], check=False)
        else:
            subprocess.run(["git", "clone", repo, str(dest)], check=False)

    print("[✓] YARA rules updated")


if __name__ == "__main__":
    update()
