# P2P File Sharing with GUI

This is a Python-based Peer-to-Peer file sharing application with a central server for discovery, and a GUI for ease of use.

## 🔧 Components

- `server.py`: Handles peer registration and file discovery.
- `client.py`: Acts as both client and server for file sharing.
- `gui.py`: Simple Tkinter GUI for interacting with the system.

## 📂 Setup

1. Place files to share in `shared_files/`.
2. Downloaded files go into `p2pdownloads/`.

## 🚀 How to Run

### On Server
```bash
python3 server.py
```

### On Each Peer
```bash
python3 client.py
python3 gui.py
```

## 🔌 Networking

- Ensure all machines are on the same network.
- Set `SERVER_IP` in `client.py` and `gui.py` to server IP.
