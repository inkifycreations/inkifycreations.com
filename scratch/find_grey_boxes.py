import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
img_path = os.path.join(pictures_dir, "Cat mug Design", "CAT WALLSEE.png")

with Image.open(img_path) as img:
    img_rgb = img.convert('RGB')
    width, height = img_rgb.size
    
    # Create a set of grey pixels for O(1) lookup
    grey_set = set()
    for y in range(height):
        for x in range(width):
            r, g, b = img_rgb.getpixel((x, y))
            # Neutral grey check
            if abs(r - g) <= 2 and abs(g - b) <= 2 and 120 <= r <= 200:
                grey_set.add((x, y))
                
    print(f"Total grey pixels: {len(grey_set)}")
    
    # BFS to find connected components
    visited = set()
    components = []
    
    for pixel in grey_set:
        if pixel in visited:
            continue
        
        # Start a new component
        comp = []
        queue = [pixel]
        visited.add(pixel)
        
        while queue:
            cx, cy = queue.pop(0)
            comp.append((cx, cy))
            
            # Check 4-connected neighbors
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = cx + dx, cy + dy
                neighbor = (nx, ny)
                if neighbor in grey_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
        # Only keep components with a significant area (e.g. > 100 pixels)
        if len(comp) > 100:
            xs = [p[0] for p in comp]
            ys = [p[1] for p in comp]
            components.append({
                'bbox': (min(xs), min(ys), max(xs), max(ys)),
                'pixels': len(comp)
            })
            
    print(f"Found {len(components)} major grey components:")
    for idx, comp in enumerate(components):
        print(f"Component {idx+1}: BBox={comp['bbox']} | Pixel count={comp['pixels']}")
