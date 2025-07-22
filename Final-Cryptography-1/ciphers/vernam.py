def vernam_encrypt(input_bytes: bytes, key: str) -> bytes:
    key_bytes = key.encode('utf-8')
    key_len = len(key_bytes)
    output = bytearray(len(input_bytes))
    for i in range(len(input_bytes)):
        output[i] = input_bytes[i] ^ key_bytes[i % key_len]
    return bytes(output)

def vernam_decrypt(input_bytes: bytes, key: str) -> bytes:
    # Vernam encryption and decryption are symmetric (XOR)
    return vernam_encrypt(input_bytes, key)
