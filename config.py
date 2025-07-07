import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
COINVERA_API_KEY = os.getenv("COINVERA_API_KEY")  # API key CoinVera
COPY_WALLET = os.getenv("COPY_WALLET")            # Wallet yang ingin dicopy
