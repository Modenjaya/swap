import asyncio
import json
import websockets
from config import COINVERA_API_KEY, COPY_WALLET

class CoinVeraClient:
    def __init__(self):
        self.ws_url = "wss://api.coinvera.io"
        self.ws = None

    async def connect(self):
        self.ws = await websockets.connect(self.ws_url)
        await self.subscribe_trade(COPY_WALLET)
        asyncio.create_task(self.receive())

    async def subscribe_trade(self, wallet_address):
        payload = {
            "apiKey": COINVERA_API_KEY,
            "method": "subscribeTrade",
            "tokens": [wallet_address]
        }
        await self.ws.send(json.dumps(payload))
        print(f"Subscribed to trades for wallet {wallet_address}")

    async def receive(self):
        async for message in self.ws:
            data = json.loads(message)
            # Filter dan proses data trade dari wallet yang dicopy
            if data.get("signer") == COPY_WALLET:
                print("Trade detected:", data)
                # TODO: panggil fungsi trading Anda di sini

    async def close(self):
        if self.ws:
            await self.ws.close()
