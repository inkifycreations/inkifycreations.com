import os
from PIL import Image

path = r"C:\Users\anaka\OneDrive\Pictures\mugs design\birthday\happy birthday without photose.png"

if os.path.exists(path):
    with Image.open(path) as img:
        print(f"File: {path}")
        print(f"Size: {img.size} | Mode: {img.mode}")
        if img.mode == 'RGBA':
            alpha = img.split()[-1]
            # getbbox of alpha finds the bbox of non-transparent areas.
            # To find transparent areas, we can invert the alpha channel.
            from PIL import ImageOps
            inverted_alpha = ImageOps.invert(alpha)
            trans_bbox = inverted_alpha.getbbox()
            print(f"Transparent BBox: {trans_bbox}")
            
            # Count transparent pixels
            trans_count = 0
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b, a = img.getpixel((x, y))
                    if a < 255:
                        trans_count += 1
            print(f"Total transparent pixels: {trans_count} ({trans_count / (img.width * img.height) * 100:.2f}%)")
else:
    print("File does not exist.")
