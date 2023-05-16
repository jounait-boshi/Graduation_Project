import json
import tkinter as tk
from tkinter import filedialog
import zlib
import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import gzip
import shutil
from pathlib import Path
import base64


def get_file_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path


def compress_text(text):
    # Convert the text to bytes
    compressed_text = zlib.compress(bytes(text, 'utf-8'))

    # Convert the compressed text to Base64-encoded string
    compressed_text_b64 = compressed_text.hex()

    return compressed_text_b64


def decompress_text(compressed_text_b64):
    # Decode the Base64-encoded string
    compressed_text = bytes.fromhex(compressed_text_b64)

    # Decompress the text
    text = zlib.decompress(compressed_text)

    # Convert the decompressed text to string
    text = text.decode('utf-8')

    return text


def main():
    # Get file path
    file_path = get_file_path()

    # Read the text file
    with open(file_path, 'r') as f:
        text = f.read()

    # Compress the text
    compressed_text_b64 = compress_text(text)

    # Store compressed text information in JSON
    compressed_text_info = {
        "file_name": file_path.split("/")[-1],
        "compressed_text": compressed_text_b64
    }

    with open('compressed_text_info.json', 'w') as f:
        json.dump(compressed_text_info, f)

    # Restore and save text in its original form
    with open('compressed_text_info.json', 'r') as f:
        compressed_text_info = json.load(f)

    text = decompress_text(compressed_text_info["compressed_text"])

    # Save the restored text in a new file
    new_file_path = filedialog.asksaveasfilename(defaultextension='.txt')
    with open(new_file_path, 'w') as f:
        f.write(text)

    # Show the restored text
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showinfo(title='Restored Text', message=text)


if __name__ == "__main__":
    main()