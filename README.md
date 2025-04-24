
# Peer TO Peer File SHaring
📁 P2P File Sharing with GUI

*This project is a simple peer-to-peer (P2P) file sharing system using Python sockets. It includes:*

- A central server for peer discovery.
- A client peer capable of sharing and downloading files.
- A GUI frontend (using Tkinter) for easier interaction.

---
📄 File Structure
```graphql
p2p-file-sharing/
├── server.py           # Central peer registry and file host
├── client.py           # Peer client with file sharing and P2P download
├── gui.py              # GUI to select peer, view files, and download
├── shared_files/       # Folder to place files you want to share
├── p2pdownloads/       # Folder where downloaded files are saved
└── README.md           # You’re reading it :)
```

---
✅ Requirements
    
- Python 3.6+
- Works on Linux, Windows, or WSL
- No third-party packages required

---
🚀 How to Run

- Start the Server On one machine (ideally the host):
    ```
    python3 server.py
    ```

- Start the Client (Peer) On each peer, including the server if needed:
    ```
    python3 client.py
    ```

- Run GUI (on peer):
    ```
    python3 gui.py
    ```

---
🌐 Network Instructions
    
- Make sure all systems are on the same network.
- Update SERVER_IP in client.py and gui.py to the IP of the system running server.py.
- Open port 6000 on all peers for P2P downloads.
- You can test peer connections with:
  ```bash
    nc -vz <peer_ip> 6000
  ```

---
📦 File Sharing
    
- Place files you want to share in shared_files/
- Downloaded files will be saved to p2pdownloads/
- From GUI: Enter a peer’s IP, select a file, and hit Download

---
🛠 Troubleshooting
    
- Make sure shared_files/ and p2pdownloads/ exist before running.
- If GUI hangs or fails, check:
- Firewall or network issues
- Wrong IP or peer not running

---
😊 BY
    
- *Aneesh Bharadwaj K S*
- *Akanksh Rai*


