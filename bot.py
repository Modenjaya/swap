from telegram_bot import TelegramBot
import asyncio

async def main():
    bot = TelegramBot()
    await bot.run()  # Pastikan metode run mengelola event loop dengan benar

if __name__ == "__main__":
    asyncio.run(main())
