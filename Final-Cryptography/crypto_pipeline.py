
from ciphers.transpotional import *
from ciphers.aes import *
from ciphers.vernam import *

def determineOrder(action, key):
    total_sum = sum(key.encode('utf-8'))
    total_process = 3

    order = []
    for i in range(total_process):
        order.append(total_sum % total_process)
        total_sum += 1

    if action == "decrypt":
        order = order[::-1]

    return order


def startEncryptOrDecrypt(action, key, inputFile, outputFile):
    order = determineOrder(action, key)

    try:
        # Read file as bytes, not string
        with open(inputFile, 'rb') as f:
            file_bytes = f.read()

        if action == "encrypt":
            # Run your custom process first (transpositional etc)
            result_data = startLoopProcess(order, key, file_bytes, operation=1)
            # Then encrypt with AES last step
            result_data = encrypt_aes(result_data, key)

            # Save encrypted data as binary
            with open(outputFile, 'wb') as f_out:
                f_out.write(result_data)

        elif action == "decrypt":
            # First decrypt AES
            decrypted_bytes = decrypt_aes(file_bytes, key)

            # Then run your custom decrypt processes
            result_data = startLoopProcess(order, key, decrypted_bytes, operation=0)

            # Save the final decrypted data as utf-8 text
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

        

def startLoopProcess(order, key, input_data, operation):
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
                # Encrypt
                encrypted = encrypt_transpositional(current_data, key)
                current_data = encrypted
                print(f"Cipher Output (hex): {current_data.hex()}")
            else:
                # Decrypt
                decrypted = decrypt_transpositional(current_data, key)
                current_data = decrypted
                try:
                    print(f"Decrypted Output: {current_data.rstrip().decode('utf-8', errors='ignore')}")
                except Exception:
                    print("Decrypted output cannot be decoded to UTF-8")

        elif step == 1: # There is spaces when decrypted at last
            print("\n\nVERNAM")
            # Placeholder for Vernam encrypt/decrypt
            if operation == 1:
                # Encrypt
                encrypted = vernam_encrypt(current_data, key)
                current_data = encrypted
                print(f"Cipher Output (hex): {current_data.hex()}")
            else:
                decrypted = vernam_decrypt(current_data, key)
                current_data = decrypted
                

        elif step == 2:
            print("\n\nRSA")
            # Placeholder for RSA encrypt/decrypt
            print("RSA step not implemented.")

        else:
            print(f"Unknown step in order: {step}")

    return current_data
