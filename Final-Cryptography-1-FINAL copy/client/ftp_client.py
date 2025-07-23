import threading
from client_config import *
from client_operations import *

SERVER_IP = '127.0.0.1'
PORT = 5001
room_key = ""
peer_public_key = None

def main():
    global room_key
    print("\n====================================\n")
    print("Wassup This is Secure File Transfer Client")
    print("\n====================================\n")

    room_key = input("Enter room key to join: ").strip()
    print("\n====================================\n")

    sock = connect_to_room(room_key, SERVER_IP, PORT)

    print("\n-------- Welcome to peer to peer Secure File Transfer --------\n")
    # Start thread for receiving files
    threading.Thread(target=receive_file, args=(sock, room_key), daemon=True).start()

    while True:
        send_file(sock, room_key)

if __name__ == "__main__":
    main()
