"""BUG-BOUNTY-xterminator - bounty lifecycle: scope -> triage -> report. Scope-guarded."""
SEVERITY = {"critical":9.0,"high":7.5,"medium":5.0,"low":2.5,"info":0.5}
def in_scope(target, allowlist):
    t=target.lower(); return any(t==a.lower() or t.endswith("."+a.lower()) or t.startswith(a.lower()) for a in allowlist)
def triage(title, severity, in_scope_flag):
    if not in_scope_flag: return {"title":title,"action":"drop - out of scope","score":0.0}
    return {"title":title,"action":"report","score":SEVERITY.get(severity.lower(),0.5),"severity":severity.lower()}
def report_scaffold(title, target, steps):
    lines=[f"# {title}","","Target: "+target,"","## Steps to reproduce"]+[f"{i+1}. {s}" for i,s in enumerate(steps)]+["","## Impact","","## Remediation",""]
    return "\n".join(lines)
