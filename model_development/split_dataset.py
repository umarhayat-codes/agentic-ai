import os
import shutil
import random

# Source folders
source_dir = "archive"

# Target base folder
base_dataset_dir = "dataset"
train_dir = os.path.join(base_dataset_dir, "training")
val_dir = os.path.join(base_dataset_dir, "validation")

# Categories
categories = ["cats", "dogs"]

# Create directory structure
for folder in [train_dir, val_dir]:
    for category in categories:
        os.makedirs(os.path.join(folder, category), exist_ok=True)

# Function to split and copy images
def split_and_copy(category):
    src_folder = os.path.join(source_dir, category)
    images = os.listdir(src_folder)
    random.shuffle(images)

    split_idx = int(0.8 * len(images))
    train_imgs = images[:split_idx]
    val_imgs = images[split_idx:]

    for img in train_imgs:
        shutil.copy(os.path.join(src_folder, img),
                    os.path.join(train_dir, category, img))

    for img in val_imgs:
        shutil.copy(os.path.join(src_folder, img),
                    os.path.join(val_dir, category, img))

# Run for each category
for cat in categories:
    split_and_copy(cat)

print("Dataset folders created and images distributed successfully!")
