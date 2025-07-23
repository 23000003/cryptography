import os
from crypto_pipeline import start_encrypt_decrypt
import socket

def send_file(sock, room_key):
    global peer_public_key
    if peer_public_key is None:
        print("No peer public key. Cannot send encrypted file.")
        return

    filepath = input("Enter path to file to send: ").strip()
    if not os.path.isfile(filepath):
        print("-> File not found.")
        return

    filename = os.path.basename(filepath)
    encrypted_filename = f"encrypted_{filename}"

    # Encrypt file using peer's public key
    start_encrypt_decrypt("encrypt", room_key, filepath, encrypted_filename)

    if not os.path.isfile(encrypted_filename):
        print("-> Encryption failed.")
        return

    with open(encrypted_filename, 'rb') as f:
        file_data = f.read()

    filesize = len(file_data)

    # Send file metadata and data
    sock.send(len(filename).to_bytes(4, 'big'))
    sock.send(filename.encode())
    sock.send(filesize.to_bytes(8, 'big'))
    sock.sendall(file_data)

    print(f"\nSent encrypted file: {filename} ({filesize} bytes)\n")

def receive_file(sock: socket, room_key: str):
    while True:
        try:
            filename_len_bytes = sock.recv(4)
            if not filename_len_bytes:
                break
            filename_len = int.from_bytes(filename_len_bytes, 'big')
            filename = sock.recv(filename_len).decode()
            filesize = int.from_bytes(sock.recv(8), 'big')

            encrypted_filename = f"encrypted_{filename}"
            decrypted_filename = f"decrypted_{filename}"

            data = b''
            remaining = filesize
            while remaining > 0:
                chunk = sock.recv(min(4096, remaining))
                if not chunk:
                    break
                data += chunk
                remaining -= len(chunk)

            # Save encrypted file
            with open(encrypted_filename, "wb") as f:
                f.write(data)
            print(f"-> Key: {room_key}")
            print(f"-> Received encrypted file: {encrypted_filename}")

            # Decrypt the file
            start_encrypt_decrypt("decrypt", room_key, encrypted_filename, decrypted_filename)
            print(f"-> Decrypted to: {decrypted_filename}")

        except Exception as e:
            print(f"[!] Receive error: {e}")
            break