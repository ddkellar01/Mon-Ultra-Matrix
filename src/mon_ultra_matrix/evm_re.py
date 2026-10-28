"""EVM reverse engineering: bytecode disassembly, selectors, entropy. Pure stdlib."""
import math
OPCODES = {0x00:"STOP",0x01:"ADD",0x02:"MUL",0x03:"SUB",0x04:"DIV",0x10:"LT",0x11:"GT",0x14:"EQ",0x15:"ISZERO",0x20:"KECCAK256",0x30:"ADDRESS",0x31:"BALANCE",0x33:"CALLER",0x34:"CALLVALUE",0x35:"CALLDATALOAD",0x36:"CALLDATASIZE",0x37:"CALLDATACOPY",0x50:"POP",0x51:"MLOAD",0x52:"MSTORE",0x54:"SLOAD",0x55:"SSTORE",0x56:"JUMP",0x57:"JUMPI",0x5b:"JUMPDEST",0xa0:"LOG0",0xa1:"LOG1",0xa2:"LOG2",0xa3:"LOG3",0xa4:"LOG4",0xf0:"CREATE",0xf1:"CALL",0xf2:"CALLCODE",0xf4:"DELEGATECALL",0xfa:"STATICCALL",0xfd:"REVERT",0xfe:"INVALID",0xff:"SELFDESTRUCT"}
for i in range(1,33): OPCODES[0x5f+i-1+1] = f"PUSH{i}" if False else OPCODES.get(0x5f+i, f"PUSH{i}")
for i in range(1,33): OPCODES[0x60+i-1] = f"PUSH{i}"
for i in range(1,17): OPCODES[0x80+i-1] = f"DUP{i}"; OPCODES[0x90+i-1] = f"SWAP{i}"
def clean_hex(h):
    h=h.strip().lower(); return h[2:] if h.startswith("0x") else h
def disassemble(hexcode):
    b=bytes.fromhex(clean_hex(hexcode)); out=[]; pc=0
    while pc < len(b):
        op=b[pc]; name=OPCODES.get(op, f"UNKNOWN_{op:02x}"); arg=""
        if 0x60 <= op <= 0x7f:
            n=op-0x5f; arg=b[pc+1:pc+1+n].hex(); pc+=1+n
        else: pc+=1
        out.append({"pc": pc if not arg else pc, "op": name, "arg": arg})
    return out
def selectors(hexcode):
    """Function selectors pushed as PUSH4 in the dispatcher."""
    b=bytes.fromhex(clean_hex(hexcode)); sels=[]
    for i in range(len(b)-4):
        if b[i]==0x63: sels.append("0x"+b[i+1:i+5].hex())
    return sorted(set(sels))
def entropy(hexcode):
    b=bytes.fromhex(clean_hex(hexcode))
    if not b: return 0.0
    from collections import Counter; c=Counter(b); n=len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())
def analyze(hexcode):
    ops=disassemble(hexcode); names=[o["op"] for o in ops]
    return {"bytes": len(bytes.fromhex(clean_hex(hexcode))), "instructions": len(ops),
            "selectors": selectors(hexcode), "entropy": round(entropy(hexcode),4),
            "has_delegatecall": "DELEGATECALL" in names, "has_selfdestruct": "SELFDESTRUCT" in names,
            "has_create": "CREATE" in names, "sstore_count": names.count("SSTORE"), "sload_count": names.count("SLOAD")}
