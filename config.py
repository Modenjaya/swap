import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
JUPITER_API_URL = "https://quote-api.jup.ag/v6"
DATABASE_PATH = "bot_database.db"
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")  # Untuk enkripsi private key
