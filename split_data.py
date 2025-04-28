"""
此文件用于划分训练集和验证集，将filter_images文件夹下的图片和对应labels文件夹下的标签
随机分为训练集和验证集，并放到同目录下的train和val文件夹下面
"""
import os
import random
import shutil


images_dir = "./filter_images"       # 原始图片文件夹
labels_dir = "./labels"       # 原始标签文件夹

output_images_train_dir = "./filter_images/train"  # 训练集图片文件夹
output_images_val_dir = "./filter_images/val"      # 验证集图片文件夹
output_labels_train_dir = "./labels/train"  # 训练集标签文件夹
output_labels_val_dir = "./labels/val"      # 验证集标签文件夹


os.makedirs(output_images_train_dir, exist_ok=True)
os.makedirs(output_images_val_dir, exist_ok=True)
os.makedirs(output_labels_train_dir, exist_ok=True)
os.makedirs(output_labels_val_dir, exist_ok=True)


image_files = [f for f in os.listdir(images_dir) if f.endswith((".jpg", ".png"))]

# 随机打乱图片文件名
random.seed(42)  # 固定随机种子，确保结果可复现
random.shuffle(image_files)

# 划分训练集和验证集
train_ratio = 0.8
split_index = int(len(image_files) * train_ratio)
train_images = image_files[:split_index]
val_images = image_files[split_index:]

# 辅助函数：复制文件到目标文件夹
def copy_files(file_list, src_images_dir, src_labels_dir, dst_images_dir, dst_labels_dir):
    for file in file_list:
        # 复制图片
        src_image_path = os.path.join(src_images_dir, file)
        dst_image_path = os.path.join(dst_images_dir, file)
        shutil.copy(src_image_path, dst_image_path)

        # 复制对应的标签文件
        label_file = os.path.splitext(file)[0] + ".txt"
        src_label_path = os.path.join(src_labels_dir, label_file)
        dst_label_path = os.path.join(dst_labels_dir, label_file)
        if os.path.exists(src_label_path):  # 确保标签文件存在
            shutil.copy(src_label_path, dst_label_path)

# 复制训练集图片和标签
copy_files(train_images, images_dir, labels_dir, output_images_train_dir, output_labels_train_dir)

# 复制验证集图片和标签
copy_files(val_images, images_dir, labels_dir, output_images_val_dir, output_labels_val_dir)

print(f"数据集划分完成！")
print(f"训练集图片数量: {len(train_images)}")
print(f"验证集图片数量: {len(val_images)}")