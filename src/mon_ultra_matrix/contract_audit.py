"""Monad-Vul-X - Monad smart-contract audit heuristics on top of evm_re.
Heuristics, not proof: every hit is a lead for manual RE, especially under Monad parallel execution.
"""
from .evm_re import disassemble
def audit_bytecode(hexcode):
    ops=[o["op"] for o in disassemble(hexcode)]; findings=[]
    # Reentrancy lead: external CALL seen before a later SSTORE in linear order
    if "CALL" in ops and "SSTORE" in ops and ops.index("CALL") < len(ops)-1-ops[::-1].index("SSTORE"):
        findings.append({"check":"reentrancy-lead","detail":"CALL occurs before a later SSTORE - verify checks-effects-interactions"})
    if "DELEGATECALL" in ops: findings.append({"check":"delegatecall","detail":"Upgrade/proxy surface - audit implementation + admin"})
    if "SELFDESTRUCT" in ops: findings.append({"check":"selfdestruct","detail":"Contract can be destroyed - verify gating"})
    if "CALL" in ops: findings.append({"check":"unchecked-call-lead","detail":"Verify every CALL return value is checked"})
    return findings
def monad_parallel_notes():
    return ["Monad executes in parallel: do not assume sequential ordering between independent txs.",
            "Check shared-state writes for ordering races that sequential-EVM audits would miss.",
            "0.8s finality is fast - front-running windows are short but automation is faster."]
