from oletools.olevba import VBA_Parser

def extract(path):
    payloads = []
    vba = VBA_Parser(path)

    if vba.detect_vba_macros():
        for (_, _, _, code) in vba.extract_macros():
            payloads.append(code.encode())

    return payloads
