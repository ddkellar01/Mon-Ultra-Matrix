"""Deconstruction - strip a contract/system to its core logic (from credkellar/deconstruction)."""
from .evm_re import disassemble
DEAD = {"STOP","INVALID","REVERT"}
def deconstruct(hexcode):
    ops=disassemble(hexcode); names=[o["op"] for o in ops]
    core=[n for n in names if n not in DEAD]
    return {"total_instructions": len(names), "core_instructions": len(core),
            "fluff_ratio": round(1-len(core)/len(names),3) if names else 0.0,
            "core_logic": sorted(set(core)), "storage_writes": names.count("SSTORE"),
            "external_calls": sum(names.count(x) for x in ("CALL","DELEGATECALL","STATICCALL","CALLCODE"))}
def deconstruct_text(text):
    """Text version: strip filler words, keep the load-bearing terms."""
    filler={"the","a","an","very","really","just","actually","basically","simply","stuff","things"}
    words=[w for w in text.split() if w.lower().strip(".,") not in filler]
    return {"original_words": len(text.split()), "core_words": len(words), "core": " ".join(words)}
