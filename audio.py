import json
import tkinter as tk
from tkinter import filedialog
import base64
from pydub import AudioSegment
import os
import subprocess


def get_file_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path


def compress_audio(audio_path):
    # Compress the audio using pydub
    compressed_audio_path = audio_path + '_compressed.mp3'
    audio = AudioSegment.from_file(audio_path)
    audio.export(compressed_audio_path, format='mp3', bitrate='64k')

    # Read compressed audio data
    with open(compressed_audio_path, 'rb') as f:
        compressed_audio_data = f.read()

    # Convert compressed audio data to Base64-encoded string
    compressed_audio_b64 = base64.b64encode(compressed_audio_data).decode('utf-8')

    # Remove the temporary compressed audio file
    os.remove(compressed_audio_path)

    return compressed_audio_b64


def decompress_audio(compressed_audio_b64, audio_path):
    # Decode the Base64-encoded string
    compressed_audio_data = base64.b64decode(compressed_audio_b64)

    # Write compressed audio data to file
    compressed_audio_path = audio_path + '_compressed.mp3'
    with open(compressed_audio_path, 'wb') as f:
        f.write(compressed_audio_data)

    # Decompress the audio using pydub
    audio = AudioSegment.from_file(compressed_audio_path)
    audio.export(audio_path, format='wav')

    # Remove the temporary compressed audio file
    os.remove(compressed_audio_path)


def main():
    # Get audio path
    audio_path = get_file_path()

    # Compress the audio
    compressed_audio_b64 = compress_audio(audio_path)

    # Store compressed audio information in JSON
    compressed_audio_info = {
        "audio_name": audio_path.split("/")[-1],
        "compressed_audio": compressed_audio_b64
    }

    with open('compressed_audio_info.json', 'w') as f:
        json.dump(compressed_audio_info, f)

    # Restore and save audio in its original form
    with open('compressed_audio_info.json', 'r') as f:
        compressed_audio_info = json.load(f)

    decompress_audio(compressed_audio_info["compressed_audio"], compressed_audio_info["audio_name"])

    # Show the restored audio
    subprocess.call(['start', compressed_audio_info["audio_name"]], shell=True)

    # Save the restored audio
    new_audio_path = filedialog.asksaveasfilename(defaultextension='.wav')
    subprocess.call(['cp', compressed_audio_info["audio_name"], new_audio_path])


if __name__ == "__main__":
    main()