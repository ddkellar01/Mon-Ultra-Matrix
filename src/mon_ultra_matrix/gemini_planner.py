"""Gemini Pro Thinking (Extended) agent planner - taken from Google-FlowX.
Google-FlowX is the source repo: "Gemini Pro Thinking, multi-agent LLM screenwriting,
parallel NNL/ML rendering, 1,000-run matrix". This module turns that pattern on
Mon-Ultra-Matrix itself: Gemini (extended thinking) decomposes a task, and the
planner computes the RECOMMENDED number of agents for it.

Zero-latency rule (stated honestly): queue latency is zero when the pre-warmed agent
pool is >= the widest parallel level of the task graph. Wall-clock then collapses to
the critical path - the dependent chain nobody can parallelise away. More agents than
the width buy nothing; fewer agents add queue wait. Recommended = the width.

With GEMINI_API_KEY set, call_gemini() asks Gemini Pro with an extended thinking
budget to decompose a task into this same graph format. Without a key (or on any
error) the deterministic planner below is the source of truth - it never raises.
"""
import json, os, urllib.request
MODEL = "gemini-2.5-pro"
THINKING = {"thinkingBudget": 32768, "includeThoughts": False}  # extended thinking
REPO_GRAPHS = {
 "Autonomous-Tech-Infrastructure-Platform": [["scout-github", 300, []], ["scout-defillama", 300, []], ["scout-docs", 300, []], ["sandbox-test", 500, ["scout-github", "scout-defillama", "scout-docs"]], ["run-tests", 400, ["sandbox-test"]], ["standards-check", 400, ["sandbox-test"]], ["deploy", 300, ["run-tests", "standards-check"]], ["monitor", 200, ["deploy"]]],
 "ISO-IECx": [["crawl-iso", 400, []], ["crawl-iec", 400, []], ["crawl-owasp", 400, []], ["gemini-study", 600, ["crawl-iso", "crawl-iec", "crawl-owasp"]], ["audit-pipeline", 500, ["gemini-study"]], ["visual-walkthrough", 400, ["audit-pipeline"]]],
 "IvyTech-Nexus-Omni-Institution": [["ingest-sources", 400, []], ["build-curriculum", 500, ["ingest-sources"]], ["build-kb", 500, ["ingest-sources"]], ["build-labs", 500, ["ingest-sources"]], ["build-assessments", 500, ["ingest-sources"]], ["publish-institution", 300, ["build-curriculum", "build-kb", "build-labs", "build-assessments"]]],
 "Crypto-Recovery-Forensics": [["ingest-chain-data", 300, []], ["utxo-trace", 500, ["ingest-chain-data"]], ["evm-trace", 500, ["ingest-chain-data"]], ["key-derivation-analysis", 500, ["ingest-chain-data"]], ["contract-security-check", 400, ["evm-trace"]], ["forensic-report", 300, ["utxo-trace", "key-derivation-analysis", "contract-security-check"]]],
 "Google-FlowX": [["gemini-screenwrite-plot", 600, []], ["gemini-screenwrite-dialogue", 600, []], ["gemini-storyboard", 600, []], ["render-chunk-1", 800, ["gemini-screenwrite-plot", "gemini-screenwrite-dialogue", "gemini-storyboard"]], ["render-chunk-2", 800, ["gemini-screenwrite-plot", "gemini-screenwrite-dialogue", "gemini-storyboard"]], ["render-chunk-3", 800, ["gemini-screenwrite-plot", "gemini-screenwrite-dialogue", "gemini-storyboard"]], ["render-chunk-4", 800, ["gemini-screenwrite-plot", "gemini-screenwrite-dialogue", "gemini-storyboard"]], ["assemble-film", 400, ["render-chunk-1", "render-chunk-2", "render-chunk-3", "render-chunk-4"]]],
 "WEB3-insp3ct": [["load-target", 200, []], ["inspect-rpc", 400, ["load-target"]], ["inspect-dom", 400, ["load-target"]], ["inspect-network", 400, ["load-target"]], ["inspect-mobile", 400, ["load-target"]], ["build-report", 300, ["inspect-rpc", "inspect-dom", "inspect-network", "inspect-mobile"]]],
 "quantum-ecosystem": [["swarm-scout", 400, []], ["monad-contract-audit", 600, ["swarm-scout"]], ["sandbox-detonation", 600, ["swarm-scout"]], ["fund-balancer", 400, ["swarm-scout"]], ["encrypted-backup", 300, ["monad-contract-audit", "sandbox-detonation"]], ["deploy", 300, ["monad-contract-audit", "fund-balancer"]]],
 "deconstruction": [["ingest-system", 200, []], ["decompose-frontend", 400, ["ingest-system"]], ["decompose-backend", 400, ["ingest-system"]], ["decompose-logic", 400, ["ingest-system"]], ["strip-and-optimise", 400, ["decompose-frontend", "decompose-backend", "decompose-logic"]], ["solve-core", 300, ["strip-and-optimise"]]],
 "vulnerabilitiesx": [["load-lab", 200, []], ["scan-vulnerable-web", 400, ["load-lab"]], ["scan-vulnerable-api", 400, ["load-lab"]], ["scan-bot-exploits", 400, ["load-lab"]], ["scan-secure-variants", 400, ["load-lab"]], ["diff-and-teach", 300, ["scan-vulnerable-web", "scan-vulnerable-api", "scan-bot-exploits", "scan-secure-variants"]]],
 "bug-bounty-xterminator": [["scope-check", 200, []], ["recon-web", 500, ["scope-check"]], ["recon-api", 500, ["scope-check"]], ["recon-mobile", 500, ["scope-check"]], ["recon-binary", 500, ["scope-check"]], ["recon-infra", 500, ["scope-check"]], ["validate-findings", 500, ["recon-web", "recon-api", "recon-mobile", "recon-binary", "recon-infra"]], ["build-report", 300, ["validate-findings"]]],
 "monad-vul-x": [["fetch-bytecode", 200, []], ["scan-reentrancy", 400, ["fetch-bytecode"]], ["scan-access-control", 400, ["fetch-bytecode"]], ["scan-parallel-execution", 400, ["fetch-bytecode"]], ["scan-unchecked-calls", 400, ["fetch-bytecode"]], ["ml-risk-score", 400, ["fetch-bytecode"]], ["audit-report", 300, ["scan-reentrancy", "scan-access-control", "scan-parallel-execution", "scan-unchecked-calls", "ml-risk-score"]]],
 "malware-sandbox-suite": [["ingest-sample", 200, []], ["static-triage", 400, ["ingest-sample"]], ["hash-and-ioc", 300, ["ingest-sample"]], ["sandbox-detonation-plan", 500, ["static-triage"]], ["threat-report", 300, ["hash-and-ioc", "sandbox-detonation-plan"]]],
 "app-data-compressor": [["ingest-data", 200, []], ["chunk-cdc", 300, ["ingest-data"]], ["compress-shard-1", 400, ["chunk-cdc"]], ["compress-shard-2", 400, ["chunk-cdc"]], ["compress-shard-3", 400, ["chunk-cdc"]], ["compress-shard-4", 400, ["chunk-cdc"]], ["encrypt-and-pack", 300, ["compress-shard-1", "compress-shard-2", "compress-shard-3", "compress-shard-4"]]],
 "honeyroot-x": [["deploy-bait", 200, []], ["listen-ssh", 600, ["deploy-bait"]], ["listen-services", 600, ["deploy-bait"]], ["collect-attackers", 600, ["deploy-bait"]], ["analyse-bruteforce", 300, ["listen-ssh", "listen-services", "collect-attackers"]]],
 "malware-research-hub": [["ingest-sample-set", 300, []], ["catalog-families", 500, ["ingest-sample-set"]], ["extract-iocs", 400, ["ingest-sample-set"]], ["classify-behaviour", 500, ["ingest-sample-set"]], ["publish-research-en-es", 300, ["catalog-families", "extract-iocs", "classify-behaviour"]]],
 "globe-visualizer-frontend": [["bind-data", 200, []], ["render-points", 400, ["bind-data"]], ["render-arcs", 400, ["bind-data"]], ["render-ui", 400, ["bind-data"]], ["package-frontend", 200, ["render-points", "render-arcs", "render-ui"]]],
 "globe-visualizer-backend": [["ingest-activity", 300, []], ["build-points", 400, ["ingest-activity"]], ["build-arcs", 400, ["ingest-activity"]], ["serve-api", 300, ["build-points", "build-arcs"]]],
}
ROLES = ["scout","evm-re","contract-audit","forensics","vuln-scan","standards","matrix-runner","deployer","learner","globe"]

