import os
import glob
from heapq import heapify, heappop, heappush
from collections import defaultdict
from ast import literal_eval

# Set the directory path where the files are located
#توضع المسار الذي سو ياخد المسار 
dir_path = 'data'

# Initialize variables to store sizes and relative values of different file types
# تحديد انواع المتحولات التي سوف نتعامل معها 
image_size = 0
video_size = 0
audio_size = 0
text_size = 0

# Loop through all the files in the directory
#حلقة تفحص جميغ انواع الملفات الموجودة ضمن المسار المحدد بالسطر (9)
for file_path in glob.glob(os.path.join(dir_path, '*')):

    # Get the file size in bytes
    #الحصول على احجام الملفات المتلاقاة بل bit 
    file_size = os.path.getsize(file_path)

    # Categorize the file type based on the file extension
    # تصنيف البيانات تبعا للاحقة الخاصة بها وجمع احجام البيانات المتشابهة مع بعضها
    if file_path.endswith('.jpg') or file_path.endswith('.png'):
        image_size += file_size
    elif file_path.endswith('.mp4') or file_path.endswith('.avi'):
        video_size += file_size
    elif file_path.endswith('.mp3') or file_path.endswith('.wav'):
        audio_size += file_size
    elif file_path.endswith('.txt'):
        text_size += file_size
    
    
# Calculate the total size and individual size of each file type
#حساب الحجم الكلي للملفات الموجودة ضمن المسار المحدد
total_size = (image_size + video_size + audio_size + text_size ) / 1024
# Print the total size and individual size of each file type
#طباعة الحجم المحسوب (الحجم الكلي) وطباعة الحجم للملفات حسب النوع كلا على حدا 
print(f"Total size of all files: {total_size} bytes")
print(f"Size of image files: {image_size} bytes")
print(f"Size of video files: {video_size} bytes")
print(f"Size of audio files: {audio_size} bytes")
print(f"Size of text files: {text_size} bytes")



# Calculate the relative value of each file type compared to the total size
# حساب الحجم النسبي للملفات كلا حسب النوع وذلك باخد حجم ملفات ذات النوع المحدد على حجم الملفات الكلية 
image_relative_value = image_size / total_size
video_relative_value = video_size / total_size
audio_relative_value = audio_size / total_size
text_relative_value = text_size / total_size

# Create a dictionary to store the relative values of each file type
#انشاء قاموس يخزن الحجوم النسبية ليتم استعداء الحجوم وفق مفتاح خاص بها وذلك حسب النوع
relative_values = {
    'Image': image_relative_value,
    'Video': video_relative_value,
    'Audio': audio_relative_value,
    'Text': text_relative_value,
    }

# Sort the dictionary in descending order by relative value
#ترتيب البيانات تبعا من الاعلى حجما للاصغر
sorted_relative_values = sorted(relative_values.items(), key=lambda x: x[1], reverse=True)
# sorted_relative_values = sorted(relative_values.items(), reverse=True)


# Print the sorted relative values of each file type
# طباعة الاحجام النسبية بعد ترتيبها
for file_type, relative_value in sorted_relative_values:
    print(f"{file_type}: {relative_value:.2%}")

# Create huffman tree (nodes)
# انشاء تابع لتشكيل شجرة هوفمن (العقد)
def build_huffman_tree(relative_values):
   
    # Create a priority queue of tuples (relative value, file type)
    # انشاء مكدس يخزن البيانات 
    pq = [(value, key) for key, value in relative_values.items()]
    heapify(pq)
    # heapq.heapify(pq)

    # Combine nodes until only one is left (the root)
    #جمع العقد حتى يبقى عقدة نهائية (نهاية شجرة هوفمن) وذلك عن طريق حلقة تفحص عدد العقد وتتوقف عند الوصل لعدد عقد مساوي للواحد
    while len(pq) > 1:
       
        # Pop the two nodes with the lowest relative values
        #اجمع اصغر عقدتين من حيث الحجم النسبي 
        left, right = heappop(pq), heappop(pq)
        # left, right = heapq.heappop(pq), heapq.heappop(pq)

        # Combine the nodes by creating a parent node with a relative value equal to the sum of the child nodes
        #اعطي عقدة جديدة تحوي المجموع 
        parent = (left[0] + right[0], left, right)

        # Add the parent node back to the priority queue
        #اعد العقدة الجديدة للمكدس
        heappush(pq, parent)
        # heapq.heappush(pq, parent)

    # Return the root node of the Huffman tree
    #اعد العقد الناتجة لاعطاء قيمة وفقا لتوزيع عوفمن الشجري 
    return pq[0]

