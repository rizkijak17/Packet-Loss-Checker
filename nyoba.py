import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from pathlib import Path
import re
from datetime import datetime


class PacketLossCheckerApp:
    def __init__(self):
        # Setup window
        self.window = ctk.CTk()
        self.window.title("Packet Loss Checker")
        self.window.geometry("900x600")

        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(2, weight=1)

        # Variables
        self.selected_files = []
        self.packet_loss_data = []
        self.current_folder = ""

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = ctk.CTkLabel(self.window, text="Packet Loss Checker",
                                   font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Input Frame
        input_frame = ctk.CTkFrame(self.window)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(2, weight=1)

        # File Input Button
        self.file_btn = ctk.CTkButton(input_frame, text="Input File txt",
                                      command=self.select_files)
        self.file_btn.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        # Folder Input Button
        self.folder_btn = ctk.CTkButton(input_frame, text="Input Folder",
                                        command=self.select_folder)
        self.folder_btn.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # Reset Button
        self.reset_btn = ctk.CTkButton(input_frame, text="Reset",
                                       command=self.reset_app,
                                       fg_color="#d9534f", hover_color="#c9302c")
        self.reset_btn.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

        # Folder Label
        self.folder_label = ctk.CTkLabel(input_frame, text="FOLDER: ",
                                         font=ctk.CTkFont(weight="bold"))
        self.folder_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        # Main Content Frame
        content_frame = ctk.CTkFrame(self.window)
        content_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Left Frame - All Ping Files
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)

        left_title = ctk.CTkLabel(left_frame, text="All Ping txt",
                                  font=ctk.CTkFont(weight="bold"))
        left_title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Text widget for all files (bisa select text)
        self.all_files_text = tk.Text(left_frame, bg="#2b2b2b", fg="white",
                                      font=("Consolas", 10), wrap=tk.WORD,
                                      selectbackground="#4a4a4a", selectforeground="white",
                                      height=15, width=40)
        self.all_files_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for left text widget
        left_scrollbar = tk.Scrollbar(left_frame, command=self.all_files_text.yview)
        left_scrollbar.grid(row=1, column=1, sticky="ns")
        self.all_files_text.config(yscrollcommand=left_scrollbar.set)

        # Right Frame - Packet Loss List
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)

        self.right_title = ctk.CTkLabel(right_frame, text="Packet Loss List dari folder",
                                        font=ctk.CTkFont(weight="bold"))
        self.right_title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Text widget for packet loss files (bisa select text)
        self.packet_loss_text = tk.Text(right_frame, bg="#2b2b2b", fg="white",
                                        font=("Consolas", 10), wrap=tk.WORD,
                                        selectbackground="#4a4a4a", selectforeground="white",
                                        height=15, width=40)
        self.packet_loss_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for right text widget
        right_scrollbar = tk.Scrollbar(right_frame, command=self.packet_loss_text.yview)
        right_scrollbar.grid(row=1, column=1, sticky="ns")
        self.packet_loss_text.config(yscrollcommand=right_scrollbar.set)

        # Footer
        footer_label = ctk.CTkLabel(self.window, text="By : Heker satellit",
                                    font=ctk.CTkFont(size=12))
        footer_label.grid(row=3, column=0, padx=20, pady=10, sticky="e")

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Ping Result Files",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if files:
            self.selected_files = list(files)
            folder_path = Path(files[0]).parent
            self.current_folder = folder_path.name
            self.folder_label.configure(text=f"FOLDER: {folder_path}")
            self.update_right_title()
            self.process_files()

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder with Ping Results")

        if folder:
            folder_path = Path(folder)
            self.current_folder = folder_path.name
            self.folder_label.configure(text=f"FOLDER: {folder_path}")
            self.update_right_title()

            # Find all txt files in folder
            txt_files = list(folder_path.glob("*.txt"))
            ping_files = [f for f in txt_files if "ping" in f.name.lower()]

            self.selected_files = ping_files
            self.process_files()

    def update_right_title(self):
        if self.current_folder:
            self.right_title.configure(text=f"Packet Loss List dari folder {self.current_folder}")
        else:
            self.right_title.configure(text="Packet Loss List dari folder")

    def reset_app(self):
        self.selected_files = []
        self.packet_loss_data = []
        self.current_folder = ""
        self.folder_label.configure(text="FOLDER: ")
        self.right_title.configure(text="Packet Loss List dari folder")
        self.all_files_text.delete(1.0, tk.END)
        self.packet_loss_text.delete(1.0, tk.END)
        messagebox.showinfo("Reset", "Application has been reset!")

    def process_files(self):
        # Clear previous content
        self.all_files_text.delete(1.0, tk.END)
        self.packet_loss_text.delete(1.0, tk.END)
        self.packet_loss_data = []

        all_files_content = ""
        packet_loss_content = ""

        # Counter untuk file dengan packet loss
        files_with_loss = 0

        for file_path in self.selected_files:
            packet_loss = self.extract_packet_loss(file_path)
            display_name = f"{Path(file_path).name}    {packet_loss}% packet loss\n"

            # Add to all files content
            all_files_content += display_name

            # Add to packet loss content if loss > 0%
            if packet_loss > 0:
                formatted_info = self.format_packet_loss_info(file_path, packet_loss)
                packet_loss_content += f"{formatted_info}\n"
                self.packet_loss_data.append({
                    'file': file_path,
                    'loss': packet_loss,
                    'info': formatted_info
                })
                files_with_loss += 1

        # Insert content to text widgets
        self.all_files_text.insert(1.0, all_files_content)

        # Cek jika tidak ada packet loss sama sekali
        if files_with_loss == 0 and len(self.selected_files) > 0:
            if self.current_folder:
                packet_loss_content = f"Tidak Ada Packet Loss Sama Sekali pada Folder {self.current_folder}"
            else:
                packet_loss_content = "Tidak Ada Packet Loss Sama Sekali"

        self.packet_loss_text.insert(1.0, packet_loss_content)

    def extract_packet_loss(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Mencari pola packet loss
            pattern = r'(\d+)% packet loss'
            match = re.search(pattern, content)

            if match:
                return int(match.group(1))
            else:
                return 0

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return 0

    def format_packet_loss_info(self, file_path, packet_loss):
        filename = Path(file_path).name

        # Mapping jenis koneksi
        connection_types = {
            'aws': 'AWS',
            'vlanbras': 'BRAS',
            'vlanpe': 'PE',
            'cgnat': 'CGNAT',
            'windows': 'WINDOWS',
            'vimpe': 'VIMPE',
            'sws': 'AWS'
        }

        # Ekstrak informasi dari filename
        connection_type = "Unknown"
        date_str = "Unknown"
        time_str = "Unknown"

        # Pattern untuk filename: ping-xxx-to-yyy_YYYYMMDD_HHMMSS.txt
        pattern = r'ping-([a-zA-Z]+)-to-([a-zA-Z]+)_(\d{8})_(\d{6})\.txt'
        match = re.search(pattern, filename)

        if match:
            conn_key = match.group(2).lower()  # Ambil bagian kedua (to-xxx)
            connection_type = connection_types.get(conn_key, conn_key.upper())

            # Format tanggal
            date_part = match.group(3)
            try:
                date_obj = datetime.strptime(date_part, "%Y%m%d")
                date_str = date_obj.strftime("%d %m %Y")
            except:
                date_str = date_part

            # Format waktu
            time_part = match.group(4)
            try:
                time_obj = datetime.strptime(time_part[:4], "%H%M")
                time_str = time_obj.strftime("jam %H:%M")
            except:
                time_str = f"jam {time_part[:2]}:{time_part[2:4]}"

        return f"{connection_type} {date_str} {time_str}    {packet_loss}% packet loss"

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    # Set appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = PacketLossCheckerApp()
    app.run()