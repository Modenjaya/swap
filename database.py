import sqlite3
from typing import Optional

class DatabaseManager:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallets (
                user_id INTEGER PRIMARY KEY,
                wallet_address TEXT,
                encrypted_private_key TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, user_id: int, username: str, first_name: str, last_name: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        self.conn.commit()

    def save_wallet(self, user_id: int, wallet_address: str, encrypted_private_key: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO wallets (user_id, wallet_address, encrypted_private_key)
            VALUES (?, ?, ?)
        ''', (user_id, wallet_address, encrypted_private_key))
        self.conn.commit()

    def get_wallet(self, user_id: int) -> Optional[dict]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT wallet_address, encrypted_private_key FROM wallets WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            return {"wallet_address": row[0], "encrypted_private_key": row[1]}
        return None
