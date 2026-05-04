Compile py to exe with command below
pyinstaller --onefile --windowed --name "PacketLossChecker" --icon=l300.ico --clean --noupx --version-file file_version_info.txt --exclude-module unittest --exclude-module pydoc main.py
