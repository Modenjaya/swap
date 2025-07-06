from solders.keypair import Keypair
from solana_client import SolanaClient
from jupiter_client import JupiterClient

class TradingEngine:
    def __init__(self, solana_client: SolanaClient, jupiter_client: JupiterClient):
        self.solana_client = solana_client
        self.jupiter_client = jupiter_client

    async def buy_token(self, wallet_keypair: Keypair, token_mint: str, sol_amount: float, slippage_bps: int = 50):
        # Konversi SOL ke lamports
        amount = int(sol_amount * 1_000_000_000)
        sol_mint = "So11111111111111111111111111111111111111112"
        quote = await self.jupiter_client.get_quote(sol_mint, token_mint, amount, slippage_bps)
        if not quote or not quote.get("data"):
            return None
        # TODO: Implement swap transaction signing & sending
        # Placeholder return
        return "dummy_signature"

    async def sell_token(self, wallet_keypair: Keypair, token_mint: str, token_amount: float, slippage_bps: int = 50):
        # TODO: Implement sell logic mirip buy_token
        return "dummy_signature"
