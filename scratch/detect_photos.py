import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"

templates = {}
photos = {}

for root, dirs, files in os.walk(pictures_dir):
    folder_name = os.path.relpath(root, pictures_dir)
    for name in files:
        if name.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_path = os.path.join(root, name)
            try:
                with Image.open(full_path) as img:
                    img_rgb = img.convert('RGB')
                    width, height = img_rgb.size
                    
                    # Search for neutral grey pixels
                    grey_count = 0
                    for y in range(0, height, 4):  # Step by 4 for speed
                        for x in range(0, width, 4):
                            r, g, b = img_rgb.getpixel((x, y))
                            if abs(r - g) <= 2 and abs(g - b) <= 2 and 120 <= r <= 200:
                                grey_count += 1
                                
                    # If grey pixels make up a significant portion of the image, it's a template
                    total_sampled = (width // 4) * (height // 4)
                    grey_ratio = grey_count / total_sampled if total_sampled > 0 else 0
                    
                    if folder_name not in templates:
                        templates[folder_name] = []
                    if folder_name not in photos:
                        photos[folder_name] = []
                        
                    rel_path = os.path.relpath(full_path, pictures_dir)
                    if grey_ratio > 0.05:  # Over 5% grey sampled pixels
                        templates[folder_name].append((name, img.size, grey_ratio))
                    else:
                        photos[folder_name].append((name, img.size, grey_ratio))
            except Exception as e:
                print(f"Error {name}: {e}")

print("CLASSIFICATION REPORT:")
print("=" * 80)
for folder in sorted(templates.keys()):
    print(f"\nFolder: '{folder}'")
    print("  Templates:")
    for t in templates[folder]:
        print(f"    - {t[0]} ({t[1][0]}x{t[1][1]}) | Grey Ratio: {t[2]:.2%}")
    print("  Photos:")
    for p in photos[folder]:
        print(f"    - {p[0]} ({p[1][0]}x{p[1][1]})")
print("=" * 80)
