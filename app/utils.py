import base64
from cryptography.fernet import Fernet

class ObfuscatedSecret:
    def __init__(self, secret):
        key = Fernet.generate_key()
        self.key = key
        f = Fernet(key)
        self.encrypted = f.encrypt(secret.encode())

    def __str__(self):
        return "ObfuscatedSecret"

    def get(self):
        f = Fernet(self.key)
        return f.decrypt(self.encrypted).decode()