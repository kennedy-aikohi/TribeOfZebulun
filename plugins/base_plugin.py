class DecoderPlugin:
    name = "Base"
    description = ""

    def detect(self, data):
        raise NotImplementedError

    def decode(self, data):
        raise NotImplementedError
