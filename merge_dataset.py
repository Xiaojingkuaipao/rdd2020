"""
将rddc2020数据集的图片和xml标注文件都放到一起，分别放到images和labels文件夹下面
并过滤没有标注信息的图片
"""
import os
import xml.etree.ElementTree as ET
import shutil

raw_path = "./train"
output_images_dir = "./images"  
output_xmls_dir = "./xmls"  

os.makedirs(output_images_dir, exist_ok=True)
os.makedirs(output_xmls_dir, exist_ok=True)


sub_dirs = ["Czech", "India", "Japan"]


for sub_dir in sub_dirs:
    img_path_root = os.path.join(raw_path, sub_dir, 'images')
    xml_path_root = os.path.join(raw_path, sub_dir, 'annotations', 'xmls')

    for img_file in os.listdir(img_path_root):
        img_file_path = os.path.join(img_path_root, img_file)
        xml_file_name = os.path.splitext(img_file)[0] + '.xml'  # 对应的 XML 文件名
        xml_file_path = os.path.join(xml_path_root, xml_file_name)


        if os.path.exists(xml_file_path):
            try:
                tree = ET.parse(xml_file_path)
                root = tree.getroot()

                # 检查是否有 <object> 标签
                objects = root.findall("object")
                if len(objects) > 0:  # 如果有目标检测的标注信息
                    target_img_path = os.path.join(output_images_dir, img_file)
                    target_xml_path = os.path.join(output_xmls_dir, xml_file_name)

                    shutil.copy(img_file_path, target_img_path)
                    shutil.copy(xml_file_path, target_xml_path)
            except ET.ParseError:
                print(f"XML 文件解析错误，跳过文件: {xml_file_path}")

print("整合完成！图片和标签文件已分别存放在 images 和 xmls 文件夹中。")