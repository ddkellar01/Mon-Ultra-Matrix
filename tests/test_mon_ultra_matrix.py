from mon_ultra_matrix.monad_stats import summary, TOKENOMICS, SNAPSHOT
from mon_ultra_matrix.evm_re import analyze, disassemble, selectors
from mon_ultra_matrix.abi_re import identify, is_erc20
from mon_ultra_matrix.forensics import is_valid_evm_address, risk_flags
from mon_ultra_matrix.standards import score
from mon_ultra_matrix.tx_tracer import TxGraph
from mon_ultra_matrix.protocol_re import fingerprint
from mon_ultra_matrix.experiment import ProjectRegistry, pipeline
from mon_ultra_matrix.matrix_runner import run_matrix
from mon_ultra_matrix.learner import KNN, MLP, reason
from mon_ultra_matrix.deployer import deploy_plan
from mon_ultra_matrix.sandbox import run_experiment

CODE = "6080604052348015600e575f5ffd5b5063a9059cbb5063a9059cbb00"

def test_stats():
    s = summary(); assert "10000 TPS" in s and "Monad" in s
    assert TOKENOMICS["total_supply"] == 100_000_000_000
    assert TOKENOMICS["cliff_unlock"]["date"] == "2026-11-24"
    assert SNAPSHOT["apps_live"] == "143+"

def test_disassemble_and_selectors():
    ops = disassemble(CODE); assert ops[0]["op"] == "PUSH1"
    assert "0xa9059cbb" in selectors(CODE)

def test_abi():
    assert identify("0xa9059cbb") == "transfer(address,uint256)"
    assert is_erc20(["0xa9059cbb","0x23b872dd","0x70a08231","0x18160ddd"])

def test_forensics_and_standards():
    assert is_valid_evm_address("0x"+"a"*40) and not is_valid_evm_address("0x123")
    a = analyze(CODE); assert isinstance(risk_flags(a), list); assert 0 <= score(a) <= 1

def test_txgraph():
    g = TxGraph(); g.add("A","B",5,"h1"); g.add("B","C",3,"h2")
    assert g.total_out("A")==5 and g.counterparties("B")==["A","C"] and "C" in g.hops("A")

def test_protocol_fingerprint():
    assert "uniswap_v4" in fingerprint(["PoolManager unlock swap"])

def test_registry_keeps_success_removes_failure(tmp_path):
    reg = ProjectRegistry(tmp_path/"r.jsonl")
    pipeline(reg, "ok", lambda: "done")
    e = pipeline(reg, "bad", lambda: 1/0)
    assert e["status"]=="FAILED" and e["removed"] is True and e["recorded"] is False
    s = reg.summary(); assert s["total"]==1 and s["successful"]==1 and s["failed"]==0
    assert [x["name"] for x in reg.all()] == ["ok"]

def test_remove_failures_purges_existing_file(tmp_path):
    p = tmp_path/"r.jsonl"; reg = ProjectRegistry(p)
    import json; p.write_text(json.dumps({"name":"old-ok","status":"SUCCESS"})+"\n"+json.dumps({"name":"old-bad","status":"FAILED"})+"\n")
    assert reg.remove_failures()==1 and [x["name"] for x in reg.all()] == ["old-ok"]

def test_deployer_gates_failures(tmp_path):
    reg = ProjectRegistry(tmp_path/"r.jsonl"); e = pipeline(reg, "bad", lambda: 1/0)
    assert deploy_plan(e)["deploy"] is False

def test_matrix_removes_failed_cells():
    m = run_matrix(["x"], {"ok": lambda v: v, "boom": lambda v: 1/0})
    assert m["attempted"]==2 and m["total"]==1 and m["successful"]==1 and m["failed"]==0 and m["removed"]==1 and len(m["cells"])==1

def test_sandbox():
    assert run_experiment(lambda: 42)["status"]=="SUCCESS"
    assert run_experiment(lambda: 1/0)["status"]=="FAILED"

def test_learners():
    knn = KNN(k=1).fit([[0,0],[10,10]], ["low","high"]); assert knn.predict([9,9])=="high"
    mlp = MLP(2).train([[0,0],[1,1]],[0,1],epochs=50); assert 0 <= mlp.predict([1,1]) <= 1
    assert reason("delegatecall proxy upgrade")["answers"]

def test_entropy_range():
    a = analyze(CODE); assert 0 <= a["entropy"] <= 8

# --- Second merge: Docker Hub images ---
from mon_ultra_matrix.docker_images import IMAGES, total_pulls, pull_commands
from mon_ultra_matrix.deconstruction import deconstruct, deconstruct_text
from mon_ultra_matrix.vuln_scan import scan_source, scan_contract
from mon_ultra_matrix.bounty import in_scope, triage
from mon_ultra_matrix.contract_audit import audit_bytecode, monad_parallel_notes
from mon_ultra_matrix.malware_sandbox import triage_bytes, indicators
from mon_ultra_matrix.compressor import compress, decompress, dedup_chunks
from mon_ultra_matrix.honeypot import parse_log
from mon_ultra_matrix.malware_research import extract_iocs, catalog_sample
from mon_ultra_matrix.globe import backend_payload, frontend_snippet, point_for

