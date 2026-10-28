"""Monad network facts as supplied in Darion's 2026-10-27 research video.
Sources named in the video: DefiLlama, CoinGecko, CoinMarketCap, MetaMask, Kraken, Ledger.
Figures are snapshots, not live queries - re-check before acting on price/TVL.
"""
MONAD = {
    "name": "Monad", "token": "MON", "chain_type": "EVM-compatible Layer 1",
    "mainnet_launch": "2025-11-24", "throughput_tps": 10000,
    "block_time_s": 0.4, "finality_s": 0.8,
    "consensus": "MonadBFT", "networking": "RaptorCast", "storage": "MonadDb",
    "execution": "parallel execution, pipelined block production, full EVM bytecode + RPC compatibility",
    "gas": "near-zero fees (per video sources)",
}
SNAPSHOT = {
    "transactions": "~989M", "active_wallets": "9M+", "apps_live": "143+",
    "defi_tvl_usd": 975_000_000, "defi_tvl_alt_usd": 1_032_443_020,
    "tvl_note": "DefiLlama $974.7M vs CoinGecko $1.03B in the same video - platform variance, not an error",
    "volume_24h_usd": 40_942_993,
}
TOKENOMICS = {
    "total_supply": 100_000_000_000, "supply_model": "fixed, dual-issuance + fee-burn debated in sources",
    "circulating": 11_830_000_000, "price_usd_range": (0.021, 0.023),
    "market_cap_usd": 266_940_000, "volume_24h_usd": 20_190_000, "ath_usd": 0.049,
    "cliff_unlock": {"date": "2026-11-24", "amount": 16_600_000_000, "holders": "team and investors",
                     "note": "one year post-mainnet; high annual inflation / supply-expansion risk flagged by analysts in video"},
    "uses": ["gas fees", "staking for PoS security", "governance"],
}
TOP_PROTOCOLS = {
    "lending": [{"name": "Aave", "note": "Monad market became its 3rd-largest fee generator in 46 days; $321M TVL at day 46 (2026-09-17 in video), 5th of 21 Aave deployments by TVL, 3rd by weekly fees, 2nd-highest fees overall in that window"}],
    "dex_by_volume": ["Kuru", "Uniswap V4", "Uniswap V3", "PancakeSwap V3", "Balancer V3", "Curve"],
    "trending_coins": ["WETH", "WMON", "EURW", "WNAUSD", "WNUSDT0", "APRMON", "FLING", "EMO"],
}
COMPARE = {"Base TVL (video)": "$6.0B", "Monad TVL (video)": "$974.7M"}
TRACKING = ["DefiLlama (TVL/fees/revenue)", "CoinGecko (price/TVL)", "Moralis + Blockworks Analytics (tx / contract data via MonadStats)"]
def summary():
    return f"{MONAD['name']} ({MONAD['token']}): {MONAD['throughput_tps']} TPS, {MONAD['block_time_s']}s blocks, {MONAD['finality_s']}s finality, TVL ${SNAPSHOT['defi_tvl_usd']:,}, {SNAPSHOT['active_wallets']} wallets, {SNAPSHOT['apps_live']} apps"
