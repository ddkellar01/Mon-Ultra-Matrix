"""ABI / selector reverse engineering against a small known-signature DB."""
KNOWN = {
 "0xa9059cbb":"transfer(address,uint256)","0x095ea7b3":"approve(address,uint256)",
 "0x23b872dd":"transferFrom(address,address,uint256)","0x70a08231":"balanceOf(address)",
 "0x18160ddd":"totalSupply()","0x06fdde03":"name()","0x95d89b41":"symbol()",
 "0x313ce567":"decimals()","0xdd62ed3e":"allowance(address,address)",
 "0x8da5cb5b":"owner()","0x715018a6":"renounceOwnership()","0xf2fde38b":"transferOwnership(address)",
 "0x7ff36ab5":"swapExactETHForTokens(uint256,address[],address,uint256)",
 "0x38ed1739":"swapExactTokensForTokens(uint256,uint256,address[],address,uint256)",
 "0x02751cec":"exit()","0xe9e05c42":"deposit(uint256)"}
def identify(selector): return KNOWN.get(selector.lower(), "unknown")
def identify_all(selectors): return {s: identify(s) for s in selectors}
def is_erc20(selectors):
    need={"0xa9059cbb","0x23b872dd","0x70a08231","0x18160ddd"}; return need.issubset({s.lower() for s in selectors})
