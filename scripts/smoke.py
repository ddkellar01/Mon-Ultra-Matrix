import sys; sys.path.insert(0, "src")
from mon_ultra_matrix.monad_stats import summary
from mon_ultra_matrix.evm_re import analyze
from mon_ultra_matrix.experiment import ProjectRegistry, pipeline
from mon_ultra_matrix.matrix_runner import run_matrix
import tempfile, pathlib
print(summary())
code = "6080604052348015600e575f5ffd5b50606380601a5f395ff3fe60806040525f5ffd"
print(analyze(code))
with tempfile.TemporaryDirectory() as d:
    reg = ProjectRegistry(pathlib.Path(d)/"r.jsonl")
    pipeline(reg, "smoke-ok", lambda: "ok")
    pipeline(reg, "smoke-fail", lambda: 1/0)
    s = reg.summary(); print(s); assert s == {"total":1,"successful":1,"failed":0,"failures_removed":True}
    assert [x["name"] for x in reg.all()] == ["smoke-ok"]
m = run_matrix(["a","b"], {"len": len, "upper": lambda x: x.upper()})
print(m); assert m["total"]==4 and m["attempted"]==4 and m["removed"]==0
from mon_ultra_matrix.docker_images import total_pulls
from mon_ultra_matrix.globe import backend_payload
assert total_pulls()==6699 and backend_payload(["aave","kuru"])["points"]
from mon_ultra_matrix.gemini_planner import recommend_all
ua = recommend_all(); print("unified agents:", ua["unified_recommended_agents_zero_latency"]); assert ua["unified_recommended_agents_zero_latency"]>0
print("SMOKE OK")
