import socket
import os
import threading
from crypto_pipeline import start_encrypt_decrypt

SERVER_IP = '127.0.0.1'
PORT = 5001
room_key = ""

def send_file(sock):
    filepath = input("Enter path to file to send: ").strip()
    if not os.path.isfile(filepath):
        print("File not found.")
        return

    filename = os.path.basename(filepath)
    encrypted_filename = f"encrypted_{filename}"

    # Encrypt file and save raw bytes
    start_encrypt_decrypt("encrypt", room_key, filepath, encrypted_filename)

    if not os.path.isfile(encrypted_filename):
        print("Encryption failed.")
        return

    # Read encrypted file as raw bytes
    with open(encrypted_filename, 'rb') as f:
        file_data = f.read()

    filesize = len(file_data)

    # Send file metadata and data
    sock.send(len(filename).to_bytes(4, 'big'))   # Send filename length
    sock.send(filename.encode())                 # Send filename
    sock.send(filesize.to_bytes(8, 'big'))       # Send filesize
    sock.sendall(file_data)                      # Send encrypted file data

    print(f"[✓] Sent encrypted file: {filename} ({filesize} bytes)")

def receive_file(sock):
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

            print(f"[+] Received encrypted file: {encrypted_filename}")

            # Decrypt the file
            start_encrypt_decrypt("decrypt", room_key, encrypted_filename, decrypted_filename)
            print(f"[✓] Decrypted to: {decrypted_filename}")

        except Exception as e:
            print(f"[!] Receive error: {e}")
            break

def main():
    global room_key
    room_key = input("Enter room key to join: ").strip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))

    # Send room key
    sock.send(len(room_key).to_bytes(2, 'big'))
    sock.send(room_key.encode())

    # Start receiver thread
    threading.Thread(target=receive_file, args=(sock,), daemon=True).start()

    while True:
        send_file(sock)

if __name__ == "__main__":
    main()
