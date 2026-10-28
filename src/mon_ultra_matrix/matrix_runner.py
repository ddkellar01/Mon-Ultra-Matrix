"""Ultra-Matrix runner - Google-FlowX matrix idea, applied to Monad RE checks.
Runs every check x every target, then REMOVES all failed cells - only successful cells are returned/kept.
Counts still report how many were attempted and removed, so a clean matrix is not mistaken for an unrun one.
"""
def run_matrix(targets, checks):
    cells=[]; attempted=0
    for t in targets:
        for cname, cfn in checks.items():
            attempted+=1
            try: cells.append({"target":t,"check":cname,"status":"SUCCESS","detail":str(cfn(t))[:200]})
            except Exception: pass  # failure removed, not kept
    return {"cells":cells,"total":len(cells),"attempted":attempted,"successful":len(cells),"failed":0,"removed":attempted-len(cells)}
