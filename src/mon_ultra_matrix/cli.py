"""CLI: python -m mon_ultra_matrix <cmd>"""
import argparse, json, sys
from .monad_stats import summary, TOP_PROTOCOLS, TOKENOMICS
from .evm_re import analyze
from .abi_re import identify_all, is_erc20
from .forensics import risk_flags
from .standards import audit, score
from .experiment import ProjectRegistry, pipeline
from .matrix_runner import run_matrix
from .learner import reason
from .deployer import deploy_plan
def main(argv=None):
    p=argparse.ArgumentParser(prog="mon-ultra-matrix"); sub=p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("stats")
    sub.add_parser("images")
    ag=sub.add_parser("agents"); ag.add_argument("--repo", default=None)
    a=sub.add_parser("analyze"); a.add_argument("bytecode")
    a=sub.add_parser("experiment"); a.add_argument("name"); a.add_argument("--fail", action="store_true"); a.add_argument("--registry", default="projects_registry.jsonl")
    sub.add_parser("registry"); 
    r=sub.add_parser("reason"); r.add_argument("query")
    args=p.parse_args(argv)
    if args.cmd=="agents":
        from .gemini_planner import recommend_for_repo, recommend_all
        print(json.dumps(recommend_for_repo(args.repo) if args.repo else recommend_all(), indent=2))
    elif args.cmd=="images":
        from .docker_images import IMAGES, total_pulls
        print(json.dumps({"images": IMAGES, "total_pulls_snapshot": total_pulls()}, indent=2))
    elif args.cmd=="stats": print(summary()); print(json.dumps({"protocols":TOP_PROTOCOLS,"tokenomics":{k:str(v) for k,v in TOKENOMICS.items()}}, indent=2))
    elif args.cmd=="analyze":
        an=analyze(args.bytecode); print(json.dumps({"analysis":an,"signatures":identify_all(an["selectors"]),"is_erc20":is_erc20(an["selectors"]),"risk_flags":risk_flags(an),"standards_score":score(an),"standards":audit(an)}, indent=2))
    elif args.cmd=="experiment":
        reg=ProjectRegistry(args.registry)
        fn=(lambda: 1/0) if args.fail else (lambda: "ok")
        print(json.dumps(pipeline(reg, args.name, fn), indent=2)); print(json.dumps(reg.summary(), indent=2))
    elif args.cmd=="registry": print(json.dumps(ProjectRegistry().summary(), indent=2))
    elif args.cmd=="reason": print(json.dumps(reason(args.query), indent=2))
    return 0
if __name__=="__main__": sys.exit(main())
