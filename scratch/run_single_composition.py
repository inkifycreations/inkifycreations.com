import os
import sys
from collections import deque
from PIL import Image, ImageEnhance

pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
output_dir = os.path.join(pictures_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)

child_photo_path = os.path.join(pictures_dir, "birthday", "ChatGPT Image Jun 9, 2026, 11_41_55 AM.png")
child_photo = Image.open(child_photo_path)

def crop_and_fit(photo, target_width, target_height):
    pw, ph = photo.size
    photo_ratio = pw / ph
    target_ratio = target_width / target_height
    if photo_ratio > target_ratio:
        new_height = target_height
        new_width = int(pw * (target_height / ph))
        resized = photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        left = (new_width - target_width) // 2
        return resized.crop((left, 0, left + target_width, target_height))
    else:
        new_width = target_width
        new_height = int(ph * (target_width / pw))
        resized = photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        top = (new_height - target_height) // 2
        return resized.crop((0, top, target_width, top + target_height))

def find_grey_components(img_rgb):
    w, h = img_rgb.size
    is_grey = [[False for _ in range(w)] for _ in range(h)]
    grey_pixels = []
    for y in range(h):
        for x in range(w):
            r, g, b = img_rgb.getpixel((x, y))
            if abs(r - g) <= 3 and abs(g - b) <= 3 and 110 <= r <= 210:
                is_grey[y][x] = True
                grey_pixels.append((x, y))
    if not grey_pixels:
        return []
    visited = [[False for _ in range(w)] for _ in range(h)]
    components = []
    for x, y in grey_pixels:
        if visited[y][x]:
            continue
        comp = []
        queue = deque([(x, y)])
        visited[y][x] = True
        while queue:
            cx, cy = queue.popleft()
            comp.append((cx, cy))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < w and 0 <= ny < h:
                    if is_grey[ny][nx] and not visited[ny][nx]:
                        visited[ny][nx] = True
                        queue.append((nx, ny))
        if len(comp) > 200:
            xs = [p[0] for p in comp]
            ys = [p[1] for p in comp]
            components.append({
                'bbox': (min(xs), min(ys), max(xs), max(ys)),
                'pixels': comp
            })
    return components

template_path = os.path.join(pictures_dir, "Cat mug Design", "CAT WALLSEE.png")
print("Reading template:", template_path)
print("Template exists:", os.path.exists(template_path))

with Image.open(template_path) as template:
    template_rgb = template.convert('RGB')
    components = find_grey_components(template_rgb)
    print("Found components:", len(components))
    
    template_rgba = template.convert('RGBA')
    pixels = template_rgba.load()
    for comp in components:
        for x, y in comp['pixels']:
            pixels[x, y] = (0, 0, 0, 0)
            
    photo_layer = Image.new('RGBA', template.size, (0, 0, 0, 0))
    for idx, comp in enumerate(components):
        x1, y1, x2, y2 = comp['bbox']
        fw = x2 - x1 + 1
        fh = y2 - y1 + 1
        cropped = crop_and_fit(child_photo, fw, fh)
        photo_layer.paste(cropped, (x1, y1))
        
    final_img = Image.alpha_composite(photo_layer, template_rgba)
    final_img_rgb = final_img.convert('RGB')
    
    target_dir = os.path.join(output_dir, "Cat mug Design")
    os.makedirs(target_dir, exist_ok=True)
    out_path = os.path.join(target_dir, "CAT WALLSEE.png")
    final_img_rgb.save(out_path, 'PNG', dpi=(300, 300))
    print("Saved to:", out_path)
    print("Out path exists:", os.path.exists(out_path))
    print("Outputs structure:", os.listdir(output_dir))
    if os.path.exists(target_dir):
        print("Subfolder contents:", os.listdir(target_dir))
