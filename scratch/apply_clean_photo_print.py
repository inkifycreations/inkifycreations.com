import os
import shutil

assets_dir = "assets"
original_path = os.path.join(assets_dir, "mug_photo_print.png")
backup_path = os.path.join(assets_dir, "mug_photo_print_original.png")
cleaned_path = os.path.join(assets_dir, "mug_photo_print_clean.png")

if os.path.exists(original_path):
    if not os.path.exists(backup_path):
        shutil.copy2(original_path, backup_path)
        print(f"Backed up original mug_photo_print.png to {backup_path}")
    else:
        print(f"Backup already exists at {backup_path}")

if os.path.exists(cleaned_path):
    shutil.copy2(cleaned_path, original_path)
    print(f"Replaced {original_path} with cleaned blank mug!")
else:
    print(f"Error: Cleaned image not found at {cleaned_path}!")
