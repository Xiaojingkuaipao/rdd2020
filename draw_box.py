import os
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image


filter_images_dir = "./filter_images"  
labels_dir = "./labels"              

class_id_map = {0: "d00", 1: "d10", 2: "d20", 3: "d40"}

image_files = os.listdir(filter_images_dir)
if len(image_files) < 4:
    raise ValueError("filter_images 文件夹中的图片数量不足四张！")

random_image_files = random.sample(image_files, 4)

fig, axes = plt.subplots(2, 2, figsize=(12, 12))

axes = axes.flatten()

for i, image_file in enumerate(random_image_files):
    image_path = os.path.join(filter_images_dir, image_file)
    img = Image.open(image_path)
    img_width, img_height = img.size

    label_file = os.path.splitext(image_file)[0] + ".txt"
    label_path = os.path.join(labels_dir, label_file)

    ax = axes[i]
    ax.imshow(img)
    ax.axis("off")

    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            for line in f:
                class_id, x_center, y_center, bbox_width, bbox_height = map(float, line.split())
                class_name = class_id_map[int(class_id)]

                x_min = (x_center - bbox_width / 2) * img_width
                y_min = (y_center - bbox_height / 2) * img_height
                box_width = bbox_width * img_width
                box_height = bbox_height * img_height

                # 绘制边界框
                rect = patches.Rectangle(
                    (x_min, y_min), box_width, box_height,
                    linewidth=2, edgecolor="red", facecolor="none"
                )
                ax.add_patch(rect)

                # 添加类别名称
                ax.text(
                    x_min, y_min - 5, class_name,
                    color="red", fontsize=10, weight="bold",
                    bbox=dict(facecolor="white", alpha=0.7, edgecolor="none")
                )

plt.tight_layout()
plt.show()