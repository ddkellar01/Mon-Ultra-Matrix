"""Deployer: testnet-first gate. FAILED projects are removed, never deployed."""
def deploy_plan(entry, network="monad-testnet"):
    if entry.get("status")!="SUCCESS": return {"deploy":False,"reason":"FAILED projects are removed, never deployed","entry":entry.get("name")}
    return {"deploy":True,"network":network,"steps":["verify bytecode hash","deploy to testnet","run matrix checks","promote to mainnet only after testnet matrix is green"]}
