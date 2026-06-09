import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
output_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design\outputs"

print("VERIFYING GENERATED OUTPUT WRAPS:")
print("=" * 80)

verified_count = 0
error_count = 0

for root, dirs, files in os.walk(output_dir):
    for name in sorted(files):
        if name.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(root, name)
            rel_path = os.path.relpath(path, output_dir)
            try:
                with Image.open(path) as img:
                    w, h = img.size
                    dpi = img.info.get('dpi')
                    
                    # Check for grey pixels in the output
                    img_rgb = img.convert('RGB')
                    grey_pixels = 0
                    for y in range(0, h, 4):
                        for x in range(0, w, 4):
                            r, g, b = img_rgb.getpixel((x, y))
                            if abs(r - g) <= 3 and abs(g - b) <= 3 and 110 <= r <= 210:
                                grey_pixels += 1
                    
                    total_sampled = (w // 4) * (h // 4)
                    grey_ratio = (grey_pixels / total_sampled) * 100 if total_sampled > 0 else 0
                    
                    print(f"  - {rel_path:50s} | Size: {w:4d}x{h:4d} | DPI: {dpi} | Remaining Grey: {grey_ratio:.2f}%")
                    verified_count += 1
            except Exception as e:
                print(f"  - {rel_path:50s} | Error: {e}")
                error_count += 1

print("=" * 80)
print(f"Verification finished: {verified_count} verified successfully, {error_count} errors.")
