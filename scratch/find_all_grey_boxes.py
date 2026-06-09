import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"

print("Scanning all design/template files for grey placeholder boxes...")
print("-" * 100)

for root, dirs, files in os.walk(pictures_dir):
    for name in files:
        if name.lower().endswith(('.png', '.jpg', '.jpeg')):
            # We target files that are likely templates
            # e.g., containing 'without', 'design', 'wallsee', 'awesome', 'best', etc.
            # Or we can just scan all files that have at least one significant grey component.
            full_path = os.path.join(root, name)
            try:
                with Image.open(full_path) as img:
                    img_rgb = img.convert('RGB')
                    width, height = img_rgb.size
                    
                    # Search for neutral grey pixels
                    grey_set = set()
                    for y in range(0, height, 2):  # Step by 2 for speed
                        for x in range(0, width, 2):
                            r, g, b = img_rgb.getpixel((x, y))
                            if abs(r - g) <= 2 and abs(g - b) <= 2 and 120 <= r <= 200:
                                grey_set.add((x, y))
                    
                    if len(grey_set) < 200:
                        continue  # Not a template or no placeholders
                        
                    # BFS to find connected components
                    visited = set()
                    components = []
                    
                    # Convert grey_set to a list for iteration
                    for pixel in list(grey_set):
                        if pixel in visited:
                            continue
                        
                        comp = []
                        queue = [pixel]
                        visited.add(pixel)
                        
                        while queue:
                            cx, cy = queue.pop(0)
                            comp.append((cx, cy))
                            
                            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2)]:
                                nx, ny = cx + dx, cy + dy
                                neighbor = (nx, ny)
                                if neighbor in grey_set and neighbor not in visited:
                                    visited.add(neighbor)
                                    queue.append(neighbor)
                                    
                        if len(comp) > 150:  # Significant size
                            xs = [p[0] for p in comp]
                            ys = [p[1] for p in comp]
                            # Multiply back by 2 for original coordinates
                            components.append({
                                'bbox': (min(xs), min(ys), max(xs), max(ys)),
                                'pixels': len(comp) * 4
                            })
                            
                    if components:
                        rel_path = os.path.relpath(full_path, pictures_dir)
                        print(f"\nFile: {rel_path} (Size: {width}x{height})")
                        for idx, comp in enumerate(components):
                            print(f"  Component {idx+1}: BBox={comp['bbox']} | Est. Pixel Count={comp['pixels']}")
            except Exception as e:
                pass
print("-" * 100)
