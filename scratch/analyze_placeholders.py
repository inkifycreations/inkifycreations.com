import os
from PIL import Image

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
img_path = os.path.join(pictures_dir, "Cat mug Design", "CAT WALLSEE.png")

with Image.open(img_path) as img:
    img_rgb = img.convert('RGB')
    width, height = img_rgb.size
    
    # BBoxes from earlier run:
    # Component 1: BBox=(453, 41, 740, 677)
    # Component 2: BBox=(8, 232, 133, 549)
    
    bboxes = [
        (453, 41, 740, 677),
        (8, 232, 133, 549)
    ]
    
    for idx, (x1, y1, x2, y2) in enumerate(bboxes):
        total_pixels = (x2 - x1 + 1) * (y2 - y1 + 1)
        grey_pixels = 0
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                r, g, b = img_rgb.getpixel((x, y))
                if abs(r - g) <= 2 and abs(g - b) <= 2 and 120 <= r <= 200:
                    grey_pixels += 1
        pct = (grey_pixels / total_pixels) * 100
        print(f"BBox {idx+1}: {x1, y1, x2, y2} | Total pixels: {total_pixels} | Grey pixels: {grey_pixels} ({pct:.2f}%)")
