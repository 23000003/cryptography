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
    key_bytes = key.encode()[:16]
    if len(key_bytes) < 16:
        key_bytes = key_bytes.ljust(16, b' ')
    output = bytearray()

    for i in range(0, len(input_bytes), 16):
        chunk = input_bytes[i:i+16]
        if action == "encrypt":
            encrypted_chunk = encrypt_aes(chunk, key_bytes)
            output.extend(encrypted_chunk)
        elif action == "decrypt":
            decrypted_chunk = decrypt_aes(chunk, key_bytes)
            output.extend(decrypted_chunk)
        else:
            raise ValueError("Invalid AES action. Use 'encrypt' or 'decrypt'.")
    else:
        return bytes(output)


def encrypt_aes(plaintext, master_key):

    """
    Based on GFG docs and yt vid
    Encrypts the plaintext using AES with the given key.
    The plaintext is padded with spaces if its length is not a multiple of 16.
    The AES encryption is performed in 10 rounds for a 128-bit key.
    The function returns the encrypted ciphertext.
    """

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

    """
    Based on GFG docs and yt vid
    Decrypts the ciphertext using AES with the given key.
    The ciphertext is expected to be padded with spaces if its length is not a multiple of 16.
    The AES decryption is performed in 10 rounds for a 128-bit key and 2 functions are inversed.
    The function returns the decrypted plaintext.
    """

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
