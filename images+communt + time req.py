import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import gzip
import shutil
from pathlib import Path
import base64
import time

# Define a function to open a file dialog and get the path to an image file
def get_file_path():
    root = tk.Tk()  # Create a new Tkinter window
    root.withdraw()  # Hide the window

    file_path = filedialog.askopenfilename()  # Show the file dialog and get the selected file path
    return file_path

# Define a function to compress an image file using JPEG compression
def compress_image(image_path):
    start_time = time.time()  # Get the current time
    with Image.open(image_path) as im:  # Open the image file
        # Compress the image using JPEG compression with quality 75
        im.save(image_path + ".jpg", "JPEG", optimize=True, quality=75)

        # Read the compressed image data from the temporary file
        with open(image_path + ".jpg", "rb") as f:
            compressed_data = f.read()

        # Remove the temporary compressed image file
        Path(image_path + ".jpg").unlink()

        end_time = time.time()  # Get the current time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken for compressing image: {elapsed_time:.4f} seconds")  # Print the elapsed time with 4 decimal places

        return compressed_data

# Define a function to decompress an image file
def decompress_image(image_data, image_path):
    start_time = time.time()  # Get the current time
    # Write the compressed image data to a temporary file
    with open(image_path + ".jpg", "wb") as f:
        f.write(image_data)

    # Decompress the image using JPEG
    with Image.open(image_path + ".jpg") as im:
        im.save(image_path, "JPEG")

    # Remove the temporary compressed image file
    Path(image_path + ".jpg").unlink()

    end_time = time.time()  # Get the current time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Time taken for decompressing image: {elapsed_time:.4f} seconds")  # Print the elapsed time with 4 decimal places

# Define the main function of the program
def main():
    # Get the path to an image file using the get_file_path() function
    image_path = get_file_path()

    # Compress the image using the compress_image() function
    start_time = time.time()  # Get the current time
    compressed_image_data = compress_image(image_path)
    end_time = time.time()  # Get the current time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Time taken for compressing the image and getting compressed data: {elapsed_time:.4f} seconds")  # Print the elapsed time with 4 decimal places

    # Store information about the compressed image in a dictionary
    compressed_image_info = {
        "image_name": image_path.split("/")[-1],  # Get the name of the original image file
        "compressed_image_data": base64.b64encode(gzip.compress(compressed_image_data)).decode("utf-8")  # Compress the image data using gzip and encode it with base64
    }

    # Save the compressed image information to a JSON file
    with open('compressed_image_info.json', 'w') as f:
        json.dump(compressed_image_info, f)

    # Restore and save the image in its original form
    with open('compressed_image_info.json', 'r') as f:
        compressed_image_info = json.load(f)

    start_time = time.time()  # Get the current time
    decompressed_image_data = gzip.decompress(base64.b64decode(compressed_image_info["compressed_image_data"]))  # Decode and decompress the image data
    decompress_image(decompressed_image_data, compressed_image_info["image_name"])  # Restore the image using the decompressed data
    end_time = time.time()  # Get the current time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Time taken for decoding and decompressing the image data and restoring the image: {elapsed_time:.4f} seconds")  # Print the elapsed time with 4 decimal places

    # Open the restored image using the PIL Image library
    with Image.open(compressed_image_info["image_name"]) as im:
        im.show()

    # Save the restored image using a file dialog
    new_image_path = filedialog.asksaveasfilename(defaultextension='.jpg')
    im.save(new_image_path)

# Call the main function when the program is executed
if __name__ == "__main__":
    main()