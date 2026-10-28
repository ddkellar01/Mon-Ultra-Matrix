"""Minimal Monad JSON-RPC client (stdlib urllib). Offline-safe: errors return None, never raise."""
import json, urllib.request
DEFAULT_RPCS = ["https://rpc.monad.xyz", "https://rpc1.monad.xyz", "https://rpc-mainnet.monadinfra.com"]
class MonadClient:
    def __init__(self, rpc=DEFAULT_RPCS[0], timeout=10): self.rpc=rpc; self.timeout=timeout
    def call(self, method, params=None):
        body=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params or []}).encode()
        req=urllib.request.Request(self.rpc, data=body, headers={"Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r: return json.loads(r.read()).get("result")
        except Exception: return None
    def block_number(self):
        v=self.call("eth_blockNumber"); return int(v,16) if v else None
    def get_code(self, address): return self.call("eth_getCode",[address,"latest"])
    def get_balance(self, address):
        v=self.call("eth_getBalance",[address,"latest"]); return int(v,16) if v else None
    def chain_id(self):
        v=self.call("eth_chainId"); return int(v,16) if v else None
