import jsonlines
import os
import json
import tkinter as tk
from tkinter import filedialog
import zlib
import time

# Define the chunk size in bytes (8 KB)
CHUNK_SIZE = 1 * 512

def get_file_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path

def compress_text(text):
    # Divide the text into chunks of size CHUNK_SIZE
    chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]

    # Compress each chunk and store the compressed text in a list
    compressed_chunks = []
    for chunk in chunks:
        compressed_chunk = zlib.compress(bytes(chunk, 'utf-8'))
        compressed_chunk_b64 = compressed_chunk.hex()
        compressed_chunks.append(compressed_chunk_b64)

    return compressed_chunks

def decompress_text(compressed_text_chunks):
    # Decompress each chunk and store the decompressed text in a list
    decompressed_chunks = []
    for compressed_chunk_b64 in compressed_text_chunks:
        compressed_chunk = bytes.fromhex(compressed_chunk_b64)
        decompressed_chunk = zlib.decompress(compressed_chunk)
        decompressed_chunk = decompressed_chunk.decode('utf-8')
        decompressed_chunks.append(decompressed_chunk)

    # Join the decompressed chunks into a single string
    text = ''.join(decompressed_chunks)

    return text

def main():
    # Get file path
    file_path = get_file_path()

    # Read the text file
    with open(file_path, 'r') as f:
        text = f.read()

    # Compress the text
    start_time = time.time()
    compressed_text_chunks = compress_text(text)
    end_time = time.time()

    compression_time = end_time - start_time

    # Store compressed text information in JSONLines
    file_name = os.path.basename(file_path)
    with jsonlines.open('compressed-data/combined_data.json', mode='w') as writer:
        chunk_info = {
            "file_name": file_name,
            "compressed_chunks": compressed_text_chunks
        }
        writer.write(chunk_info)

    # Restore and save text in its original form
    with jsonlines.open('compressed-data/combined_data.json', mode='r') as reader:
        chunk_info = reader.read()
        compressed_text_chunks = chunk_info["compressed_chunks"]
    
    text = decompress_text(compressed_text_chunks)

    # Save the restored text in a new file
    new_file_path = filedialog.asksaveasfilename(defaultextension='.txt')
    with open(new_file_path, 'w') as f:
        f.write(text)

    # Calculate decompression time and show the restored text and compression/decompression time
    start_time = time.time()
    text = decompress_text(compressed_text_chunks)
    end_time = time.time()

    decompression_time = end_time - start_time

    print(f'Restored Text: {text}')
    print(f'Compression Time: {round(compression_time*1000, 8)} miles seconds')
    print(f'Decompression Time: {round(decompression_time*1000, 8)} miles seconds')


if __name__ == "__main__":
    main()