"""RPC / Web3 inspection - merged from WEB3-insp3ct."""
from .monad_client import MonadClient, DEFAULT_RPCS
def inspect_endpoint(rpc):
    c=MonadClient(rpc); cid=c.chain_id(); blk=c.block_number()
    return {"rpc": rpc, "reachable": cid is not None, "chain_id": cid, "block_number": blk}
def inspect_all(rpcs=DEFAULT_RPCS): return [inspect_endpoint(r) for r in rpcs]
def inspect_contract(client, address):
    code=client.get_code(address)
    if not code or code=="0x": return {"address":address,"is_contract":False}
    from .evm_re import analyze; from .forensics import risk_flags
    a=analyze(code); return {"address":address,"is_contract":True,"analysis":a,"risk_flags":risk_flags(a)}
