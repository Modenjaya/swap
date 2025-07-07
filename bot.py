import asyncio
from telegram_bot import TelegramBot
from coinvera_client import CoinVeraClient

async def main():
    # Start Telegram bot (non-blocking)
    telegram_bot = TelegramBot()
    telegram_task = asyncio.to_thread(telegram_bot.run)

    # Start CoinVera WebSocket client
    coinvera_client = CoinVeraClient()
    await coinvera_client.connect()

    # Jalankan kedua task secara paralel
    await asyncio.gather(telegram_task)

if __name__ == "__main__":
    asyncio.run(main())
