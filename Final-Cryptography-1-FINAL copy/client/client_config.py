import socket
import base64
import ciphers.rsa_pems
from ciphers.rsa_pems import PUBLIC_KEY

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

def connect_to_room(room_key, SERVER_IP, PORT) -> socket:
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

    return sock