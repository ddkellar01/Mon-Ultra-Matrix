"""Standards compliance slice - merged from ISO-IECx.
Checks a contract analysis against a small ISO/IEC-flavoured control set. Educational, not a certification.
"""
CONTROLS = [
 ("access-control", lambda a: not a.get("has_selfdestruct"), "No uncontrolled SELFDESTRUCT (ISO/IEC 27001 A.9 / access & change control spirit)"),
 ("upgrade-transparency", lambda a: not a.get("has_delegatecall") or a.get("selectors"), "DELEGATECALL only behind a visible dispatcher"),
 ("auditability", lambda a: a.get("sstore_count",0)>=0, "State writes are on-chain and auditable"),
 ("interface-clarity", lambda a: len(a.get("selectors",[]))>0, "Public interface is enumerable from bytecode"),
]
def audit(analysis):
    return [{"control":n,"pass":bool(fn(analysis)),"note":note} for n,fn,note in CONTROLS]
def score(analysis):
    r=audit(analysis); return round(sum(1 for x in r if x["pass"])/len(r),3) if r else 0.0
