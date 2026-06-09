import os
import sys
from PIL import Image, ImageChops

sys.stdout.reconfigure(encoding='utf-8')
cat_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design\Cat mug Design"

templates = ["CAT WALLSEE.png", "cat come out.png", "cat nap.png", "cat sleep.png"]
print("Comparing Cat mug Design files:")
print("=" * 80)

for i in range(len(templates)):
    for j in range(i + 1, len(templates)):
        t1 = templates[i]
        t2 = templates[j]
        p1 = os.path.join(cat_dir, t1)
        p2 = os.path.join(cat_dir, t2)
        
        with Image.open(p1) as img1, Image.open(p2) as img2:
            img1_rgb = img1.convert('RGB')
            img2_rgb = img2.convert('RGB')
            
            # Print dimensions
            print(f"Comparing '{t1}' ({img1.size}) with '{t2}' ({img2.size})")
            
            # Check if one is a crop or resize of another, or if they are entirely different designs
            # Let's count how many pixels are different
            if img1.size == img2.size:
                diff = ImageChops.difference(img1_rgb, img2_rgb)
                stat = diff.getbbox()
                if stat is None:
                    print("  -> The images are identical!")
                else:
                    print(f"  -> Images have same size but different pixels. Diff BBox: {stat}")
            else:
                print("  -> Images have different sizes.")
                
            # Let's check grey regions overlap
            # Find grey bboxes in both
            bboxes1 = []
            bboxes2 = []
            for img, bboxes in [(img1_rgb, bboxes1), (img2_rgb, bboxes2)]:
                w, h = img.size
                grey_set = set()
                for y in range(0, h, 2):
                    for x in range(0, w, 2):
                        r, g, b = img.getpixel((x, y))
                        if abs(r - g) <= 2 and abs(g - b) <= 2 and 120 <= r <= 200:
                            grey_set.add((x, y))
                # BFS components
                visited = set()
                for p in list(grey_set):
                    if p in visited:
                        continue
                    comp = []
                    q = [p]
                    visited.add(p)
                    while q:
                        cx, cy = q.pop(0)
                        comp.append((cx, cy))
                        for dx, dy in [(-2,0), (2,0), (0,-2), (0,2)]:
                            nx, ny = cx + dx, cy + dy
                            if (nx, ny) in grey_set and (nx, ny) not in visited:
                                visited.add((nx, ny))
                                q.append((nx, ny))
                    if len(comp) > 100:
                        xs = [px[0] for px in comp]
                        ys = [px[1] for px in comp]
                        bboxes.append((min(xs), min(ys), max(xs), max(ys)))
            print(f"  '{t1}' grey bboxes: {bboxes1}")
            print(f"  '{t2}' grey bboxes: {bboxes2}")
            print("-" * 50)
