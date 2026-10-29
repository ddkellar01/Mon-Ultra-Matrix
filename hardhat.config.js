require("@dotenvx/dotenvx").config(); // or require('dotenv').config();
const MAINNET_RPC_URL = process.env.MAINNET_RPC_URL || "";
const TESTNET_RPC_URL = process.env.TESTNET_RPC_URL || "";
const PRIVATE_KEY = process.env.PRIVATE_KEY || "";

module.exports = {
  solidity: "0.8.24",
  networks: {
    mainnet: {
      url: MAINNET_RPC_URL,
      accounts: [PRIVATE_KEY],
    },
    sepolia: {
      url: TESTNET_RPC_URL,
      accounts: [PRIVATE_KEY],
    },
  },
};
