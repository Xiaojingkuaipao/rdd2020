"""
此文件用于统计RDDC2020数据集中各个类别出现的频数
"""
import os
import xml.etree.ElementTree as ET
import tqdm
 
 
def xml_parse(target):
    """
    Arguments:
        target (annotation) : the target annotation to be made usable
            will be an ET.Element
    Returns:
        a list containing lists of bounding boxes  [bbox coords, class name]
    """
    res = []
    for obj in target.iter("object"):
        name = obj.find("name").text.strip()
        bbox = obj.find("bndbox")
 
        pts = ["xmin", "ymin", "xmax", "ymax"]
        bndbox = [name]
        for i, pt in enumerate(pts):
            cur_pt = int(float(bbox.find(pt).text))
            # scale height or width
            # cur_pt = cur_pt / width if i % 2 == 0 else cur_pt / height
            bndbox.append(cur_pt)
 
        res.append(bndbox)  # [xmin, ymin, xmax, ymax, label_name]
        # img_id = target.find('filename').text[:-4]
 
    return res  # [[xmin, ymin, xmax, ymax, label_ind], ... ]
 
 
if __name__ == '__main__':
    raw_path = "./train"
    sub_dirs = ["Czech", "India", "Japan"]
 
    statistic = {}
    for sub_dir in sub_dirs:
        img_path_root = os.path.join(raw_path, sub_dir, 'images')
        xml_path_root = os.path.join(raw_path, sub_dir, 'annotations', 'xmls')
        for f in tqdm.tqdm(os.listdir(img_path_root), ncols=100):
 
            # parse xml
            xml_path = os.path.join(xml_path_root, os.path.splitext(f)[0]+'.xml')
            target = ET.parse(xml_path)
            res = xml_parse(target)
 
 
            for r in res:
                cls = r[0]
                # statistic
                if cls not in statistic.keys():
                    statistic[cls] = 1
                else:
                    statistic[cls] += 1
 
    print(statistic)
    for key in sorted(statistic):
        print(f"{key}: {statistic[key]}")