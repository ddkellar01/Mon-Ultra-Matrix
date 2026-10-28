# Monad Architecture (from the 2026-10-27 research video)

- Layer 1, launched November 24, 2025. Full EVM bytecode + RPC compatibility - existing Solidity deploys unmodified.
- 10,000 TPS, ~0.4s block times, ~0.8s finality, near-zero gas.
- Core: parallel transaction execution, pipelined block production, MonadBFT consensus, RaptorCast networking, MonadDb storage.
- Why it matters for RE: parallel execution + pipelining change ordering / MEV assumptions vs sequential Ethereum - the matrix runner exists to test those assumptions contract by contract.
- Snapshot (video, Oct 2026 sources): ~989M transactions, 9M+ active wallets, 143+ apps live, DeFi TVL $974.7M (DefiLlama) / $1.03B (CoinGecko).
- Token: MON, 100B fixed supply, ~11.83B circulating, ~$0.021-$0.023, ~$266.9M market cap, ATH $0.049.
- Watch date: **November 24, 2026** - cliff unlock of ~16.6B MON to team and investors (1 year post-mainnet).
- Top protocols: Aave (lending), Kuru (DEX volume leader), Uniswap V4/V3, PancakeSwap V3, Balancer V3, Curve.
