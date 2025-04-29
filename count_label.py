import os
import xml.etree.ElementTree as ET
from collections import defaultdict

def count_labels(root_dir):
    label_counts = defaultdict(int)
    
    # Walk through all subdirectories
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.xml'):
                xml_path = os.path.join(dirpath, filename)
                try:
                    tree = ET.parse(xml_path)
                    root = tree.getroot()
                    
                    # Count each object's name in the XML
                    for obj in root.findall('object'):
                        name = obj.find('name').text
                        label_counts[name] += 1
                except Exception as e:
                    print(f"Error parsing {xml_path}: {e}")
    
    return label_counts

if __name__ == "__main__":
    train_dir = os.path.join('train')
    counts = count_labels(train_dir)
    
    print("Label counts:")
    for label, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{label}: {count}")
