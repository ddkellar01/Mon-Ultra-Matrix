# Curriculum - learn Monad by reverse engineering it

1. EVM basics on Monad: disassemble a dispatcher, extract PUSH4 selectors (`evm_re`, `abi_re`).
2. Token RE: prove/disprove ERC20 from selectors alone; map a real MON-ecosystem token.
3. Proxy RE: find DELEGATECALL, locate the implementation, repeat step 1 there.
4. Protocol RE: fingerprint Aave / Kuru / Uniswap against `protocol_re`.
5. Forensics: build a TxGraph, trace counterparties and hop distance (`tx_tracer`).
6. Standards: run the ISO/IEC-flavoured audit, defend every failed control (`standards`).
7. Experiments: run one deliberate failure and one success through the pipeline - confirm the failure is removed and only the success is kept and gets a deploy plan.
8. Matrix: run all checks x all your lab contracts; failed cells are removed - work only from the successful cells that remain.
9. Risk: model the Nov 24, 2026 unlock against a MON position.
10. Ship: testnet deploy plan only after the matrix is green.
