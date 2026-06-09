import os
from PIL import Image

assets_dir = "assets"
mug_images = ["mug.png", "mug_photo_print.png"]

for name in mug_images:
    path = os.path.join(assets_dir, name)
    if os.path.exists(path):
        with Image.open(path) as img:
            print(f"File: {name} | Size: {img.size} | Mode: {img.mode}")
    else:
        print(f"File: {name} does not exist!")
