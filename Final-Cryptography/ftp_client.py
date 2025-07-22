import socket
import os
import threading
from crypto_pipeline import startEncryptOrDecrypt

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

    # Encrypt before sending
    startEncryptOrDecrypt("encrypt", room_key, filepath, encrypted_filename)

    if not os.path.isfile(encrypted_filename):
        print("Encryption failed.")
        return

    filesize = os.path.getsize(encrypted_filename)

    sock.send(len(filename).to_bytes(4, 'big'))  # Send original filename length
    sock.send(filename.encode())                 # Send original filename
    sock.send(filesize.to_bytes(8, 'big'))       # Send size of encrypted file

    with open(encrypted_filename, 'rb') as f:
        while chunk := f.read(4096):
            sock.sendall(chunk)

    print(f"[✓] Sent encrypted {filename}")

def receive_file(sock):
    while True:
        try:
            filename_len = int.from_bytes(sock.recv(4), 'big')
            filename = sock.recv(filename_len).decode()
            filesize = int.from_bytes(sock.recv(8), 'big')

            encrypted_filename = f"encrypted_{filename}"  # Save encrypted as "encrypted_originalfilename"
            decrypted_filename = filename                 # Save decrypted as original filename

            data = b''
            remaining = filesize
            while remaining > 0:
                chunk = sock.recv(min(4096, remaining))
                if not chunk:
                    break
                data += chunk
                remaining -= len(chunk)

            with open(encrypted_filename, "wb") as f:
                f.write(data)

            print(f"[+] Received encrypted file: {encrypted_filename}")

            # Decrypt after receiving
            startEncryptOrDecrypt("decrypt", room_key, encrypted_filename, decrypted_filename)
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

    # Start receiving thread
    threading.Thread(target=receive_file, args=(sock,), daemon=True).start()

    while True:
        send_file(sock)

if __name__ == "__main__":
    main()
