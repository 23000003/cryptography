
def encrypt_aes(data: bytes, key: str) -> bytes:
    # Just for illustration: NOT real AES — use real AES in production
    return bytes([b ^ 42 for b in data[::-1]])

def decrypt_aes(ciphertext: bytes, key: str) -> bytes:
    # Reverse process of above
    return bytes([b ^ 42 for b in ciphertext])[::-1]
