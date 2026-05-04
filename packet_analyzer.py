from pathlib import Path
import re
from datetime import datetime


class PacketAnalyzer:
    def __init__(self):
        self.connection_types = {
            'aws': 'AWS',
            'vlanbras': 'BRAS',
            'vlanpe': 'PE',
            'cgnat': 'CGNAT',
            'windows': 'WINDOWS',
            'vimpe': 'VIMPE',
            'sws': 'AWS',
            'bras': 'BRAS',
            'pe': 'PE'
        }

    def analyze_files(self, file_paths, current_folder=""):
        all_files_content = ""
        packet_loss_content = ""
        files_with_loss = 0

        for file_path in file_paths:
            packet_loss = self.extract_packet_loss(file_path)
            display_name = f"{Path(file_path).name}    {packet_loss}% packet loss\n"

            # Add to all files content
            all_files_content += display_name

            # Add to packet loss content if loss > 0%
            if packet_loss > 0:
                formatted_info = self.format_packet_loss_info(file_path, packet_loss)
                packet_loss_content += f"{formatted_info}\n"
                files_with_loss += 1

        # Check if no packet loss found
        if files_with_loss == 0 and len(file_paths) > 0:
            if current_folder:
                packet_loss_content = f"Tidak Ada Packet Loss Sama Sekali pada Folder {current_folder}"
            else:
                packet_loss_content = "Tidak Ada Packet Loss Sama Sekali"

        return {
            'all_files_content': all_files_content,
            'packet_loss_content': packet_loss_content,
            'files_with_loss': files_with_loss
        }

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

        # Ekstrak informasi dari filename
        extracted_info = self.extract_info_from_filename(filename)

        if extracted_info['recognized']:
            connection_type = extracted_info['connection_type']
            date_str = extracted_info['date_str']
            time_str = extracted_info['time_str']

            # Jika connection_type masih Unknown, gunakan nama file (tanpa ekstensi)
            if connection_type == "Unknown":
                display_name = Path(filename).stem  # Nama file tanpa .txt
                return f"{display_name} {date_str} {time_str}    {packet_loss}% packet loss"
            else:
                return f"{connection_type} {date_str} {time_str}    {packet_loss}% packet loss"
        else:
            # Format tidak dikenali sama sekali, tampilkan nama file asli
            return f"{filename}    {packet_loss}% packet loss"

    def extract_info_from_filename(self, filename):
        """Extract information from filename with multiple pattern attempts"""

        # Pattern 1: ping-xxx-to-yyy_YYYYMMDD_HHMMSS.txt (format utama)
        pattern1 = r'ping-([a-zA-Z0-9]+)-to-([a-zA-Z0-9]+)_(\d{8})_(\d{6})\.txt'
        match1 = re.search(pattern1, filename)

        if match1:
            conn_key = match1.group(2).lower()
            connection_type = self.connection_types.get(conn_key, conn_key.upper())

            date_str = self.format_date(match1.group(3))
            time_str = self.format_time(match1.group(4))

            return {
                'recognized': True,
                'connection_type': connection_type,
                'date_str': date_str,
                'time_str': time_str
            }

        # Pattern 2: ping-yyy_YYYYMMDD_HHMMSS.txt (format alternatif)
        pattern2 = r'ping-([a-zA-Z0-9]+)_(\d{8})_(\d{6})\.txt'
        match2 = re.search(pattern2, filename)

        if match2:
            conn_key = match2.group(1).lower()
            connection_type = self.connection_types.get(conn_key, conn_key.upper())

            date_str = self.format_date(match2.group(2))
            time_str = self.format_time(match2.group(3))

            return {
                'recognized': True,
                'connection_type': connection_type,
                'date_str': date_str,
                'time_str': time_str
            }

        # Pattern 3: Cari kata kunci connection type dan tanggal/waktu
        connection_type = "Unknown"
        for key, value in self.connection_types.items():
            if key in filename.lower():
                connection_type = value
                break

        # Coba ekstrak tanggal dan waktu
        date_match = re.search(r'(\d{8})', filename)
        time_match = re.search(r'(\d{6})', filename)

        date_str = self.format_date(date_match.group(1)) if date_match else "Unknown"
        time_str = self.format_time(time_match.group(1)) if time_match else "Unknown"

        # Jika berhasil ekstrak tanggal dan waktu, anggap dikenali
        if date_str != "Unknown" and time_str != "Unknown":
            return {
                'recognized': True,
                'connection_type': connection_type,
                'date_str': date_str,
                'time_str': time_str
            }
        else:
            # Benar-benar tidak dikenali
            return {
                'recognized': False,
                'filename': filename
            }

    def format_date(self, date_str):
        """Format date from YYYYMMDD to DD MM YYYY"""
        try:
            date_obj = datetime.strptime(date_str, "%Y%m%d")
            return date_obj.strftime("%d %m %Y")
        except:
            return "Unknown"

    def format_time(self, time_str):
        """Format time from HHMMSS to jam HH:MM"""
        try:
            time_obj = datetime.strptime(time_str[:4], "%H%M")
            return time_obj.strftime("jam %H:%M")
        except:
            return "Unknown"