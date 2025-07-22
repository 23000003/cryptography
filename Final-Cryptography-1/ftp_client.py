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

    # Encrypt file to hex string file
    startEncryptOrDecrypt("encrypt", room_key, filepath, encrypted_filename)

    if not os.path.isfile(encrypted_filename):
        print("Encryption failed.")
        return

    # Read encrypted file as hex string
    with open(encrypted_filename, 'r', encoding='utf-8') as f:
        hex_str = f.read()

    hex_bytes = hex_str.encode('utf-8')
    filesize = len(hex_bytes)

    sock.send(len(filename).to_bytes(4, 'big'))  # Send original filename length
    sock.send(filename.encode())                 # Send original filename
    sock.send(filesize.to_bytes(8, 'big'))      # Send size of hex string bytes

    # Send hex string as bytes
    sock.sendall(hex_bytes)

    print(f"[✓] Sent encrypted {filename} as hex")

def receive_file(sock):
    while True:
        try:
            filename_len = int.from_bytes(sock.recv(4), 'big')
            filename = sock.recv(filename_len).decode()
            filesize = int.from_bytes(sock.recv(8), 'big')

            encrypted_filename = f"encrypted_{filename}"  # file to save hex string
            decrypted_filename = filename + "1"            # decrypted file output

            data = b''
            remaining = filesize
            while remaining > 0:
                chunk = sock.recv(min(4096, remaining))
                if not chunk:
                    break
                data += chunk
                remaining -= len(chunk)

            # data received is hex string encoded as bytes
            hex_str = data.decode('utf-8')

            # Save encrypted hex string to file
            with open(encrypted_filename, "w", encoding='utf-8') as f:
                f.write(hex_str)

            print(f"[+] Received encrypted hex file: {encrypted_filename}")

            # Decrypt hex file to original
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
