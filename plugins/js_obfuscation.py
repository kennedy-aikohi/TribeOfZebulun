import re, base64
from plugins.base_plugin import DecoderPlugin

class JSPlugin(DecoderPlugin):
    name = "JavaScript Decoder"

    def detect(self, data):
        return b"atob(" in data or b"fromcharcode" in data.lower()

    def decode(self, data):
        results = []
        text = data.decode(errors="ignore")

        for b64 in re.findall(r'atob\(["\'](.+?)["\']\)', text):
            try:
                results.append(base64.b64decode(b64))
            except:
                pass

        return results
