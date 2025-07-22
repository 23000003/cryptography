import socket
import os
import threading
import base64
from crypto_pipeline import start_encrypt_decrypt
from ciphers.rsa_pems import PUBLIC_KEY
import ciphers.rsa_pems

SERVER_IP = '127.0.0.1'
PORT = 5001
room_key = ""
peer_public_key = None

def reliable_recv(sock, n):
    """Receive exactly n bytes or raise an error."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise ConnectionError("Socket connection broken")
        data += packet
    return data

def wait_for_peer_key(sock):
    global peer_public_key
    print("Waiting for peer public key...")

    # Expect "PEER_KEY" (8 bytes)
    prefix = reliable_recv(sock, 8)
    if prefix != b'PEER_KEY':
        raise ValueError(f"Expected PEER_KEY prefix, got {prefix}")

    # Then 4 bytes length of key
    key_len_bytes = reliable_recv(sock, 4)
    key_len = int.from_bytes(key_len_bytes, 'big')

    # Then key bytes themselves
    key_bytes = reliable_recv(sock, key_len)

    peer_public_key = base64.b64encode(key_bytes).decode()
    ciphers.rsa_pems.peer_public_key = peer_public_key 
    
    print("Received peer public key.")
    
    print("\n====================================\n")

def send_file(sock):
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
            print(f"-> Key: {room_key}")
            print(f"-> Received encrypted file: {encrypted_filename}")

            # Decrypt the file
            start_encrypt_decrypt("decrypt", room_key, encrypted_filename, decrypted_filename)
            print(f"-> Decrypted to: {decrypted_filename}")

        except Exception as e:
            print(f"[!] Receive error: {e}")
            break

def main():
    global room_key
    print("\n====================================\n")
    print("Wassup This is Secure File Transfer Client")
    print("\n====================================\n")

    room_key = input("Enter room key to join: ").strip()
    print("\n====================================\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))

    # Send room key
    sock.send(len(room_key).to_bytes(2, 'big'))
    sock.send(room_key.encode())

    # Send our public key (decoded from base64)
    pubkey_bytes = base64.b64decode(PUBLIC_KEY.encode())
    sock.send(len(pubkey_bytes).to_bytes(4, 'big'))
    sock.send(pubkey_bytes)

    print("\n====================================\n")
    print("Waiting for peer to join...")
    # Wait for peer key BEFORE starting receive thread
    wait_for_peer_key(sock)

    print("\n-------- Welcome to peer to peer Secure File Transfer --------\n")
    # Start thread for receiving files
    threading.Thread(target=receive_file, args=(sock,), daemon=True).start()

    while True:
        send_file(sock)

if __name__ == "__main__":
    main()
