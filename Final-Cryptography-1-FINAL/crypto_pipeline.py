
from ciphers.transpotional import decrypt_transpositional, encrypt_transpositional
from ciphers.aes import start_aes
from ciphers.vernam import vernam_encrypt, vernam_decrypt
from ciphers.rsa import encrypt_rsa, decrypt_rsa

def hash_content(input_bytes: bytes) -> int:
    total = sum(b for b in input_bytes)
    length = len(input_bytes)
    return (total % 1000) + (length * 7)

def determine_order(action: str, key: str) -> list[int]:
    total_sum = sum(key.encode('utf-8'))
    total_process = 3

    order = []
    for i in range(total_process):
        order.append(total_sum % total_process)
        total_sum += 1

    if action == "decrypt":
        order = order[::-1]

    return order


def start_encrypt_decrypt(action: str, key: str, inputFile: str, outputFile: str) -> None:
    order = determine_order(action, key)

    try:
        if action == "encrypt":
            with open(inputFile, 'rb') as f:
                file_bytes = f.read()

            print("\n====================================\n")
            print(f"Before Encryption Hash Value: {hash_content(file_bytes)}")
            print("\n====================================\n")
            result_data = start_loop_process(order, key, file_bytes, operation=1)

            result_data = start_aes(action, result_data, key)

            with open(outputFile, 'wb') as f_out:
                f_out.write(result_data)

        elif action == "decrypt":
            with open(inputFile, 'rb') as f:
                file_bytes = f.read()

            decrypted_bytes = start_aes(action, file_bytes, key)
            result_data = start_loop_process(order, key, decrypted_bytes, operation=0)
            result_data = result_data.rstrip(b' ')
            
            print("\n====================================\n")
            print(f"After Decryption Hash Value: {hash_content(result_data)}")
            print("\n====================================\n")

            with open(outputFile, 'wb') as f_out:
                f_out.write(result_data)

        else:
            print("Unknown action")
            return

        print(f"{action.capitalize()}ion completed successfully.")

    except FileNotFoundError:
        print(f"Input file '{inputFile}' not found.")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"Error processing file: {e}")



        

def start_loop_process(order: list[int], key: str, input_data: bytes, operation: int) -> bytes:
    """
    order: list[int] with 3 steps
    key: string key
    input_data: bytes (the data to encrypt/decrypt)
    operation: 1 for encrypt, else decrypt
    """

    current_data = input_data

    for step in order:
        if step == 0:
            print("\n\nTRANSPOSITIONAL")
            if operation == 1:
                encrypted = encrypt_transpositional(current_data, key)
                current_data = encrypted
            else:
                decrypted = decrypt_transpositional(current_data, key)
                current_data = decrypted
        elif step == 1: # There is spaces when decrypted at last
            print("\n\nVERNAM")
            if operation == 1:
                encrypted = vernam_encrypt(current_data, key)
                current_data = encrypted
            else:
                decrypted = vernam_decrypt(current_data, key)
                current_data = decrypted

        elif step == 2:
            print("\n\nRSA")
            if operation == 1:
                # encrypt_rsa returns bytes (not base64 string) - update rsa.py accordingly
                encrypted_bytes = encrypt_rsa(current_data)  # bytes
                # convert to hex bytes to be consistent with other ciphers
                current_data = encrypted_bytes.hex().encode('utf-8')
            else:
                # current_data is hex bytes, convert back to bytes before decrypting
                hex_str = current_data.decode('utf-8')
                encrypted_bytes = bytes.fromhex(hex_str)
                decrypted_bytes = decrypt_rsa(encrypted_bytes)
                current_data = decrypted_bytes
        else:
            print(f"Unknown step in order: {step}")

    return current_data
