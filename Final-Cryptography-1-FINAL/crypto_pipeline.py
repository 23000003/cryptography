
from ciphers.transpotional import decrypt_transpositional, encrypt_transpositional
from ciphers.aes import start_aes
from ciphers.vernam import vernam_encrypt, vernam_decrypt
from ciphers.rsa import encrypt_rsa, decrypt_rsa

def hash_content(input_bytes: bytes) -> int:
    """
    Hashes the content of the input bytes.
    """
    total = sum(b for b in input_bytes)
    length = len(input_bytes)
    return (total % 1000) + (length * 7)

def determine_order(action: str, key: str) -> list[int]:
    """
    Determines the order of processing steps based on the action and key.
    The order is based on the sum of the key's character values modulo the number of steps.
    """
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
    """
    Starts the encryption or decryption process.
    action: "encrypt" or "decrypt"
    key: encryption/decryption key
    inputFile: path to the input file
    outputFile: path to the output file
    """
    order = determine_order(action, key)
    key = key.replace(" ", "")
    try:
        if action == "encrypt":
            with open(inputFile, 'rb') as f:
                file_bytes = f.read()
                
            print('\n------------- Encryption Process -------------')

            print("\n====================================\n")
            print(f"Before Encryption Hash Value: {hash_content(file_bytes)}")
            print("\n====================================\n")
            result_data = start_loop_process(order, key, file_bytes, operation=1)

            print("\n -> 4 AES")
            result_data = start_aes(action, result_data, key)

            with open(outputFile, 'wb') as f_out:
                f_out.write(result_data)
                
            print("\n----------- End of Encryption Process ------------\n")

        elif action == "decrypt":
            with open(inputFile, 'rb') as f:
                file_bytes = f.read()
            
            print('\n------------- Decryption Process -------------')
            
            print("\n -> 1 AES")
            decrypted_bytes = start_aes(action, file_bytes, key)
            result_data = start_loop_process(order, key, decrypted_bytes, operation=0)
            result_data = result_data.rstrip(b' ')
            
            print("\n====================================\n")
            print(f"After Decryption Hash Value: {hash_content(result_data)}")
            print("\n====================================\n")

            with open(outputFile, 'wb') as f_out:
                f_out.write(result_data)
            
            print("\n----------- End of Decryption Process ------------\n")
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
    print(f"NEW KEY1: {key}")
    for step in order:
        if step == 0:
            print("\n -> %d TRANSPOSITIONAL" % step)
            if operation == 1:
                encrypted = encrypt_transpositional(current_data, key)
                current_data = encrypted
            else:
                decrypted = decrypt_transpositional(current_data, key)
                current_data = decrypted
        elif step == 1:
            print("\n -> %d VERNAM" % step)
            if operation == 1:
                encrypted = vernam_encrypt(current_data, key)
                current_data = encrypted
            else:
                decrypted = vernam_decrypt(current_data, key)
                current_data = decrypted

        elif step == 2:
            print("\n -> %d RSA" % step)
            if operation == 1:
                current_data = encrypt_rsa(current_data)
            else:
                current_data = decrypt_rsa(current_data)
        else:
            print(f"Unknown step in order: {step}")

    return current_data
