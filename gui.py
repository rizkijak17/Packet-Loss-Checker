import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
from pathlib import Path
from packet_analyzer import PacketAnalyzer
from file_processor import FileProcessor


class PacketLossCheckerApp:
    def __init__(self):
        # Setup window
        self.window = ctk.CTk()
        self.window.title("Packet Loss Checker")
        self.window.geometry("900x600")

        # Configure window grid
        self.window.grid_rowconfigure(0, weight=0)  # Title
        self.window.grid_rowconfigure(1, weight=0)  # Input frame
        self.window.grid_rowconfigure(2, weight=1)  # Content frame
        self.window.grid_rowconfigure(3, weight=0)  # Footer
        self.window.grid_columnconfigure(0, weight=1)

        # Initialize components
        self.analyzer = PacketAnalyzer()
        self.file_processor = FileProcessor()

        # Variables
        self.selected_files = []
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
        input_frame.grid_rowconfigure(0, weight=1)
        input_frame.grid_rowconfigure(1, weight=1)

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
        left_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=0)  # Title
        left_frame.grid_rowconfigure(1, weight=1)  # Text widget

        left_title = ctk.CTkLabel(left_frame, text="All Ping txt",
                                  font=ctk.CTkFont(weight="bold"))
        left_title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Text widget for all files - READ ONLY
        self.all_files_text = tk.Text(left_frame, bg="#2b2b2b", fg="white",
                                      font=("Consolas", 10), wrap=tk.WORD,
                                      selectbackground="#4a4a4a", selectforeground="white",
                                      state='disabled')  # READ ONLY
        self.all_files_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Scrollbar for left text widget
        left_scrollbar = tk.Scrollbar(left_frame, command=self.all_files_text.yview)
        left_scrollbar.grid(row=1, column=1, sticky="ns")
        self.all_files_text.config(yscrollcommand=left_scrollbar.set)

        # Right Frame - Packet Loss List
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=0)  # Title
        right_frame.grid_rowconfigure(1, weight=1)  # Text widget

        self.right_title = ctk.CTkLabel(right_frame, text="Packet Loss List dari folder",
                                        font=ctk.CTkFont(weight="bold"))
        self.right_title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Text widget for packet loss files - READ ONLY
        self.packet_loss_text = tk.Text(right_frame, bg="#2b2b2b", fg="white",
                                        font=("Consolas", 10), wrap=tk.WORD,
                                        selectbackground="#4a4a4a", selectforeground="white",
                                        state='disabled')  # READ ONLY
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

            # Use file processor to get ping files
            self.selected_files = self.file_processor.get_ping_files_from_folder(folder_path)
            self.process_files()

    def update_right_title(self):
        if self.current_folder:
            self.right_title.configure(text=f"Packet Loss List dari folder {self.current_folder}")
        else:
            self.right_title.configure(text="Packet Loss List dari folder")

    def reset_app(self):
        self.selected_files = []
        self.current_folder = ""
        self.folder_label.configure(text="FOLDER: ")
        self.right_title.configure(text="Packet Loss List dari folder")

        # Clear text widgets dengan mengaktifkan sementara
        self.all_files_text.config(state='normal')
        self.packet_loss_text.config(state='normal')

        self.all_files_text.delete(1.0, tk.END)
        self.packet_loss_text.delete(1.0, tk.END)

        # Kembali ke mode read-only
        self.all_files_text.config(state='disabled')
        self.packet_loss_text.config(state='disabled')

        messagebox.showinfo("Reset", "Application has been reset!")

    def process_files(self):
        # Enable text widgets sementara untuk update content
        self.all_files_text.config(state='normal')
        self.packet_loss_text.config(state='normal')

        # Clear previous content
        self.all_files_text.delete(1.0, tk.END)
        self.packet_loss_text.delete(1.0, tk.END)

        # Process files using analyzer
        analysis_result = self.analyzer.analyze_files(self.selected_files, self.current_folder)

        # Display results
        self.all_files_text.insert(1.0, analysis_result['all_files_content'])
        self.packet_loss_text.insert(1.0, analysis_result['packet_loss_content'])

        # Kembali ke mode read-only setelah update
        self.all_files_text.config(state='disabled')
        self.packet_loss_text.config(state='disabled')

    def run(self):
        self.window.mainloop()