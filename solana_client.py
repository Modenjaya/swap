import asyncio
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
import base58
import json

class SolanaClient:
    def __init__(self, rpc_url: str):
        self.client = AsyncClient(rpc_url)

    async def get_balance(self, pubkey: str) -> float:
        resp = await self.client.get_balance(pubkey)
        lamports = resp['result']['value'] if resp['result'] else 0
        return lamports / 1_000_000_000  # Convert lamports to SOL

    def keypair_from_private_key(self, private_key_str: str) -> Keypair:
        # private_key_str bisa format JSON array atau base58
        try:
            if private_key_str.startswith('['):
                key_bytes = bytes(json.loads(private_key_str))
            else:
                key_bytes = base58.b58decode(private_key_str)
            return Keypair.from_secret_key(key_bytes)
        except Exception as e:
            raise ValueError("Invalid private key format") from e

    async def close(self):
        await self.client.close()
