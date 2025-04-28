"""
此文件用于将images文件夹中以及xmls文件夹中的图片以及标签根据指定的类别进行过滤
并将过滤好的图片放入filter_images文件夹中，将xml标注转化成YOLO格式放在labels文件夹下
"""

import os
import xml.etree.ElementTree as ET
import shutil
import json

# 定义路径
xmls_dir = "./xmls"  # 原始 XML 文件夹
images_dir = "./images"  # 原始图片文件夹
output_labels_dir = "./labels"  # 存放转换后的 YOLO 标签文件
output_images_dir = "./filter_images"  # 存放筛选后的图片
class_mapping_file = "./class_mapping.json"  # 类别 ID 映射文件

# 创建目标文件夹
os.makedirs(output_labels_dir, exist_ok=True)
os.makedirs(output_images_dir, exist_ok=True)

# 定义需要保留的类别及其 ID 映射
class_names = ["d00", "d10", "d20", "d40"]
class_id_map = {cls: idx for idx, cls in enumerate(class_names)}

# 初始化统计信息
processed_images_count = 0
skipped_images_count = 0

# 遍历所有 XML 文件
for xml_file in os.listdir(xmls_dir):
    if not xml_file.endswith(".xml"):
        continue  # 跳过非 XML 文件

    xml_path = os.path.join(xmls_dir, xml_file)
    image_name = os.path.splitext(xml_file)[0] + ".jpg"  # 对应的图片文件名
    image_path = os.path.join(images_dir, image_name)

    # 检查对应的图片是否存在
    if not os.path.exists(image_path):
        print(f"图片不存在，跳过 XML 文件: {xml_file}")
        continue

    try:
        # 解析 XML 文件
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 获取图片尺寸
        size = root.find("size")
        width = int(size.find("width").text)
        height = int(size.find("height").text)

        # 查找所有 <object> 标签
        objects = root.findall("object")

        # 筛选符合条件的目标
        valid_objects = []
        for obj in objects:
            name = obj.find("name").text.strip().lower()  # 类别名称统一转为小写
            if name in class_id_map:  # 只保留指定的类别
                bbox = obj.find("bndbox")
                xmin = float(bbox.find("xmin").text)
                ymin = float(bbox.find("ymin").text)
                xmax = float(bbox.find("xmax").text)
                ymax = float(bbox.find("ymax").text)

                # 转换为 YOLO 格式：[class_id, x_center, y_center, width, height]
                x_center = (xmin + xmax) / 2.0 / width
                y_center = (ymin + ymax) / 2.0 / height
                bbox_width = (xmax - xmin) / width
                bbox_height = (ymax - ymin) / height

                valid_objects.append([class_id_map[name], x_center, y_center, bbox_width, bbox_height])

        # 如果没有符合条件的目标，则跳过该图片和 XML 文件
        if not valid_objects:
            skipped_images_count += 1
            continue

        # 处理符合条件的图片和标签
        processed_images_count += 1

        # 保存 YOLO 格式的标签文件
        label_file_name = os.path.splitext(xml_file)[0] + ".txt"
        label_path = os.path.join(output_labels_dir, label_file_name)
        with open(label_path, "w") as f:
            for obj in valid_objects:
                f.write(" ".join(map(str, obj)) + "\n")

        # 复制对应的图片到 filter_images 文件夹
        target_image_path = os.path.join(output_images_dir, image_name)
        shutil.copy(image_path, target_image_path)

    except Exception as e:
        print(f"处理 XML 文件时出错: {xml_path}, 错误信息: {e}")

# 保存类别 ID 映射到 JSON 文件
with open(class_mapping_file, "w") as f:
    json.dump({str(idx): cls for cls, idx in class_id_map.items()}, f, indent=4)

print(f"处理完成！共处理 {processed_images_count} 张图片，跳过 {skipped_images_count} 张图片。")
print(f"类别 ID 映射已保存到 {class_mapping_file}")