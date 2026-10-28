# Merge Map - Mon-Ultra-Matrix

Perfect merge of the 7 repos named in the 2026-10-27 video, plus the Monad research in that video. Nothing dropped: every source repo maps to a living module.

| Source repo (ddkellar01) | What it contributed | Where it lives here |
|---|---|---|
| Autonomous-Tech-Infrastructure-Platform | Scout top repos, sandbox-test inventions, CI/CD deploy, continuous learning | `scout.py`, `sandbox.py`, `deployer.py`, CI workflow |
| ISO-IECx | Crawl/study ISO/IEC standards, audit pipelines | `standards.py` (control audit + score) |
| IvyTech-Nexus-Omni-Institution | Omni-institution learning layer | `docs/CURRICULUM.md`, `learner.py` KB |
| Crypto-Recovery-Forensics | EVM/UTXO tracing, key/ledger transparency, contract security research | `tx_tracer.py`, `forensics.py` |
| Google-FlowX | 1,000-run matrix testing, multi-agent orchestration | `matrix_runner.py` (every check x every target; failed cells removed, successful cells only) |
| WEB3-insp3ct | Inspect/debug live Web3 RPC, DOM/network inspection | `rpc_inspector.py`, `monad_client.py` |
| quantum-ecosystem | Monad contract auditing, swarm scout, sandbox detonation, encrypted-backup ethos | `evm_re.py` + `abi_re.py` auditing, `scout.py`, `sandbox.py` |

Plus, native to this repo:
- `monad_stats.py` - Monad architecture, snapshot stats, tokenomics and the Nov 24, 2026 cliff unlock, exactly as supplied in the video (with the DefiLlama-vs-CoinGecko TVL variance noted, not hidden).
- `protocol_re.py` - fingerprints for Aave, Kuru, Uniswap V4/V3, PancakeSwap V3, Balancer V3, Curve.
- `experiment.py` - the operating rule as updated by Darion 2026-10-27: **successful projects only - remove all failures.** Failures are never written to the registry, and `remove_failures()` purges any already on disk; only successes are deployable. This supersedes the keep-all-failures rule in the founding video.
- `learner.py` - SML (kNN) + NNL (from-scratch MLP) + LLM reasoner (offline KB, Gemini if a key is set), carried from shannon-re-lab / bug-bounty-re.

Deliberately NOT merged: live trading / fund movement. Mon-Ultra-Matrix is a research and RE lab - analysis, experiments and testnet deployment plans only.

## Second merge - 10 Docker Hub images (2026-10-27)

All verified live/active on Docker Hub on 2026-10-27; pull counts are that day's snapshot (6,699 total).

| Docker Hub image (credkellar) | Pulls | What it contributed | Where it lives here |
|---|---|---|---|
| deconstruction | 668 | Strip fluff, optimise core logic | `deconstruction.py` |
| vulnerabilitiesx | 751 | Vulnerable-vs-secure lab, OWASP web/API | `vuln_scan.py` |
| bug-bounty-xterminator | 1,852 | Autonomous bounty lifecycle (LLM-x/ML-x/Gemini swarm) | `bounty.py` |
| monad-vul-x | 424 | AI/ML contract security testing for Monad | `contract_audit.py` |
| malware-sandbox-suite | 227 | Threat-analysis sandbox environment | `malware_sandbox.py` (static triage only - never executes samples) |
| app-data-compressor | 251 | CDC chunking + compression (KMS/zstd in the image; stdlib zlib port here) | `compressor.py` |
| honeyroot-x | 266 | SSH honeypot, root-access bait, brute-force logs | `honeypot.py` |
| malware-research-hub | 108 | Malware family/sample research catalog | `malware_research.py` |
| globe-visualizer-frontend | 1,009 | Globe visualisation front-end | `globe.py` (payload consumer + render snippet) |
| globe-visualizer-backend | 1,143 | Globe visualisation back-end | `globe.py` (points/arcs payload builder) |

Registry of record: `docker_images.py`. Runnable stack: `docker-compose.ultra.yml` (all services behind the `ultra` profile).

## Agent planning - Gemini Pro Thinking (Extended), from Google-FlowX

`gemini_planner.py` takes Google-FlowX's pattern (Gemini Pro Thinking + multi-agent parallel work) and applies it per repo and to the unified repo. Each source repo gets a subtask graph; the recommended agent count is the graph's widest parallel level - the point where queue wait hits zero and wall-clock equals the critical path. `python -m mon_ultra_matrix agents` prints every per-repo recommendation plus the unified Mon-Ultra-Matrix total; `--repo <name>` prints one repo's full roster. With `GEMINI_API_KEY` set, `call_gemini()` asks Gemini Pro (thinkingBudget 32768) to decompose new tasks into the same graph format; offline, the deterministic planner is authoritative.
