"""Forensics slice merged from Crypto-Recovery-Forensics: address checks + risk flags."""
def is_valid_evm_address(a): return isinstance(a,str) and a.startswith("0x") and len(a)==42 and all(c in "0123456789abcdefABCDEF" for c in a[2:])
def checksum_note(a): return "checksummed" if any(c.isupper() for c in a[2:]) and any(c.islower() for c in a[2:]) else "not checksummed / all one case"
def risk_flags(analysis):
    flags=[]
    if analysis.get("has_delegatecall"): flags.append("DELEGATECALL present - proxy / upgrade risk, verify implementation")
    if analysis.get("has_selfdestruct"): flags.append("SELFDESTRUCT present - contract can be destroyed")
    if analysis.get("entropy",0)>7.5: flags.append("High bytecode entropy - possible obfuscation / packed data")
    if not analysis.get("selectors"): flags.append("No PUSH4 selectors found - may not be a standard dispatcher contract")
    return flags
