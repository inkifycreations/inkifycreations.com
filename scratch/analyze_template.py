import os
from PIL import Image
from collections import Counter

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
img_path = os.path.join(pictures_dir, "Cat mug Design", "CAT WALLSEE.png")

print(f"Analyzing: {img_path}")
with Image.open(img_path) as img:
    print(f"Size: {img.size} | Mode: {img.mode}")
    img_rgb = img.convert('RGB')
    width, height = img_rgb.size
    
    # Let's count color frequencies to see if there are dominant colors
    pixels = list(img_rgb.getdata())
    counter = Counter(pixels)
    most_common = counter.most_common(10)
    print("Most common colors:")
    for color, count in most_common:
        print(f"Color: {color} | Count: {count} ({count*100/(width*height):.2f}%)")

    # Let's write a function to find large solid color rectangles
    # In templates, a placeholder is often a solid grey (e.g. RGB around 200, 200, 200)
    # or solid black/white. Let's print the colors of a grid of points.
    print("\nColor grid (10x10):")
    for y in range(0, height, height // 10):
        row = []
        for x in range(0, width, width // 10):
            row.append(str(img_rgb.getpixel((x, y))))
        print(" | ".join(row))
