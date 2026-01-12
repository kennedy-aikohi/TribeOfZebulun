from core.decoders.base64_decoder import try_base64
from core.decoders.utf16_base64_decoder import try_utf16_base64
from core.decoders.powershell_decoder import try_powershell
from core.decoders.js_decoder import try_js
from core.decoders.gzip_decoder import try_gzip
from core.decoders.xor_bruteforce import try_xor_bruteforce

DECODERS = [
    try_utf16_base64,
    try_base64,
    try_powershell,
    try_gzip,
    try_js,
    try_xor_bruteforce,
]
