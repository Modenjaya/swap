import base64
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt(self, data: str) -> str:
        token = self.cipher.encrypt(data.encode())
        return token.decode()

    def decrypt(self, token: str) -> str:
        data = self.cipher.decrypt(token.encode())
        return data.decode()

def generate_key() -> bytes:
    return Fernet.generate_key()
