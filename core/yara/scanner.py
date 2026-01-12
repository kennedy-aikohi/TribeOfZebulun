import yara
from pathlib import Path

RULES_DIR = Path(__file__).parent / "rules"


def load_rules():
    valid_rules = {}
    skipped = []

    for rule in RULES_DIR.rglob("*.yar"):
        try:
            yara.compile(
                filepath=str(rule),
                externals={
                    "filepath": "",
                    "filename": "",
                    "extension": "",
                    "filetype": "",
                    "owner": ""
                }
            )
            valid_rules[str(rule)] = str(rule)

        except yara.SyntaxError as e:
            skipped.append((rule.name, str(e)))

    if skipped:
        print("[YARA] Skipped invalid rules:")
        for name, err in skipped:
            print(f"  - {name}: {err}")

    if not valid_rules:
        print("[YARA] No valid YARA rules loaded")
        return None

    return yara.compile(
        filepaths=valid_rules,
        externals={
            "filepath": "",
            "filename": "",
            "extension": "",
            "filetype": "",
            "owner": ""
        }
    )


YARA_RULES = load_rules()


def scan_with_yara(data: bytes, path: str = ""):
    if not YARA_RULES:
        return [], None, None

    try:
        matches = YARA_RULES.match(
            data=data,
            externals={
                "filepath": path,
                "filename": Path(path).name if path else "",
                "extension": Path(path).suffix if path else "",
                "filetype": "",
                "owner": ""
            }
        )

        rule_names = []
        family = None
        description = None

        for m in matches:
            rule_names.append(m.rule)

            if not family:
                family = (
                    m.meta.get("family")
                    or m.meta.get("malware")
                    or m.meta.get("threat")
                    or m.meta.get("family_name")
                )

            if not description:
                description = m.meta.get("description")

        return rule_names, family, description

    except Exception as e:
        print(f"[YARA] Scan error: {e}")
        return [], None, None
