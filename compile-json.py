import json

# Read the contents of each file
with open('compressed-data/compressed_audio_info.json', 'r') as f:
    audio_data = json.load(f)

with open('compressed-data/compressed_text_info.json', 'r') as f:
    text_data = json.load(f)

with open('compressed-data/compressed_video_info.json', 'r') as f:
    video_data = json.load(f)

with open('compressed-data/compressed_image_info.json', 'r') as f:
    image_data = json.load(f)

# Combine the data into a new dictionary
combined_data = {
    'audio': audio_data,
    'text': text_data,
    'video': video_data,
    'image': image_data
}

# Save the combined data to a new file
with open('compressed-data/combined_data.json', 'w') as f:
    json.dump(combined_data, f)