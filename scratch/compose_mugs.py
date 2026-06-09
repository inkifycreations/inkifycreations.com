import os
import sys
from collections import deque
from PIL import Image, ImageEnhance

# Reconfigure stdout to support unicode prints on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Source paths
pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
output_dir = os.path.join(pictures_dir, "outputs")

child_photo_path = os.path.join(pictures_dir, "birthday", "ChatGPT Image Jun 9, 2026, 11_41_55 AM.png")
couple_photo_path = os.path.join(pictures_dir, "love and annversiary", "ChatGPT Image Jun 9, 2026, 11_11_18 AM.png")

# Load and enhance source photos
print("Loading and enhancing actual photos...")
child_photo = Image.open(child_photo_path)
couple_photo = Image.open(couple_photo_path)

# Apply mild enhancements (contrast + sharpness)
def enhance_photo(img):
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.10)
    return img

child_photo = enhance_photo(child_photo)
couple_photo = enhance_photo(couple_photo)

print(f"Child Photo: {child_photo.size} | Couple Photo: {couple_photo.size}")

def crop_and_fit(photo, target_width, target_height):
    pw, ph = photo.size
    photo_ratio = pw / ph
    target_ratio = target_width / target_height
    
    if photo_ratio > target_ratio:
        # Photo is wider than target frame: scale to match target height, then crop width
        new_height = target_height
        new_width = int(pw * (target_height / ph))
        resized_photo = photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        left = (new_width - target_width) // 2
        cropped_photo = resized_photo.crop((left, 0, left + target_width, target_height))
    else:
        # Photo is taller than target frame: scale to match target width, then crop height
        new_width = target_width
        new_height = int(ph * (target_width / pw))
        resized_photo = photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        top = (new_height - target_height) // 2
        cropped_photo = resized_photo.crop((0, top, target_width, top + target_height))
        
    return cropped_photo

def find_grey_components(img_rgb):
    w, h = img_rgb.size
    # Identify neutral grey pixels (R ≈ G ≈ B between 110 and 210)
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
                        
        if len(comp) > 200:  # Threshold for photo frame component size
            xs = [p[0] for p in comp]
            ys = [p[1] for p in comp]
            components.append({
                'bbox': (min(xs), min(ys), max(xs), max(ys)),
                'pixels': comp
            })
            
    return components

# Create output root directory
os.makedirs(output_dir, exist_ok=True)

print("\nStarting template rendering...")
print("=" * 100)

for root, dirs, files in os.walk(pictures_dir):
    # Skip output directory itself to avoid reprocessing
    if "outputs" in root.lower() or "output" in root.lower():
        continue
        
    folder_name = os.path.relpath(root, pictures_dir)
    for name in sorted(files):
        if name.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Skip the actual photo inputs
            if name == os.path.basename(child_photo_path) or name == os.path.basename(couple_photo_path):
                continue
                
            full_path = os.path.join(root, name)
            try:
                with Image.open(full_path) as template:
                    template_rgb = template.convert('RGB')
                    components = find_grey_components(template_rgb)
                    
                    if not components:
                        # Skip files that have no grey placeholders (previews/mockups or pure text/graphic mugs)
                        continue
                        
                    print(f"Processing: '{folder_name}/{name}' ({template.size[0]}x{template.size[1]})")
                    print(f"  Found {len(components)} grey placeholders.")
                    
                    # Sort bboxes by x-coordinate (left to right)
                    components_sorted = sorted(components, key=lambda c: c['bbox'][0])
                    
                    # Create RGBA copy of the template to modify pixels
                    template_rgba = template.convert('RGBA')
                    pixels = template_rgba.load()
                    
                    # Make grey pixels transparent in the template layer
                    for comp in components_sorted:
                        for x, y in comp['pixels']:
                            r, g, b, a = pixels[x, y]
                            pixels[x, y] = (r, g, b, 0)
                            
                    # Create photo layer canvas (transparent background)
                    photo_layer = Image.new('RGBA', template.size, (0, 0, 0, 0))
                    
                    # Fill each placeholder with the appropriate photo
                    for idx, comp in enumerate(components_sorted):
                        x1, y1, x2, y2 = comp['bbox']
                        fw = x2 - x1 + 1
                        fh = y2 - y1 + 1
                        
                        # Determine photo mapping rules
                        is_love = any(kw in folder_name.lower() or kw in name.lower() 
                                      for kw in ['love', 'anniv', 'wedding', 'couple', 'lover'])
                        is_birthday = any(kw in folder_name.lower() or kw in name.lower() 
                                          for kw in ['birthday', 'child', 'baby'])
                        
                        if is_love:
                            # Love and Wedding mugs always use the couple photo
                            target_photo = couple_photo
                            photo_name = "Couple Photo"
                        elif is_birthday:
                            # Birthday mugs always use the child photo
                            target_photo = child_photo
                            photo_name = "Child Photo"
                        else:
                            # For Dad, Mom, Family, Friends, Normal, Cat:
                            if len(components_sorted) == 2:
                                # Left frame child, right frame couple
                                if idx == 0:
                                    target_photo = child_photo
                                    photo_name = "Child Photo (Left Frame)"
                                else:
                                    target_photo = couple_photo
                                    photo_name = "Couple Photo (Right Frame)"
                            else:
                                # Fallback to child photo
                                target_photo = child_photo
                                photo_name = "Child Photo"
                                
                        print(f"  Placeholder {idx+1} BBox: {x1, y1, x2, y2} ({fw}x{fh}) -> Placing {photo_name}")
                        
                        # Crop and fit the photo to the placeholder bounding box
                        cropped_photo = crop_and_fit(target_photo, fw, fh)
                        photo_layer.paste(cropped_photo, (x1, y1))
                        
                    # Composite photo_layer behind the modified template_rgba
                    final_img = Image.alpha_composite(photo_layer, template_rgba)
                    
                    # Convert to RGB if template was RGB (for saving without alpha if preferred, but PNG supports RGBA)
                    # Let's keep RGBA to preserve transparency or save as RGB to be clean
                    final_img_rgb = final_img.convert('RGB')
                    
                    # Save the result in the outputs directory
                    rel_dir = os.path.relpath(root, pictures_dir)
                    target_dir = os.path.join(output_dir, rel_dir)
                    os.makedirs(target_dir, exist_ok=True)
                    
                    output_path = os.path.join(target_dir, name)
                    # Save at 300 DPI
                    final_img_rgb.save(output_path, 'PNG', dpi=(300, 300))
                    print(f"  Saved to: '{os.path.relpath(output_path, pictures_dir)}' at 300 DPI\n")
                    
            except Exception as e:
                print(f"  Error processing {name}: {e}\n")

print("=" * 100)
print("Processing completed successfully!")
