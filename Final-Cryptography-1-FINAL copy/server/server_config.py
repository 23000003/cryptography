import socket
from collections import defaultdict

rooms = defaultdict(list)
clients_info = defaultdict(dict) # addr, pubkey

def print_room_members(room_key):
    members = [f"{info['addr'][0]}:{info['addr'][1]}" for info in clients_info[room_key].values()]
    print(f"[ROOM {room_key}] Current members ({len(members)}): {', '.join(members) if members else 'No members'}")

def handle_relay(conn, room_key, addr):
     # Handle file relay between two peers
        while True:
            # Receive file metadata
            filename_len_bytes = conn.recv(4)
            if not filename_len_bytes:
                break

            filename_len = int.from_bytes(filename_len_bytes, 'big')
            filename = conn.recv(filename_len).decode()
            filesize = int.from_bytes(conn.recv(8), 'big')

            # Receive file content
            file_data = b''
            remaining = filesize
            while remaining > 0:
                chunk = conn.recv(min(4096, remaining))
                if not chunk:
                    break
                file_data += chunk
                remaining -= len(chunk)

            print(f"[ROOM {room_key}] {addr} sent file: {filename} ({filesize} bytes)")

            # Relay file to other peer
            for client in rooms[room_key]:
                if client != conn:
                    try:
                        client.send(len(filename).to_bytes(4, 'big'))
                        client.send(filename.encode())
                        client.send(filesize.to_bytes(8, 'big'))
                        client.sendall(file_data)
                    except Exception as e:
                        print(f"[!] Failed to send to peer: {e}")

def exchange_keys(conn, room_key):
    # Exchange keys with existing peer (if any)
        for peer_conn in rooms[room_key]:
            if peer_conn != conn:
                # Send existing peer's public key to new client
                peer_pubkey = clients_info[room_key][peer_conn]['pubkey']
                conn.send(b"PEER_KEY")
                conn.send(len(peer_pubkey).to_bytes(4, 'big'))
                conn.send(peer_pubkey)

                # Send new client's key to existing peer
                conn_pubkey = clients_info[room_key][conn]['pubkey']
                peer_conn.send(b"PEER_KEY")
                peer_conn.send(len(conn_pubkey).to_bytes(4, 'big'))
                peer_conn.send(conn_pubkey)

def handle_client(conn: socket, addr):
    room_key = None
    try:
        # Receive room key
        key_len = int.from_bytes(conn.recv(2), 'big')
        room_key = conn.recv(key_len).decode()
        print(f"-> {addr} joined room: {room_key}")

        # Enforce 2-person room limit
        if len(rooms[room_key]) >= 2:
            print(f"[ROOM {room_key}] Full. Rejecting {addr}")
            conn.send(b"ROOM_FULL")
            conn.close()
            return

        # Receive client's public key
        pubkey_len = int.from_bytes(conn.recv(4), 'big')
        pubkey_data = conn.recv(pubkey_len)

        # Save connection and key
        rooms[room_key].append(conn)
        clients_info[room_key][conn] = {
            "addr": addr,
            "pubkey": pubkey_data,
        }

        print_room_members(room_key)
        exchange_keys(conn, room_key)
        handle_relay(conn, room_key, addr)

    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        if room_key:
            if conn in rooms[room_key]:
                rooms[room_key].remove(conn)
            if conn in clients_info[room_key]:
                del clients_info[room_key][conn]
            print(f"[-] {addr} disconnected from room: {room_key}")
            print_room_members(room_key)
        conn.close()
