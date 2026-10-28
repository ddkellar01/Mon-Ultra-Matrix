"""Core rule (updated 2026-10-27, Darion): keep successful projects only - REMOVE ALL FAILURES.
A failure is run, reported to the caller, then removed: it is never written to the registry,
and remove_failures() purges any FAILED entry already on disk.
Pipeline: experiment -> test -> learn -> deploy (only successes exist past the test step).
"""
import json, pathlib, time
class ProjectRegistry:
    def __init__(self, path="projects_registry.jsonl"): self.path=pathlib.Path(path)
    def record(self, entry):
        entry=dict(entry)
        if entry.get("status")!="SUCCESS":
            self.remove_failures()
            entry["recorded"]=False; entry["removed"]=True; return entry
        entry.setdefault("ts", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())); entry["recorded"]=True
        with self.path.open("a") as f: f.write(json.dumps(entry)+"\n")
        return entry
    def all(self):
        if not self.path.exists(): return []
        return [json.loads(l) for l in self.path.read_text().splitlines() if l.strip()]
    def successful(self): return [e for e in self.all() if e.get("status")=="SUCCESS"]
    def failed(self): return [e for e in self.all() if e.get("status")=="FAILED"]
    def remove_failures(self):
        """Purge every FAILED entry from the registry file. Returns how many were removed."""
        entries=self.all(); kept=[e for e in entries if e.get("status")=="SUCCESS"]
        removed=len(entries)-len(kept)
        if removed: self.path.write_text("".join(json.dumps(e)+"\n" for e in kept))
        return removed
    def summary(self):
        self.remove_failures(); a=self.all()
        return {"total":len(a),"successful":len(self.successful()),"failed":0,"failures_removed":True}
def pipeline(registry, name, experiment_fn, test_fn=None):
    from .sandbox import run_experiment
    exp=run_experiment(experiment_fn, name)
    if exp["status"]=="SUCCESS" and test_fn is not None:
        t=run_experiment(test_fn, name+"::test")
        if t["status"]!="SUCCESS": exp={"name":name,"status":"FAILED","result":exp["result"],"lesson":"test failed: "+t["result"]}
    exp["deployable"]= exp["status"]=="SUCCESS"
    return registry.record(exp)
