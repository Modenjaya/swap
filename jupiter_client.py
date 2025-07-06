import aiohttp

class JupiterClient:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.session = aiohttp.ClientSession()

    async def get_quote(self, input_mint: str, output_mint: str, amount: int, slippage_bps: int = 50):
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount,
            "slippageBps": slippage_bps,
        }
        async with self.session.get(f"{self.api_url}/quote", params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            return None

    async def close(self):
        await self.session.close()
