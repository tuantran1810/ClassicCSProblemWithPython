from secrets import token_bytes
from typing import Tuple

def randomKey(length: int) -> int:
    tb: bytes = token_bytes(length)
    return int.from_bytes(tb, "big")

def encrypt(original: str) -> Tuple[int, int]:
    original_bytes: bytes = original.encode()
    dummy: int = randomKey(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = dummy ^ original_key
    return dummy, encrypted

def decrypt(key1: int, key2: int) -> str:
    decrypted = key1 ^ key2
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")
    return temp.decode()

if __name__ == "__main__":
    key1, key2 = encrypt("One Time Pad!")
    result: str = decrypt(key1, key2)
    print(result)