root_node = build_huffman_tree(relative_values)

# Generate the Huffman code for each file type by traversing the Huffman tree
# انشاء تابع يقوم بتوليد كود هوفمن ليتم استخداماه ضمن العقدلاعطاء الكود لكل عقدة على حدا
def generate_huffman_code(node, code=''):
    
    # If the node is a leaf node (a file type), return the code
    #اذا كان العقدة هي من فرع فيمكن اعطاءها قيمة محددة
    if isinstance(node[1], str):
        return {node[1]: code}

    # Traverse the left child node and add a '0' to the code
    # اعطاء قيمة 0 للعقدة من الطرف الايسر
    left = generate_huffman_code(node[1], code + '0')

    # Traverse the right child node and add a '1' to the code
    # اعطاء قيمة 1 للعقدة من الطرف الايمن
    right = generate_huffman_code(node[2], code + '1')

    # Combine the left and right codes and return the result
    #ارجاع الكود بعد جمع الطرف الايمن والايسر 
    return {**left, **right}

huffman_codes = generate_huffman_code(root_node)

# Print the Huffman code for each file type
#طباعة كود هوفمن لكل نوع من الملفات بناء على الحجم 
Huffman_code = {}
huffman_list = []
for file_type, huffman_code in huffman_codes.items():
    print(f"file type : {file_type} , the code for it: {huffman_code}")
    huffman_list.append(huffman_code)
print(Huffman_code)
print(huffman_list)
# Define segment types and their binary representations
VIDEO_SEG = '11'
IMAGE_SEG = '10'
AUDIO_SEG = '01'
TEXT_SEG = '00'


# Create the keys for each section
key_video =  "0b1"
key_image = "01"
key_audio = "001"
key_text = "000"

# Combine the keys into a single string
total_key = key_video + key_image + key_audio + key_text

# Convert the binary string to decimal
decimal_key = int(total_key, 2)

# Convert the decimal key to a polynomial
def decimal_to_polynomial(decimal):
    binary = bin(decimal)[2:]
    degree = len(binary) - 1
    polynomial = ''
    for i in range(degree, -1, -1):
        if binary[degree-i] == '1':
            polynomial += 'x^' + str(i) + ' + '
    polynomial = polynomial[:-3]
    return polynomial

polynomial_key = decimal_to_polynomial(decimal_key)

# Print the keys and polynomial
print(f"Video key: {key_video}")
print(f"Image key: {key_image}")
print(f"Audio key: {key_audio}")
print(f"Text key: {key_text}")
print(f"Total key: {total_key}")
print(f"Decimal key: {decimal_key}")
print(f"Polynomial key: {polynomial_key}")
# Convert the polynomial key to a format that can be evaluated using Python's eval() function
eval_key = polynomial_key.replace('^', '**').replace('x', '3')

# Evaluate the polynomial key for x=1
key_value = eval(eval_key) %(total_size)

# Print the key value
print(f"The value of the polynomial key for x=1 is: {key_value}")


place = []
y=1
while True:
    # Convert the polynomial key to a format that can be evaluated using Python's eval() function
    eval_key = polynomial_key.replace('^', '**').replace('x', str(y))

# Evaluate the polynomial key for x=1
    key_value = eval(eval_key) %(total_size)
    place.append(int(key_value))
    y=y+1
   
    if y>=total_size:
        break
print(place)
import json

# قراءة الملف ال JSON
with open('compressed-data/compressed_audio_info.json', 'r') as f:
    data = json.load(f)

# قائمة المواقع المراد استخدامها لإعادة ترتيب البيانات
place = []
y=1
while True:
    # Convert the polynomial key to a format that can be evaluated using Python's eval() function
    eval_key = polynomial_key.replace('^', '**').replace('x', str(y))

    # Evaluate the polynomial key for x=1
    key_value = eval(eval_key) %(total_size)
    place.append(int(key_value))
    y=y+1
   
    if y>=total_size:
        break

