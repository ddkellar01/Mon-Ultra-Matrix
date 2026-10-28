"""Protocol fingerprints for the top Monad protocols named in the video."""
PROTOCOLS = {
 "aave": {"kind":"lending","markers":["deposit","borrow","repay","withdraw"," liquidation".strip()],"note":"Top lending market on Monad per video"},
 "kuru": {"kind":"dex","markers":["placeOrder","cancelOrder"],"note":"Leads Monad DEX volume per video"},
 "uniswap_v4": {"kind":"dex","markers":["PoolManager","unlock","swap"],"note":"Uniswap V4 on Monad"},
 "uniswap_v3": {"kind":"dex","markers":["exactInputSingle","multicall"],"note":"Uniswap V3 on Monad"},
 "pancakeswap_v3": {"kind":"dex","markers":["exactInputSingle"],"note":"PancakeSwap V3 on Monad"},
 "balancer_v3": {"kind":"dex","markers":["Vault","swap"],"note":"Balancer V3 on Monad"},
 "curve": {"kind":"dex","markers":["exchange","get_virtual_price"],"note":"Curve on Monad"},
}
def fingerprint(function_names):
    names=" ".join(function_names).lower(); hits=[]
    for name,p in PROTOCOLS.items():
        if any(m.lower() in names for m in p["markers"]): hits.append(name)
    return hits
