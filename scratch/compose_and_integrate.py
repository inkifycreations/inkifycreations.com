import os
import sys
import shutil
from collections import deque
from PIL import Image, ImageEnhance

# Reconfigure stdout to support unicode prints on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Source paths
pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
child_photo_path = os.path.join(pictures_dir, "birthday", "ChatGPT Image Jun 9, 2026, 11_41_55 AM.png")
couple_photo_path = os.path.join(pictures_dir, "love and annversiary", "ChatGPT Image Jun 9, 2026, 11_11_18 AM.png")

# Web App target paths
assets_designs_dir = r"c:\Users\anaka\Downloads\third app\third app\assets\mug_designs"
app_js_path = r"c:\Users\anaka\Downloads\third app\third app\app.js"
index_html_path = r"c:\Users\anaka\Downloads\third app\third app\index.html"

# Ensure target static directory exists
os.makedirs(assets_designs_dir, exist_ok=True)

# Load and enhance source photos
print("Loading and enhancing source photos...")
child_photo = Image.open(child_photo_path)
couple_photo = Image.open(couple_photo_path)

def enhance_photo(img):
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.10)
    return img

child_photo = enhance_photo(child_photo)
couple_photo = enhance_photo(couple_photo)

print(f"Child Photo size: {child_photo.size} | Couple Photo size: {couple_photo.size}")

def crop_and_fit(photo, target_width, target_height):
    pw, ph = photo.size
    photo_ratio = pw / ph
    target_ratio = target_width / target_height
    
    if photo_ratio > target_ratio:
        new_height = target_height
        new_width = int(pw * (target_height / ph))
        resized_photo = photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        left = (new_width - target_width) // 2
        cropped_photo = resized_photo.crop((left, 0, left + target_width, target_height))
    else:
        new_width = target_width
        new_height = int(ph * (target_width / pw))
        resized_photo = photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        top = (new_height - target_height) // 2
        cropped_photo = resized_photo.crop((0, top, target_width, top + target_height))
        
    return cropped_photo

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

# Category mappings for templates catalog
category_map = {
    'birthday': ('birthday', 'Drinkware - Birthday'),
    'cat mug design': ('cats', 'Drinkware - Cats'),
    'dad gesign': ('family', 'Drinkware - Family'),
    'family design': ('family', 'Drinkware - Family'),
    'friends mugs design': ('friends', 'Drinkware - Friends'),
    'love and annversiary': ('love', 'Drinkware - Love & Anniversary'),
    'normal': ('general', 'Drinkware - General & Holiday')
}

# Classic Upload Template (always first)
templates_js_list = [
    """  {
    id: "mug-classic",
    name: "Classic Photo Mug",
    category: "classic",
    categoryLabel: "Drinkware - Classic",
    description: "Classic high-gloss ceramic mug. Fill it with a single, bold portrait or family photograph that makes you smile every morning.",
    originalPrice: 299,
    price: 219,
    overlayClass: "classic-overlay",
    overlayHtml: `
      <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7); display: flex; flex-direction: column; align-items: center; gap: 4px;">
        <i class="fa-solid fa-camera" style="font-size: 1.25rem; color: var(--accent-light);"></i>
        <span style="font-size: 0.5rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Upload Photo</span>
      </div>
    `
  }"""
]

print("\nStarting composition and direct assets export...")
print("=" * 100)

item_count = 0

