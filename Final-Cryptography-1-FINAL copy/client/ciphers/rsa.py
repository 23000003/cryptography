from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from .rsa_pems import PRIVATE_KEY
import ciphers.rsa_pems

def chunk_data(data: bytes, chunk_size: int):
    """
    Splits the data into chunks of the specified size.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]

def encrypt_rsa(data: bytes) -> bytes:
    
    """
    Encrypts data using RSA with OAEP padding.
    Uses peer public key
    The maximum plaintext chunk size is calculated as:
        max_chunk_size = key_size_in_bytes - 2 * hash_size_in_bytes - 2
        '-2' is padding overhead
    """
    print("\n\n=== Peer public key: ====\n")
    print(ciphers.rsa_pems.peer_public_key)
    key = RSA.import_key(base64.b64decode(ciphers.rsa_pems.peer_public_key))
    cipher = PKCS1_OAEP.new(key)
    
    key_size_in_bytes = key.size_in_bytes()
    hash_size_in_bytes = 32  # SHA-256
    encrypted_chunks = []
    max_chunk_size = key_size_in_bytes - 2 * hash_size_in_bytes - 2 

    for chunk in chunk_data(data, max_chunk_size):
        encrypted_chunk = cipher.encrypt(chunk)
        encrypted_chunks.append(encrypted_chunk)
    
    return b"".join(encrypted_chunks)

def decrypt_rsa(data: bytes) -> bytes:

    """
    Decrypts data using RSA with OAEP padding.
    The maximum ciphertext chunk size is equal to the key size in bytes.
    """

    key = RSA.import_key(base64.b64decode(PRIVATE_KEY))
    cipher = PKCS1_OAEP.new(key)
    
    decrypted_chunks = []
    chunk_size = key.size_in_bytes()  # 256 bytes for 2048-bit key
    
    for i in range(0, len(data), chunk_size):
        encrypted_chunk = data[i:i+chunk_size]
        decrypted_chunk = cipher.decrypt(encrypted_chunk)
        decrypted_chunks.append(decrypted_chunk)
    
    return b"".join(decrypted_chunks)