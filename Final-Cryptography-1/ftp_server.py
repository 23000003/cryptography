import socket
import threading
from collections import defaultdict

HOST = '0.0.0.0'
PORT = 5001
rooms = defaultdict(list)  # room_key -> list of sockets
clients_info = defaultdict(dict)  # room_key -> {conn: addr} to keep track of clients' addresses

def print_room_members(room_key):
    members = [f"{addr[0]}:{addr[1]}" for addr in clients_info[room_key].values()]
    print(f"[ROOM {room_key}] Current members ({len(members)}): {', '.join(members) if members else 'No members'}")

def handle_client(conn, addr):
    room_key = None
    try:
        # Step 1: Get room key
        key_len = int.from_bytes(conn.recv(2), 'big')
        room_key = conn.recv(key_len).decode()
        print(f"[+] {addr} joined room: {room_key}")

        rooms[room_key].append(conn)
        clients_info[room_key][conn] = addr

        print_room_members(room_key)

        while True:
            # Step 2: Receive filename
            filename_len = int.from_bytes(conn.recv(4), 'big')
            filename = conn.recv(filename_len).decode()

            # Step 3: Receive filesize (size of hex string bytes)
            filesize = int.from_bytes(conn.recv(8), 'big')

            # Step 4: Receive hex string data bytes
            file_data = b''
            remaining = filesize
            while remaining > 0:
                chunk = conn.recv(min(4096, remaining))
                if not chunk:
                    break
                file_data += chunk
                remaining -= len(chunk)

            print(f"[ROOM {room_key}] Received file: {filename} ({filesize} bytes)")

            # Step 5: Broadcast hex string bytes to others in the room
            for client in rooms[room_key]:
                # Uncomment this if you want to exclude sender
                # if client != conn:
                try:
                    client.send(len(filename).to_bytes(4, 'big'))
                    client.send(filename.encode())
                    client.send(filesize.to_bytes(8, 'big'))
                    client.sendall(file_data)
                except:
                    pass

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

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
