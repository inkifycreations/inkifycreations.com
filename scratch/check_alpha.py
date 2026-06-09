import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"

for root, dirs, files in os.walk(pictures_dir):
    for name in files:
        if name.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_path = os.path.join(root, name)
            try:
                with Image.open(full_path) as img:
                    rel_path = os.path.relpath(full_path, pictures_dir)
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        # Check if there are actual transparent pixels (alpha < 255)
                        alpha = img.convert('RGBA').split()[-1]
                        bbox = alpha.getbbox()
                        # getbbox returns None if the image is entirely transparent,
                        # and returns a bounding box of non-transparent areas.
                        # We check if there are any pixels with alpha < 255
                        extrema = alpha.getextrema()
                        has_transparency = extrema[0] < 255
                        print(f"{rel_path} | Mode: {img.mode} | Extrema: {extrema} | Has trans: {has_transparency}")
                    else:
                        print(f"{rel_path} | Mode: {img.mode} | No alpha channel")
            except Exception as e:
                print(f"Error {name}: {e}")
