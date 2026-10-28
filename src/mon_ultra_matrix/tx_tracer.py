"""Transaction graph tracing - from Crypto-Recovery-Forensics."""
class TxGraph:
    def __init__(self): self.edges=[]
    def add(self, frm, to, value=0, txhash=""): self.edges.append({"from":frm,"to":to,"value":value,"hash":txhash})
    def counterparties(self, addr): return sorted({e["to"] for e in self.edges if e["from"]==addr} | {e["from"] for e in self.edges if e["to"]==addr})
    def total_out(self, addr): return sum(e["value"] for e in self.edges if e["from"]==addr)
    def total_in(self, addr): return sum(e["value"] for e in self.edges if e["to"]==addr)
    def hops(self, start, max_hops=3):
        seen={start}; frontier={start}
        for _ in range(max_hops):
            nxt={e["to"] for e in self.edges if e["from"] in frontier} - seen
            seen|=nxt; frontier=nxt
            if not frontier: break
        return sorted(seen-{start})
def parse_transfer_log(topics, data=""):
    # ERC20 Transfer: topic0 signature, topic1 from, topic2 to
    if len(topics)<3: return None
    return {"from":"0x"+topics[1][-40:], "to":"0x"+topics[2][-40:], "raw_data": data}