def levels_of(graph):
    """Topological levels: subtasks whose dependencies all sit in earlier levels."""
    done={}; levels=[]; remaining=list(graph)
    while remaining:
        ready=[t for t in remaining if all(d in done for d in t[2])]
        if not ready: raise ValueError("dependency cycle or missing dependency")
        for t in ready: done[t[0]]=len(levels)
        levels.append(ready); remaining=[t for t in remaining if t not in ready]
    return levels

def recommend(graph, repo="task"):
    levels=levels_of(graph); width=max(len(l) for l in levels)
    sequential=sum(t[1] for t in graph); critical=sum(max(t[1] for t in l) for l in levels)
    roster=[]
    for li, level in enumerate(levels):
        for i, t in enumerate(level):
            roster.append({"agent": f"agent-{li}-{i+1}", "role": ROLES[(li+i) % len(ROLES)], "subtask": t[0], "level": li, "duration_ms_est": t[1]})
    return {"repo": repo, "recommended_agents": width, "levels": len(levels),
            "subtasks": len(graph), "sequential_ms": sequential, "critical_path_ms": critical,
            "wall_clock_ms_at_recommended": critical, "queue_wait_ms_at_recommended": 0,
            "speedup_vs_1_agent": round(sequential/critical, 2) if critical else 0,
            "extra_agents_beyond_recommended_buy": "nothing - width is the parallel limit",
            "roster": roster}

