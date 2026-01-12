from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_MODE_64


def detect_shellcode(data: bytes) -> bool:
    """
    Heuristic shellcode detection
    """
    suspicious = [
        b"\x90" * 8,        # NOP sled
        b"\xcc" * 4,        # INT3
        b"\xeb",            # short jump
        b"\xe8",            # call
    ]

    return any(sig in data[:200] for sig in suspicious)


def disassemble_shellcode(data: bytes) -> str:
    """
    Disassemble first bytes of shellcode
    """
    try:
        md = Cs(CS_ARCH_X86, CS_MODE_32)
        lines = []
        for ins in md.disasm(data[:200], 0x1000):
            lines.append(f"0x{ins.address:x}: {ins.mnemonic} {ins.op_str}")
        return "\n".join(lines)
    except Exception:
        return ""
