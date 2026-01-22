import os
import pandas as pd
from pathlib import Path

CSV_PATH = r"C:\Users\ASUS\Desktop\saurabh\newproject\backend\data\fashion_metadata.csv"
IMAGE_DIR = Path(r"C:\Users\ASUS\Desktop\saurabh\newproject\frontend\static\images")
IMAGE_EXT = ".jpg"

df = pd.read_csv(CSV_PATH)

# Expected correct filenames from CSV
expected_names = {str(i) + IMAGE_EXT for i in df["image_id"]}

# Current images on disk
disk_images = {p.name: p for p in IMAGE_DIR.iterdir() if p.is_file()}

# Find images that are NOT correctly named
incorrect_images = [
    p for name, p in disk_images.items()
    if name not in expected_names
]

# Find image_ids that are still missing
missing_ids = [
    str(i) for i in df["image_id"]
    if str(i) + IMAGE_EXT not in disk_images
]

print("Images to fix:", len(incorrect_images))
print("IDs missing:", len(missing_ids))

# Rename safely
renamed = 0
for img_path, image_id in zip(incorrect_images, missing_ids):
    new_name = image_id + IMAGE_EXT
    new_path = IMAGE_DIR / new_name

    os.rename(img_path, new_path)
    renamed += 1

print("================================")
print(f"Renamed (final pass): {renamed}")
print("DONE.")
