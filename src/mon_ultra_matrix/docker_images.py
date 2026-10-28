"""Docker Hub merge registry - the 10 credkellar images merged 2026-10-27.
All verified live/active on Docker Hub on 2026-10-27 (pull counts are that day's snapshot).
"""
IMAGES = {
 "deconstruction": {"hub": "credkellar/deconstruction", "pulls_snapshot": 668, "role": "Deconstruct contracts/systems to core logic, strip fluff", "module": "deconstruction"},
 "vulnerabilitiesx": {"hub": "credkellar/vulnerabilitiesx", "pulls_snapshot": 751, "role": "Vulnerable-vs-secure lab: OWASP web/API risks, bot exploits", "module": "vuln_scan"},
 "bug-bounty-xterminator": {"hub": "credkellar/bug-bounty-xterminator", "pulls_snapshot": 1852, "role": "Autonomous bounty lifecycle: scope, triage, report", "module": "bounty"},
 "monad-vul-x": {"hub": "credkellar/monad-vul-x", "pulls_snapshot": 424, "role": "AI/ML security testing for smart contracts on fast Monad networks", "module": "contract_audit"},
 "malware-sandbox-suite": {"hub": "credkellar/malware-sandbox-suite", "pulls_snapshot": 227, "role": "Scalable threat-analysis / sandbox environment (static triage here)", "module": "malware_sandbox"},
 "app-data-compressor": {"hub": "credkellar/app-data-compressor", "pulls_snapshot": 251, "role": "Content-defined chunking + compression engine", "module": "compressor"},
 "honeyroot-x": {"hub": "credkellar/honeyroot-x", "pulls_snapshot": 266, "role": "SSH honeypot, root-access bait, brute-force logging", "module": "honeypot"},
 "malware-research-hub": {"hub": "credkellar/malware-research-hub", "pulls_snapshot": 108, "role": "Malware research catalog: families, samples, IOCs", "module": "malware_research"},
 "globe-visualizer-frontend": {"hub": "credkellar/globe-visualizer-frontend", "pulls_snapshot": 1009, "role": "Globe visualisation front-end payload", "module": "globe"},
 "globe-visualizer-backend": {"hub": "credkellar/globe-visualizer-backend", "pulls_snapshot": 1143, "role": "Globe visualisation back-end data service", "module": "globe"},
}
def total_pulls(): return sum(v["pulls_snapshot"] for v in IMAGES.values())
def pull_commands(): return [f"docker pull credkellar/{k}" for k in IMAGES]
