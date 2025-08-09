# gui.py - P2P File Sharing GUI

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import client

class P2PGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("P2P File Sharing")
        self.root.geometry("500x450")
        self.root.configure(bg="#f0f4f8")

        main_frame = tk.Frame(root, bg="#e3eaf2", bd=2, relief=tk.RIDGE)
        main_frame.pack(padx=18, pady=18, fill=tk.BOTH, expand=True)

        self.label = tk.Label(main_frame, text="P2P File Sharing Client", font=("Arial", 16, "bold"), fg="#2c3e50", bg="#e3eaf2")
        self.label.pack(pady=(10, 18))

        self.list_button = tk.Button(main_frame, text="List Available Files", command=self.list_files, font=("Arial", 11), bg="#6fa3ef", fg="white", activebackground="#4a90e2", relief=tk.GROOVE)
        self.list_button.pack(pady=6, ipadx=8, ipady=2)

        self.filename_entry = tk.Entry(main_frame, width=40, font=("Arial", 11), bg="#f7fbff", fg="#34495e", relief=tk.SUNKEN)
        self.filename_entry.pack(pady=6)
        self.filename_entry.insert(0, "Enter filename to download")

        self.peer_entry = tk.Entry(main_frame, width=40, font=("Arial", 11), bg="#f7fbff", fg="#34495e", relief=tk.SUNKEN)
        self.peer_entry.pack(pady=6)
        self.peer_entry.insert(0, "Enter peer IP (or leave blank)")

        self.download_button = tk.Button(main_frame, text="Download File", command=self.download_file, font=("Arial", 11), bg="#5cb85c", fg="white", activebackground="#449d44", relief=tk.GROOVE)
        self.download_button.pack(pady=6, ipadx=8, ipady=2)

        self.quit_button = tk.Button(main_frame, text="Exit", command=root.quit, font=("Arial", 11), bg="#e74c3c", fg="white", activebackground="#c0392b", relief=tk.GROOVE)
        self.quit_button.pack(pady=12, ipadx=8, ipady=2)

        self.output_text = tk.Text(main_frame, height=12, width=55, font=("Consolas", 10), bg="#f7fbff", fg="#2c3e50", relief=tk.SUNKEN, bd=2)
        self.output_text.pack(pady=6)

        self.peer_count_label = tk.Label(main_frame, text="Peers Available: 0", font=("Arial", 11, "italic"), fg="#34495e", bg="#e3eaf2")
        self.peer_count_label.pack(pady=8)
        
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

