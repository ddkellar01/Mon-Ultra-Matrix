"""VulnerabilitiesX - vulnerable-vs-secure pattern lab (OWASP-flavoured, educational)."""
import re
SOURCE_PATTERNS = [
 ("sql-injection", r"execute\s*\(\s*f?['\"]|%s.*format|\.format\(.*SELECT", "Use parameterised queries, never string-built SQL"),
 ("hardcoded-secret", r"(password|api_key|secret)\s*=\s*['\"][^'\"]+['\"]", "Move secrets to env / vault"),
 ("eval-exec", r"\b(eval|exec)\s*\(", "Never eval untrusted input"),
 ("weak-hash", r"\b(md5|sha1)\s*\(", "Use SHA-256+ / a password KDF for credentials"),
 ("debug-enabled", r"debug\s*=\s*True", "Disable debug in production"),
]
def scan_source(code):
    hits=[]
    for name,pat,fix in SOURCE_PATTERNS:
        if re.search(pat, code, re.I): hits.append({"pattern":name,"fix":fix})
    return hits
def scan_contract(analysis):
    hits=[]
    if analysis.get("has_selfdestruct"): hits.append({"pattern":"selfdestruct-present","fix":"Remove or strictly gate SELFDESTRUCT"})
    if analysis.get("has_delegatecall"): hits.append({"pattern":"delegatecall-present","fix":"Pin + audit the implementation contract"})
    if analysis.get("sstore_count",0)==0 and analysis.get("selectors"): hits.append({"pattern":"no-state-writes","fix":"Informational: read-only contract surface"})
    return hits
