import socket
import threading
import os

PEER_PORT = 5000  # Server will help peers find each other
SHARED_FOLDER = "shared_files"
peers = {}  # Dictionary to store peer IPs and their shared files

def handle_client(client_socket, client_address):
    request = client_socket.recv(1024).decode()
    print(f"Debug: Received request -> {request}")  # Debugging

    if request.startswith("REGISTER"):
        """ Register the peer with its available files """
        _, files = request.split(" ", 1)
        peers[client_address[0]] = files.split(",")
        client_socket.send(b"Registered successfully")

    elif request.startswith("GET_PEERS"):
        """ Send back a list of available peers and their files """
        response = "\n".join([f"{ip}: {', '.join(files)}" for ip, files in peers.items()])
        client_socket.send(response.encode())

    elif request.startswith("GET"):
        """ Handle file download requests """
        _, filename = request.split(maxsplit=1)
        filepath = os.path.join(SHARED_FOLDER, filename)

        if os.path.exists(filepath):
            client_socket.send(b"OK")
            with open(filepath, "rb") as f:
                client_socket.sendfile(f)
            print(f"Debug: Sent {filename} successfully")
        else:
            client_socket.send(b"ERROR: File not found")
            print(f"Debug: {filename} not found on server")

    elif request.startswith("LIST"):
        """ Send back a list of available files in the server's shared folder """
        try:
            files = os.listdir(SHARED_FOLDER) if os.path.exists(SHARED_FOLDER) else []
            response = ";".join(files) if files else "NO_FILES"
            client_socket.send(response.encode())
            print(f"Debug: Sent file list -> {response}")
        except Exception as e:
            print("Error listing files:", e)
            client_socket.send(b"ERROR")

    client_socket.close()

def start_server():
    """ Start the central peer discovery server """
    if not os.path.exists(SHARED_FOLDER):
        os.makedirs(SHARED_FOLDER)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PEER_PORT))
    server.listen()

    print(f"[+] Peer discovery server running on port {PEER_PORT}")

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()