def test_docker_registry():
    assert len(IMAGES)==10 and total_pulls()==6699
    assert IMAGES["monad-vul-x"]["module"]=="contract_audit" and len(pull_commands())==10

def test_deconstruction():
    d = deconstruct(CODE); assert d["core_instructions"]>0 and 0 <= d["fluff_ratio"] <= 1
    assert deconstruct_text("the very core logic")["core_words"] < 4

def test_vuln_scan():
    hits = scan_source("password = 'hunter2'\nresult = eval(user_input)")
    names = {h["pattern"] for h in hits}; assert {"hardcoded-secret","eval-exec"} <= names
    assert scan_contract(analyze(CODE)) is not None

def test_bounty_scope():
    assert in_scope("api.monad.xyz", ["monad.xyz"]) and not in_scope("evil.com", ["monad.xyz"])
    assert triage("RCE","critical",True)["score"]==9.0 and triage("RCE","critical",False)["action"].startswith("drop")

def test_contract_audit():
    f = audit_bytecode("60006000f1600060005500")  # CALL-ish + SSTORE sequence presence check is heuristic
    assert isinstance(f, list) and monad_parallel_notes()

def test_malware_sandbox_static():
    t = triage_bytes(b"MZ hello world CreateRemoteThread padding padding")
    assert len(t["sha256"])==64 and "CreateRemoteThread" in indicators(t["strings"])

def test_compressor_roundtrip():
    data = (b"monad-"*5000)
    packed, meta = compress(data); assert meta["ratio"] < 0.2
    deduped, dm = dedup_chunks(data); assert dm["unique_chunks"] < dm["chunks"] and decompress(packed)

def test_honeypot_log():
    r = parse_log("1.2.3.4 user: root password: 123456\n1.2.3.4 user: admin password: admin")
    assert r["attempts"]==2 and r["top_ips"][0][0]=="1.2.3.4"

def test_malware_research_iocs():
    i = extract_iocs("c2 at 10.0.0.9 and bad.example.com via http://bad.example.com/x hash "+"a"*64)
    assert "10.0.0.9" in i["ips"] and i["sha256"]==["a"*64]
    assert catalog_sample("s.bin", b"data")["size"]==4

def test_globe_payload():
    pl = backend_payload(["aave","kuru"], ["tx1"]); assert len(pl["points"])==3 and len(pl["arcs"])==1
    assert "GLOBE_DATA" in frontend_snippet(pl) and -85 <= point_for("x")["lat"] <= 85

# --- Gemini Pro Thinking (Extended) planner: per repo + unified ---
from mon_ultra_matrix.gemini_planner import REPO_GRAPHS, recommend, recommend_for_repo, recommend_all, build_gemini_prompt, call_gemini
def test_planner_covers_all_17_sources():
    assert len(REPO_GRAPHS)==17
    assert "Google-FlowX" in REPO_GRAPHS and "monad-vul-x" in REPO_GRAPHS and "Autonomous-Tech-Infrastructure-Platform" in REPO_GRAPHS
def test_recommend_width_is_zero_queue():
    r = recommend([("a",100,[]),("b",100,[]),("c",100,[]),("d",100,["a","b","c"])], "demo")
    assert r["recommended_agents"]==3 and r["queue_wait_ms_at_recommended"]==0
    assert r["sequential_ms"]==400 and r["critical_path_ms"]==200 and r["wall_clock_ms_at_recommended"]==200
def test_per_repo_numbers():
    assert recommend_for_repo("Google-FlowX")["recommended_agents"]==4
    assert recommend_for_repo("monad-vul-x")["recommended_agents"]==5
    assert recommend_for_repo("bug-bounty-xterminator")["recommended_agents"]==5
    assert recommend_for_repo("IvyTech-Nexus-Omni-Institution")["recommended_agents"]==4
def test_unified_total_is_sum_of_per_repo():
    a = recommend_all()
    assert a["unified_recommended_agents_zero_latency"]==sum(v["recommended_agents"] for v in a["per_repo"].values())
    assert a["unified_repo"]=="Mon-Ultra-Matrix" and len(a["per_repo"])==17
    assert a["gemini"]["source_repo"].startswith("Google-FlowX")
def test_gemini_offline_safe():
    assert call_gemini("anything") is None or isinstance(call_gemini("anything"), dict)
    assert "Decompose" in build_gemini_prompt("audit a contract")
def test_cycle_rejected():
    import pytest; 
    with pytest.raises(ValueError): recommend([("a",1,["b"]),("b",1,["a"])], "bad")
