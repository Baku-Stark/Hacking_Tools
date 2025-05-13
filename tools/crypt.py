import base64
import hashlib

from services import Colors
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad


class Encryptor:
    """
    HackTools -> Encryptor | Cryptography: Base64, SHA3-256, AES
    """

    @staticmethod
    def base64_encode(text: str) -> str:
        encoded = base64.b64encode(text.encode()).decode()
        print(Colors.GREEN + "[+] Base64 Encoded: " + Colors.END, encoded)
        return encoded

    @staticmethod
    def sha3_256_hash(text: str) -> str:
        hashed = hashlib.sha3_256(text.encode()).hexdigest()
        print(Colors.GREEN + "[+] SHA3-256 Hash: " + Colors.END, hashed)
        return hashed

    @staticmethod
    def aes_encrypt(text: str, key: str) -> str:
        key_hash = hashlib.sha256(key.encode()).digest()  # 32 bytes
        cipher = AES.new(key_hash, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
        result = base64.b64encode(cipher.iv + ct_bytes).decode()

        print(Colors.GREEN + "[+] AES Encrypted (base64): " + Colors.END, result)
        return result
    
class Decryptor:
    """
    HackTools -> Decryptor | Decryption: Base64, AES
    """

    @staticmethod
    def base64_decode(b64_text: str) -> str:
        try:
            decoded = base64.b64decode(b64_text).decode()
            print(Colors.GREEN + "[+] Base64 Decoded:" + Colors.END, decoded)
            return decoded
        except Exception as e:
            print(Colors.RED + f"[!] Error decoding base64: {e}" + Colors.END)

    @staticmethod
    def aes_decrypt(b64_encrypted_text: str, key: str) -> str:
        try:
            raw = base64.b64decode(b64_encrypted_text)
            iv = raw[:16]
            ct = raw[16:]
            key_hash = hashlib.sha256(key.encode()).digest()
            cipher = AES.new(key_hash, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(ct), AES.block_size).decode()
            print(Colors.GREEN + "[+] AES Decrypted:" + Colors.END, decrypted)
            return decrypted
        except Exception as e:
            print(Colors.RED + f"[!] AES Decryption error: {e}" + Colors.END)