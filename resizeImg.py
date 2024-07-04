from PIL import Image
import os

input_folder = "data/Trang Phục Người Tày"
output_folder = "data/Trang Phục Người Tày"
output_size = (800, 800)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
file_list = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])
for i, filename in enumerate(file_list):
    i = i+148
    img = Image.open(os.path.join(input_folder, filename))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img_resized = img.resize(output_size, Image.LANCZOS)
    new_filename = f"{i}.jpg"
    img_resized.save(os.path.join(output_folder, new_filename), 'JPEG')

print("Hoàn thành việc resize và chuẩn hóa định dạng tất cả các ảnh.")
