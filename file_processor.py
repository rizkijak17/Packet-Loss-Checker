from pathlib import Path

class FileProcessor:
    def __init__(self):
        pass

    def get_ping_files_from_folder(self, folder_path):
        """Get all ping files from a folder"""
        txt_files = list(Path(folder_path).glob("*.txt"))
        ping_files = [f for f in txt_files if "ping" in f.name.lower()]
        return ping_files

    def validate_file(self, file_path):
        """Validate if file is a valid ping result file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return "ping statistics" in content.lower()
        except:
            return False