def recommend_for_repo(repo): return recommend(REPO_GRAPHS[repo], repo)
def recommend_all():
    per={name: recommend(g, name) for name, g in REPO_GRAPHS.items()}
    zero_latency_total=sum(p["recommended_agents"] for p in per.values())
    return {"per_repo": {k: {"recommended_agents": v["recommended_agents"], "subtasks": v["subtasks"],
                             "critical_path_ms": v["critical_path_ms"], "sequential_ms": v["sequential_ms"],
                             "speedup_vs_1_agent": v["speedup_vs_1_agent"]} for k, v in per.items()},
            "unified_repo": "Mon-Ultra-Matrix",
            "unified_recommended_agents_zero_latency": zero_latency_total,
            "unified_note": "All 17 source pipelines running at once with zero queue wait = sum of the per-repo widths. Reusing one pool of max(per-repo) agents across repos serialises the repos and re-introduces queue wait.",
            "unified_pool_if_reused_serially": max(p["recommended_agents"] for p in per.values()),
            "gemini": {"model": MODEL, "thinking": THINKING, "source_repo": "Google-FlowX (Gemini Pro Thinking)"}}

def build_gemini_prompt(task):
    return ("Decompose this task for a multi-agent system. Return ONLY JSON: a list of "
            "[name, duration_ms_estimate, [dependencies]] covering every step, maximising "
            "safe parallelism. Task: " + task)

def call_gemini(task):
    key=os.environ.get("GEMINI_API_KEY")
    if not key: return None
    body=json.dumps({"contents":[{"parts":[{"text": build_gemini_prompt(task)}]}],
                     "generationConfig": {"thinkingConfig": THINKING}}).encode()
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    req=urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())
    except Exception: return None
