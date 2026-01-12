from oletools.olevba import VBA_Parser, TYPE_OLE, TYPE_OpenXML

def analyze_vba(path):
    results = {
        "has_macros": False,
        "suspicious": [],
        "macros": []
    }

    try:
        vbaparser = VBA_Parser(path)

        if vbaparser.detect_vba_macros():
            results["has_macros"] = True

            for (_, _, _, macro) in vbaparser.extract_macros():
                results["macros"].append(macro)

            for kw in vbaparser.analyze_macros():
                if kw.type == 'Suspicious':
                    results["suspicious"].append(kw.keyword)

        vbaparser.close()
    except Exception:
        pass

    return results
