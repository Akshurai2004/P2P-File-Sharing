# gui.py - P2P File Sharing GUI

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import client

class P2PGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("P2P File Sharing")
        self.root.geometry("450x400")
        
        self.label = tk.Label(root, text="P2P File Sharing Client", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.list_button = tk.Button(root, text="List Available Files", command=self.list_files)
        self.list_button.pack(pady=5)
        
        self.filename_entry = tk.Entry(root, width=40)
        self.filename_entry.pack(pady=5)
        self.filename_entry.insert(0, "Enter filename to download")
        
        self.peer_entry = tk.Entry(root, width=40)
        self.peer_entry.pack(pady=5)
        self.peer_entry.insert(0, "Enter peer IP (or leave blank)")
        
        self.download_button = tk.Button(root, text="Download File", command=self.download_file)
        self.download_button.pack(pady=5)
        
        self.quit_button = tk.Button(root, text="Exit", command=root.quit)
        self.quit_button.pack(pady=10)
        
        self.output_text = tk.Text(root, height=12, width=55)
        self.output_text.pack()
        
        self.peer_count_label = tk.Label(root, text="Peers Available: 0", font=("Arial", 10))
        self.peer_count_label.pack(pady=5)
        
    def list_files(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Fetching file list...\n")
        
        def fetch_files():
            files, peer_count = client.list_files()
            print("Debug: Fetched files ->", files)  # Debug print
            
            if isinstance(files, list) and files:
                self.output_text.insert(tk.END, "Available Files:\n")
                for file in files:
                    self.output_text.insert(tk.END, f" - {file}\n")
            else:
                self.output_text.insert(tk.END, "No files available.\n")
            
            self.peer_count_label.config(text=f"Peers Available: {peer_count}")
    
        threading.Thread(target=fetch_files).start()


    
    def download_file(self):
        filename = self.filename_entry.get().strip()
        peer_ip = self.peer_entry.get().strip()
        
        if not filename:
            messagebox.showerror("Error", "Please enter a filename.")
            return
        
        self.output_text.insert(tk.END, f"Requesting {filename} from {'peer ' + peer_ip if peer_ip else 'server'}...\n")
        
        def fetch_file():
            if peer_ip:
                success, filepath = client.download_from_peer(filename, peer_ip)
            else:
                success, filepath = client.download_file(filename)
            
            if success:
                self.output_text.insert(tk.END, f"Download complete: {filename}\nSaved at: {filepath}\n")
            else:
                self.output_text.insert(tk.END, f"Failed to download: {filename}\n")
        
        threading.Thread(target=fetch_file).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = P2PGUI(root)
    root.mainloop()

