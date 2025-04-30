import os
import shutil

# Original dataset directory
source_dir = "archive"

# Target dataset directory
target_dir = "dataset"

# Define emotions
emotions = ["angry", "happy"]

# Define dataset types
dataset_types = ["train", "test"]

# Create the new structure
for dtype in dataset_types:
    for emotion in emotions:
        os.makedirs(os.path.join(target_dir, dtype, emotion), exist_ok=True)

# Copy files from original folders to new structure
for dtype in dataset_types:
    for emotion in emotions:
        src_folder = os.path.join(source_dir, dtype, emotion)
        dest_folder = os.path.join(target_dir, dtype, emotion)

        if os.path.exists(src_folder):
            for img_file in os.listdir(src_folder):
                full_src_path = os.path.join(src_folder, img_file)
                full_dest_path = os.path.join(dest_folder, img_file)
                shutil.copy(full_src_path, full_dest_path)

print("Facial Emotion dataset copied successfully into new structure!")
