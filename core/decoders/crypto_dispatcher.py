from core.decoders.rc4_decoder import try_rc4_js
from core.decoders.xor_bruteforce import try_xor_bruteforce

CRYPTO_DECODERS = {
    "rc4": [try_rc4_js],
    "xor": [try_xor_bruteforce],
}


def try_crypto(data: bytes, tags: list):
    outputs = []

    for tag in tags:
        for decoder in CRYPTO_DECODERS.get(tag, []):
            try:
                res = decoder(data)
                if res:
                    outputs.extend(res)
            except:
                pass

    return outputs
