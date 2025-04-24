# client.py - P2P File Sharing Client

import socket
import threading
import os

SERVER_IP = "10.20.205.211"
SERVER_PORT = 5000
PEER_PORT = 6000
SHARED_FOLDER = "shared_files"
DOWNLOAD_FOLDER = "p2pdownloads"

def list_files():
    """ Requests file list from the central server """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(b"LIST")
            data = s.recv(4096).decode()
            files = data.split(";") if data else []
            return files, 1  # Assuming at least 1 peer
    except Exception as e:
        print("Error fetching file list:", e)
        return [], 0

def download_file(filename):
    """ Requests a file from the server """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(f"GET {filename}".encode())
            response = s.recv(1024).decode()

            if response == "OK":
                file_path = os.path.join(DOWNLOAD_FOLDER, filename)
                with open(file_path, "wb") as f:
                    while True:
                        chunk = s.recv(4096)
                        if not chunk:
                            break
                        f.write(chunk)
                return True, file_path
            else:
                return False, ""
    except Exception as e:
        print("Error downloading file:", e)
        return False, ""

def download_from_peer(filename, peer_ip):
    """ Downloads a file from another peer """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Connecting to peer {peer_ip}:{PEER_PORT} for {filename}")  # Debug
            s.connect((peer_ip, PEER_PORT))
            s.sendall(f"GET {filename}".encode())

            response = s.recv(1024).decode()
            print("Response from peer:", response)  # Debugging output

            if response == "OK":
                file_path = os.path.join(DOWNLOAD_FOLDER, filename)
                with open(file_path, "wb") as f:
                    while True:
                        chunk = s.recv(4096)
                        if not chunk:
                            break
                        print(f"Receiving chunk of {len(chunk)} bytes...")  # Debug
                        f.write(chunk)
                print(f"File {filename} downloaded successfully!")
                return True, file_path
            else:
                print("Error: Peer responded with", response)
                return False, ""
    except Exception as e:
        print("Error downloading file from peer:", e)
        return False, ""

def handle_peer_request(peer_socket):
    try:
        request = peer_socket.recv(1024).decode()
        print(f"[+] Incoming request: {request}")

        command, filename = request.split()

        if command == "GET":
            filepath = os.path.join(SHARED_FOLDER, filename)
            print(f"[+] Requested file path: {filepath}")

            if os.path.exists(filepath):
                peer_socket.sendall(b"OK")
                with open(filepath, "rb") as f:
                    peer_socket.sendfile(f)
                print(f"[+] Sent file: {filename}")
            else:
                peer_socket.sendall(b"ERROR: File not found")
                print(f"[!] File not found: {filename}")
    except Exception as e:
        print("Error handling peer request:", e)
    finally:
        peer_socket.close()

def start_peer_server():
    """ Starts a peer server for P2P file sharing """
    peer_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    peer_server.bind(("0.0.0.0", PEER_PORT))
    peer_server.listen()
    print(f"[+] Peer server running on port {PEER_PORT}")

    while True:
        peer_socket, addr = peer_server.accept()
        print(f"[+] Connection from {addr}")
        threading.Thread(target=handle_peer_request, args=(peer_socket,)).start()

if __name__ == "__main__":
    if not os.path.exists(SHARED_FOLDER):
        os.makedirs(SHARED_FOLDER)
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    threading.Thread(target=start_peer_server, daemon=True).start()
    print("[+] Client is running. Ready to download files. Press Ctrl+C to exit.")
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\n[!] Shutting down client.")


