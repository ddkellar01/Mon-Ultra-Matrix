"""Isolated experiment sandbox. Runs a callable and reports success OR failure to the caller.
The failure itself is not kept - the registry removes it (see experiment.py).
"""
import traceback
def run_experiment(fn, name="experiment"):
    try:
        out=fn(); return {"name":name,"status":"SUCCESS","result":str(out)[:500],"lesson":""}
    except Exception as e:
        return {"name":name,"status":"FAILED","result":f"{type(e).__name__}: {e}","lesson":traceback.format_exc(limit=2)[-400:]}
