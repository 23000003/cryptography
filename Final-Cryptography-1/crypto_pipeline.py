
from ciphers.transpotional import *
from ciphers.aes import *
from ciphers.vernam import *
from ciphers.rsa import encrypt_rsa, decrypt_rsa

def hash_content(input_bytes: bytes) -> int:
    total = sum(b for b in input_bytes)
    length = len(input_bytes)
    return (total % 1000) + (length * 7)

def determineOrder(action: str, key: str) -> list[int]:
    total_sum = sum(key.encode('utf-8'))
    total_process = 3

    order = []
    for i in range(total_process):
        order.append(total_sum % total_process)
        total_sum += 1

    if action == "decrypt":
        order = order[::-1]

    return order


def startEncryptOrDecrypt(action: str, key: str, inputFile: str, outputFile: str) -> None:
    order = determineOrder(action, key)

    try:
        if action == "encrypt":
            with open(inputFile, 'rb') as f:
                file_bytes = f.read()

            # Run your custom encryption steps first
            result_data = startLoopProcess(order, key, file_bytes, operation=1)

            # Then AES encryption (returns bytes)
            result_data = encrypt_aes(result_data, key)

            # Store as hex string
            with open(outputFile, 'w', encoding='utf-8') as f_out:
                f_out.write(result_data.hex())

        elif action == "decrypt":
            # Read hex string, convert to bytes
            with open(inputFile, 'r', encoding='utf-8') as f:
                hex_data = f.read().strip()
            file_bytes = bytes.fromhex(hex_data)

            # First AES decrypt
            decrypted_bytes = decrypt_aes(file_bytes, key)

            # Then your custom decryption steps
            result_data = startLoopProcess(order, key, decrypted_bytes, operation=0)

            # Save final decrypted data as utf-8 text
            with open(outputFile, 'w', encoding='utf-8') as f_out:
                f_out.write(result_data.rstrip().decode('utf-8', errors='ignore'))

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


        

def startLoopProcess(order: list[int], key: str, input_data: bytes, operation: int) -> bytes:
    """
    order: list[int] with 3 steps
    key: string key
    input_data: bytes (the data to encrypt/decrypt)
    operation: 1 for encrypt, else decrypt
    """

    current_data = input_data  # bytes

    for step in order:
        if step == 0:
            print("\n\nTRANSPOSITIONAL")
            if operation == 1:
                encrypted = encrypt_transpositional(current_data, key)
                current_data = encrypted
                print(f"Cipher Output (hex): {current_data.hex()}")
            else:
                decrypted = decrypt_transpositional(current_data, key)
                current_data = decrypted
                try:
                    print(f"Decrypted Output: {current_data.rstrip().decode('utf-8', errors='ignore')}")
                except Exception:
                    print("Decrypted output cannot be decoded to UTF-8")

        elif step == 1: # There is spaces when decrypted at last
            print("\n\nVERNAM")
            if operation == 1:
                encrypted = vernam_encrypt(current_data, key)
                current_data = encrypted
                print(f"Cipher Output (hex): {current_data.hex()}")
            else:
                decrypted = vernam_decrypt(current_data, key)
                current_data = decrypted

        elif step == 2:
            print("\n\nRSA")
            if operation == 1:
                # encrypt_rsa returns bytes (not base64 string) - update rsa.py accordingly
                print("\nENCRYPT RSA\n")
                encrypted_bytes = encrypt_rsa(current_data)  # bytes
                print("\nWent Throguh\n")
                # convert to hex bytes to be consistent with other ciphers
                current_data = encrypted_bytes.hex().encode('utf-8')
                print(f"Cipher Output (hex): {current_data.decode()}")
            else:
                # current_data is hex bytes, convert back to bytes before decrypting
                hex_str = current_data.decode('utf-8')
                encrypted_bytes = bytes.fromhex(hex_str)
                decrypted_bytes = decrypt_rsa(encrypted_bytes)
                current_data = decrypted_bytes
                try:
                    print(f"Decrypted Output: {current_data.decode('utf-8', errors='ignore')}")
                except Exception:
                    print("RSA output not UTF-8")

        else:
            print(f"Unknown step in order: {step}")

    return current_data
