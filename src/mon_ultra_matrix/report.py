"""Report builder: successes only - all failures are removed before reporting."""
from .monad_stats import summary
def build_report(registry_summary, matrix=None, contract=None):
    lines=["# Mon-Ultra-Matrix Report","",summary(),"",
           f"Projects kept: {registry_summary.get('successful',0)} successful. All failures removed."]
    if matrix: lines+=["",f"Matrix: {matrix['successful']} successful cells kept, {matrix.get('removed',0)} failed cells removed."]
    if contract: lines+=["",f"Contract: {contract}"]
    return "\n".join(lines)
