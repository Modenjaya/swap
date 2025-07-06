import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from database import DatabaseManager
from solana_client import SolanaClient
from jupiter_client import JupiterClient
from trading_engine import TradingEngine
from security import SecurityManager
import config

class TelegramBot:
    def __init__(self):
        self.db = DatabaseManager(config.DATABASE_PATH)
        self.security = SecurityManager(config.ENCRYPTION_KEY.encode())
        self.solana_client = SolanaClient(config.SOLANA_RPC_URL)
        self.jupiter_client = JupiterClient(config.JUPITER_API_URL)
        self.trading_engine = TradingEngine(self.solana_client, self.jupiter_client)
        self.app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("wallet", self.wallet))
        self.app.add_handler(CommandHandler("balance", self.balance))
        self.app.add_handler(CommandHandler("buy", self.buy))
        # Tambah handler lain sesuai kebutuhan

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        self.db.add_user(user.id, user.username, user.first_name, user.last_name)
        await update.message.reply_text(
            f"Selamat datang, {user.first_name}! Gunakan /wallet untuk setup wallet Anda."
        )

    async def wallet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        wallet = self.db.get_wallet(user_id)
        if wallet:
            await update.message.reply_text(f"Wallet Anda: {wallet['wallet_address']}")
        else:
            await update.message.reply_text("Anda belum punya wallet. Kirim private key Anda untuk import.")

    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        wallet = self.db.get_wallet(user_id)
        if not wallet:
            await update.message.reply_text("Wallet tidak ditemukan. Gunakan /wallet untuk setup.")
            return
        balance = await self.solana_client.get_balance(wallet['wallet_address'])
        await update.message.reply_text(f"Balance wallet Anda: {balance:.6f} SOL")

    async def buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        wallet = self.db.get_wallet(user_id)
        if not wallet:
            await update.message.reply_text("Wallet tidak ditemukan. Gunakan /wallet untuk setup.")
            return
        if len(context.args) < 2:
            await update.message.reply_text("Gunakan format: /buy <token_mint> <amount_sol>")
            return
        token_mint = context.args[0]
        try:
            amount_sol = float(context.args[1])
        except ValueError:
            await update.message.reply_text("Amount harus berupa angka.")
            return

        private_key_enc = wallet['encrypted_private_key']
        private_key = self.security.decrypt(private_key_enc)
        wallet_keypair = self.solana_client.keypair_from_private_key(private_key)

        signature = await self.trading_engine.buy_token(wallet_keypair, token_mint, amount_sol)
        if signature:
            await update.message.reply_text(f"Buy order berhasil! Tx signature: {signature}")
        else:
            await update.message.reply_text("Gagal melakukan buy order.")

    async def run(self):
    await self.app.initialize()
    await self.app.start()
    print("Bot started...")
    await self.app.run_polling()  # Ini sudah blocking dan mengelola lifecycle
    # atau jika ingin manual:
    # await self.app.updater.start_polling()
    # await self.app.idle()  # Ganti idle dari updater ke app
    await self.app.stop()

