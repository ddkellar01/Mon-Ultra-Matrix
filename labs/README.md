# Labs

Educational, local-only samples for the RE pipeline:

- A sample dispatcher bytecode is embedded in the tests (`608060405234...`) - disassemble it with `analyze`.
- Build your own sample: compile any small Solidity contract for Monad testnet, paste its runtime bytecode into `analyze`, and run the full matrix (selectors, ERC20 check, standards audit, risk flags, protocol fingerprint).

Never point the forensics / tracing tools at wallets or contracts you do not own or have permission to study. This repo is for education and self-custody research, matching Crypto-Recovery-Forensics' scope.
