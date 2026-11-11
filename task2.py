import sqlite3
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class SecureCloudAuthSystem:
    def __init__(self, db_name="secure_cloud.db"):
        self.db_name = db_name
        self.encryption_key = os.urandom(32)
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                encrypted_credentials TEXT NOT NULL,
                iv TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def _encrypt_data(self, plaintext: str) -> tuple:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padding_length = 16 - (len(plaintext) % 16)
        padded_text = plaintext + (chr(padding_length) * padding_length)
        ciphertext = encryptor.update(padded_text.encode('utf-8')) + encryptor.finalize()
        return base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(iv).decode('utf-8')

    def register_user(self, username: str, sensitive_info: str):
        enc_data, iv = self._encrypt_data(sensitive_info)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, encrypted_credentials, iv) VALUES (?, ?, ?)", 
                           (username, enc_data, iv))
            conn.commit()
            print(f"[SECURE] User '{username}' registered with AES-256 encryption.")
        except sqlite3.IntegrityError:
            print(f"[WARNING] Username '{username}' already exists.")
        finally:
            conn.close()

    def secure_login_query(self, username_input: str, password_input: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = "SELECT id, username, encrypted_credentials FROM users WHERE username = ?"
        cursor.execute(query, (username_input,))
        user_record = cursor.fetchone()
        conn.close()

        if user_record:
            print(f"[ACCESS GRANTED] Safe lookup successful for user ID: {user_record[0]}")
            return True
        else:
            print("[ACCESS DENIED] Invalid credentials or injection vector blocked.")
            return False

if __name__ == "__main__":
    cloud_auth = SecureCloudAuthSystem()
    cloud_auth.register_user("admin_cloud", "SecretApiKey@12345")

    print("\n--- Testing Potential SQL Injection Attack Vector ---")
    malicious_payload = "admin_cloud' OR '1'='1"
    cloud_auth.secure_login_query(malicious_payload, "arbitrary_password")