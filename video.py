import json
import tkinter as tk
from tkinter import filedialog
import base64
import subprocess
import os
import time


def get_file_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path


def compress_video(video_path):
    # Compress the video using ffmpeg
    compressed_video_path = video_path + '_compressed.mp4'

    start_time = time.time()  # تبدأ عملية حساب وقت الضغط
    subprocess.call(['ffmpeg', '-i', video_path, '-vcodec', 'libx264', '-preset', 'fast', '-crf', '18', '-b:v', '5M', '-maxrate', '5M', '-bufsize', '10M', compressed_video_path])
    end_time = time.time()  # تنتهي عملية حساب وقت الضغط

    # Read compressed video data
    with open(compressed_video_path, 'rb') as f:
        compressed_video_data = f.read()

    # Convert compressed video data to Base64-encoded string
    compressed_video_b64 = base64.b64encode(compressed_video_data).decode('utf-8')

    # Remove the temporary compressed video file
    os.remove(compressed_video_path)

    return compressed_video_b64, end_time - start_time  # تعيد النتيجة بالإضافة إلى وقت الضغط


def decompress_video(compressed_video_b64, video_path):
    # Decode the Base64-encoded string
    compressed_video_data = base64.b64decode(compressed_video_b64)

    # Write compressed video data to file
    compressed_video_path = video_path + '_compressed.mp4'
    with open(compressed_video_path, 'wb') as f:
        f.write(compressed_video_data)

    # Decompress the video using ffmpeg
    decompressed_video_path = video_path.split("/")[-1]

    start_time = time.time()  # تبدأ عملية حساب وقت فك الضغط
    subprocess.call(['ffmpeg', '-i', compressed_video_path, '-c', 'copy', decompressed_video_path])
    end_time = time.time()  # تنتهي عملية حساب وقت فك الضغط

    # Remove the temporary compressed video file
    os.remove(compressed_video_path)

    return decompressed_video_path, end_time - start_time  # تعيد النتيجة بالإضافة إلى وقت فك الضغط


def main():
    # Get video path
    video_path = get_file_path()

    # Compress the video
    compressed_video_b64, compression_time = compress_video(video_path)

    # Store compressed video information in JSON
    compressed_video_info = {
        "video_name": video_path.split("/")[-1],
        "compressed_video": compressed_video_b64
    }

    with open('compressed_video_info.json', 'w') as f:
        json.dump(compressed_video_info, f)

    # Restore and save video in its original form
    with open('compressed_video_info.json', 'r') as f:
        compressed_video_info = json.load(f)

    decompressed_video_path, decompression_time = decompress_video(compressed_video_info["compressed_video"], compressed_video_info["video_name"])

    # Show the restored video
    root = tk.Tk()
    root.withdraw()
    subprocess.call(['start', decompressed_video_path], shell=True)

    # Save the restored video
    subprocess.call(['copy', decompressed_video_path, video_path], shell=True)

    # Convert the time to minutes and seconds
    compression_min, compression_sec = divmod(compression_time, 60)
    decompression_min, decompression_sec = divmod(decompression_time, 60)

    # Print compression and decompression times
    print("Compression time: {} minutes, {:.2f} miles seconds".format(int(compression_min), compression_sec*1000))
    print("Decompression time: {} minutes, {:.2f} miles seconds".format(int(decompression_min), decompression_sec*1000))


if __name__ == "__main__":
    main()