from .aes_operations import *

# def encrypt_aes(data: bytes, key: str) -> bytes:
#     # Just for illustration: NOT real AES — use real AES in production
#     return bytes([b ^ 42 for b in data[::-1]])

# def decrypt_aes(ciphertext: bytes, key: str) -> bytes:
#     # Reverse process of above
#     return bytes([b ^ 42 for b in ciphertext])[::-1]

# def start_aes(action: str, input_bytes: bytes, key: str) -> bytes:
#     if action == "encrypt":
#         return encrypt_aes(input_bytes, key)
#     elif action == "decrypt":
#         return decrypt_aes(input_bytes, key)


def start_aes(action: str, input_bytes: bytes, key: str) -> bytes:

    """ Get the first 16 bytes if greater than the input_bytes and """
    """ Loop, Get, Append every 16 Bytes """

    key_bytes = key.encode()[:16]
    if len(key_bytes) < 16:
        key_bytes = key_bytes.ljust(16, b' ')  # pad key if shorter than 16 bytes

    output = bytearray()

    for i in range(0, len(input_bytes), 16):
        chunk = input_bytes[i:i+16]
        # pad chunk if less than 16 bytes
        if len(chunk) < 16:
            chunk = chunk.ljust(16, b' ')
        
        if action == "encrypt":
            encrypted_chunk = encrypt_aes(chunk, key_bytes)
            output.extend(encrypted_chunk)
        elif action == "decrypt":
            decrypted_chunk = decrypt_aes(chunk, key_bytes)
            output.extend(decrypted_chunk)
        else:
            raise ValueError("Invalid AES action. Use 'encrypt' or 'decrypt'.")
    
    return bytes(output)


def encrypt_aes(plaintext, master_key):

    """Base on GFG docs and yt vid"""

    NUMBER_OF_ROUNDS = 10

    state = text2matrix(plaintext)
    round_keys = expand_key(master_key)

    add_round_key(state, round_keys[:4])
    
    for i in range(1, NUMBER_OF_ROUNDS):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[4 * i : 4 * (i + 1)])

    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, round_keys[40:])
    return matrix2text(state)

def decrypt_aes(ciphertext, master_key):

    """Base on GFG docs and yt vid"""

    NUMBER_OF_ROUNDS = 9

    state = text2matrix(ciphertext)
    round_keys = expand_key(master_key)

    add_round_key(state, round_keys[40:])
    inv_shift_rows(state)
    inv_sub_bytes(state)
    
    for i in range(NUMBER_OF_ROUNDS, 0, -1):
        add_round_key(state, round_keys[4 * i : 4 * (i + 1)])
        inv_mix_columns(state)
        inv_shift_rows(state)
        inv_sub_bytes(state)

    add_round_key(state, round_keys[:4])
    return matrix2text(state)
