def map_encryption_key(key: str):
    return sorted(range(len(key)), key=lambda k: key[k])


def encrypt_transpositional(plaintext: bytes, key: str) -> bytes:
    key_len = len(key)
    mapped_key = map_encryption_key(key)
    rows = (len(plaintext) + key_len - 1) // key_len

    # Create padded matrix
    matrix = []
    idx = 0
    for _ in range(rows):
        row = []
        for _ in range(key_len):
            if idx < len(plaintext):
                row.append(plaintext[idx])
                idx += 1
            else:
                row.append(ord(' '))  # Padding with space
        matrix.append(row)

    # Encrypt by reading columns in key order
    encrypted = bytearray()
    for col_idx in mapped_key:
        for row in matrix:
            encrypted.append(row[col_idx])

    return bytes(encrypted)


def decrypt_transpositional(ciphertext: bytes, key: str) -> bytes:
    key_len = len(key)
    mapped_key = map_encryption_key(key)
    rows = (len(ciphertext) + key_len - 1) // key_len

    # Prepare empty matrix
    matrix = [[ord(' ')] * key_len for _ in range(rows)]

    idx = 0
    for k in mapped_key:
        for i in range(rows):
            if idx < len(ciphertext):
                matrix[i][k] = ciphertext[idx]
                idx += 1

    # Read row-wise to get original plaintext
    decrypted = bytearray()
    for row in matrix:
        decrypted.extend(row)

    return bytes(decrypted[:len(ciphertext)])