for root, dirs, files in os.walk(pictures_dir):
    # Skip outputs folders
    if "outputs" in root.lower() or "output" in root.lower():
        continue
        
    folder_name = os.path.relpath(root, pictures_dir)
    folder_lower = os.path.basename(root).lower()
    
    if folder_lower not in category_map:
        continue
        
    cat_key, cat_label = category_map[folder_lower]
    
    for name in sorted(files):
        if not name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        # Skip actual photos
        if name == os.path.basename(child_photo_path) or name == os.path.basename(couple_photo_path):
            continue
            
        full_path = os.path.join(root, name)
        try:
            with Image.open(full_path) as template:
                template_rgb = template.convert('RGB')
                components = find_grey_components(template_rgb)
                
                if not components:
                    continue
                    
                print(f"Processing: '{folder_name}/{name}' ({template.size[0]}x{template.size[1]})")
                print(f"  Found {len(components)} grey placeholders.")
                
                # Sort components left to right
                components_sorted = sorted(components, key=lambda c: c['bbox'][0])
                
                # Create transparent window template layer
                template_rgba = template.convert('RGBA')
                pixels = template_rgba.load()
                
                for comp in components_sorted:
                    for x, y in comp['pixels']:
                        r, g, b, a = pixels[x, y]
                        pixels[x, y] = (r, g, b, 0)
                        
                # Create photo layer
                photo_layer = Image.new('RGBA', template.size, (0, 0, 0, 0))
                
                for idx, comp in enumerate(components_sorted):
                    x1, y1, x2, y2 = comp['bbox']
                    fw = x2 - x1 + 1
                    fh = y2 - y1 + 1
                    
                    is_love = any(kw in folder_lower or kw in name.lower() 
                                  for kw in ['love', 'anniv', 'wedding', 'couple', 'lover'])
                    is_birthday = any(kw in folder_lower or kw in name.lower() 
                                      for kw in ['birthday', 'child', 'baby'])
                    
                    if is_love:
                        target_photo = couple_photo
                        photo_name = "Couple Photo"
                    elif is_birthday:
                        target_photo = child_photo
                        photo_name = "Child Photo"
                    else:
                        if len(components_sorted) == 2:
                            if idx == 0:
                                target_photo = child_photo
                                photo_name = "Child Photo (Left Frame)"
                            else:
                                target_photo = couple_photo
                                photo_name = "Couple Photo (Right Frame)"
                        else:
                            target_photo = child_photo
                            photo_name = "Child Photo"
                            
                    print(f"    Placeholder {idx+1}: {fw}x{fh} -> Placing {photo_name}")
                    cropped_photo = crop_and_fit(target_photo, fw, fh)
                    photo_layer.paste(cropped_photo, (x1, y1))
                    
                # Composite photo_layer behind template
                final_img = Image.alpha_composite(photo_layer, template_rgba)
                final_img_rgb = final_img.convert('RGB')
                
                # Save directly to website assets folder
                clean_filename = f"{cat_key}_{name.lower().replace(' ', '_').replace('&', 'and').replace('\'', '')}"
                dst_file = os.path.join(assets_designs_dir, clean_filename)
                final_img_rgb.save(dst_file, 'PNG', dpi=(300, 300))
                print(f"    Saved directly to assets: '{clean_filename}'\n")
                
                # Display name formatting
                base_name = os.path.splitext(name)[0]
                display_name = " ".join([w.capitalize() for w in base_name.split()])
                if "mug" not in display_name.lower():
                    display_name = f"{display_name} Mug"
                    
                unique_id = f"mug-{cat_key}-{item_count}"
                
                # Description building
                desc = f"Beautiful custom themed {cat_key} design mug featuring personalized high-fidelity wrap print."
                if cat_key == 'family':
                    desc = "Celebrate family love and parents with a custom-themed trophy badge or floral design frame."
                elif cat_key == 'love':
                    desc = "Show your affection with interconnected hearts, wedding bells, or custom anniversary theme frames."
                elif cat_key == 'birthday':
                    desc = "Celebrate their birthday with festive confetti, colorful balloons, and a personalized photo wrap."
                elif cat_key == 'cats':
                    desc = "Perfect for pet lovers! Custom illustrated cat frames for your coffee and tea mornings."
                elif cat_key == 'friends':
                    desc = "A touching keepsake for best friends and corporate buddies. Commemorate your shared moments."
                
                template_js = f"""  {{
    id: "{unique_id}",
    name: "{display_name}",
    category: "{cat_key}",
    categoryLabel: "{cat_label}",
    description: "{desc}",
    originalPrice: 299,
    price: 219,
    overlayClass: "{cat_key}-overlay",
    overlayHtml: `
      <img src="assets/mug_designs/{clean_filename}?v=2" style="width: calc(100% + 8px); height: calc(100% + 8px); margin: -4px; object-fit: cover; border-radius: 1px;" alt="{display_name} Preview">
    `
  }}"""
                templates_js_list.append(template_js)
                item_count += 1
                
        except Exception as e:
            print(f"  Error processing template {name}: {e}\n")

print("=" * 100)
print(f"Total template designs generated and exported: {len(templates_js_list) - 1}")

# 5. Modify app.js template array
print("\nUpdating app.js templates catalog...")
with open(app_js_path, "r", encoding="utf-8") as f:
    app_js_content = f.read()

templates_block = "const MUG_TEMPLATES = [\n" + ",\n".join(templates_js_list) + "\n];"

start_marker = "const MUG_TEMPLATES = ["
end_marker = "// --- 1. SPA ROUTER ---"

start_idx = app_js_content.find(start_marker)
end_idx = app_js_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_app_js = app_js_content[:start_idx] + templates_block + "\n\n" + app_js_content[end_idx:]
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(new_app_js)
    print("  app.js updated successfully with all designs!")
else:
    print("  Error: Could not find MUG_TEMPLATES block in app.js!")

# 6. Modify index.html filter pills
print("\nUpdating index.html category filter pills...")
with open(index_html_path, "r", encoding="utf-8") as f:
    index_html_content = f.read()

# Target filters
pills_target = """            <div class="template-filter-row" style="display: flex; gap: 10px; flex-wrap: wrap;">
              <button class="filter-pill active" onclick="productCatalog.filterMugs('all', event)">All Mugs</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('classic', event)">Classic Upload</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('birthday', event)">Birthdays</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('love', event)">Love & Anniversary</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('family', event)">Family & Parents</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('quotes', event)">Quotes & Corporate</button>
            </div>"""

pills_replacement = """            <div class="template-filter-row" style="display: flex; gap: 10px; flex-wrap: wrap;">
              <button class="filter-pill active" onclick="productCatalog.filterMugs('all', event)">All Mugs</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('classic', event)">Classic Upload</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('birthday', event)">Birthdays</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('love', event)">Love & Anniversary</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('family', event)">Family & Parents</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('friends', event)">Friends</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('cats', event)">Cats</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('general', event)">General & Holiday</button>
            </div>"""

modified_html = False
if pills_target in index_html_content:
    index_html_content = index_html_content.replace(pills_target, pills_replacement)
    modified_html = True
else:
    pills_target_lf = pills_target.replace('\r\n', '\n')
    pills_replacement_lf = pills_replacement.replace('\r\n', '\n')
    if pills_target_lf in index_html_content:
        index_html_content = index_html_content.replace(pills_target_lf, pills_replacement_lf)
        modified_html = True

if modified_html:
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(index_html_content)
    print("  index.html updated successfully with new filter pills!")
else:
    print("  Warning: Could not find template-filter-row in index.html!")

print("\nAll tasks completed successfully!")
