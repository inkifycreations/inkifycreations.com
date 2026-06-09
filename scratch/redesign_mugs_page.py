import os
import sys
import shutil
import re
from collections import deque
from PIL import Image, ImageEnhance

# Reconfigure stdout to support unicode prints on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Paths
pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
child_photo_path = os.path.join(pictures_dir, "birthday", "ChatGPT Image Jun 9, 2026, 11_41_55 AM.png")
couple_photo_path = os.path.join(pictures_dir, "love and annversiary", "ChatGPT Image Jun 9, 2026, 11_11_18 AM.png")

assets_designs_dir = r"c:\Users\anaka\Downloads\third app\third app\assets\mug_designs"
app_js_path = r"c:\Users\anaka\Downloads\third app\third app\app.js"
index_html_path = r"c:\Users\anaka\Downloads\third app\third app\index.html"
index_css_path = r"c:\Users\anaka\Downloads\third app\third app\index.css"

os.makedirs(assets_designs_dir, exist_ok=True)

# 1. Enhance actual photos
print("Loading and enhancing actual photos...")
child_photo = Image.open(child_photo_path)
couple_photo = Image.open(couple_photo_path)

def enhance_photo(img):
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.10)
    return img

child_photo = enhance_photo(child_photo)
couple_photo = enhance_photo(couple_photo)

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

# Category mappings
category_map = {
    'birthday': ('birthday', 'Drinkware - Birthday'),
    'cat mug design': ('cats', 'Drinkware - Cats'),
    'dad gesign': ('family', 'Drinkware - Family'),
    'family design': ('family', 'Drinkware - Family'),
    'friends mugs design': ('friends', 'Drinkware - Friends'),
    'love and annversiary': ('love', 'Drinkware - Love & Anniversary'),
    'normal': ('general', 'Drinkware - General & Holiday')
}

templates_js_list = []
print("\nComposing template images...")

item_count = 0
for root, dirs, files in os.walk(pictures_dir):
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
        if name == os.path.basename(child_photo_path) or name == os.path.basename(couple_photo_path):
            continue
            
        full_path = os.path.join(root, name)
        try:
            with Image.open(full_path) as template:
                template_rgb = template.convert('RGB')
                components = find_grey_components(template_rgb)
                if not components:
                    continue
                
                # Sort components left to right
                components_sorted = sorted(components, key=lambda c: c['bbox'][0])
                
                # Create transparent window
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
                    elif is_birthday:
                        target_photo = child_photo
                    else:
                        if len(components_sorted) == 2:
                            target_photo = child_photo if idx == 0 else couple_photo
                        else:
                            target_photo = child_photo
                            
                    cropped_photo = crop_and_fit(target_photo, fw, fh)
                    photo_layer.paste(cropped_photo, (x1, y1))
                
                final_img = Image.alpha_composite(photo_layer, template_rgba)
                final_img_rgb = final_img.convert('RGB')
                
                # Save to static
                clean_filename = f"{cat_key}_{name.lower().replace(' ', '_').replace('&', 'and').replace('\'', '')}"
                dst_file = os.path.join(assets_designs_dir, clean_filename)
                final_img_rgb.save(dst_file, 'PNG', dpi=(300, 300))
                
                base_name = os.path.splitext(name)[0]
                display_name = " ".join([w.capitalize() for w in base_name.split()])
                if "mug" not in display_name.lower():
                    display_name = f"{display_name} Mug"
                unique_id = f"mug-{cat_key}-{item_count}"
                
                # Category labels / descriptions
                desc = f"Beautiful custom themed {cat_key} design mug featuring personalized high-fidelity wrap print."
                if cat_key == 'family':
                    desc = "Celebrate family love and parents with a custom-themed trophy badge or floral design frame."
                elif cat_key == 'love':
                    desc = "Show your affection with interconnected hearts, wedding bells, or custom anniversary theme wraps."
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
    wrapImage: "assets/mug_designs/{clean_filename}?v=2",
    overlayClass: "{cat_key}-overlay",
    overlayHtml: `
      <img src="assets/mug_designs/{clean_filename}?v=2" style="width: calc(100% + 8px); height: calc(100% + 8px); margin: -4px; object-fit: cover; border-radius: 1px;" alt="{display_name} Preview">
    `
  }}"""
                templates_js_list.append(template_js)
                item_count += 1
        except Exception as e:
            print(f"Error processing {name}: {e}")

print(f"Total composed templates: {len(templates_js_list)}")

# 2. Modify app.js templates catalog & renderMugsGrid method
print("\nUpdating app.js templates catalog and render method...")
with open(app_js_path, "r", encoding="utf-8") as f:
    app_js_content = f.read()

# Replace templates list
templates_block = "const MUG_TEMPLATES = [\n" + ",\n".join(templates_js_list) + "\n];"
start_idx = app_js_content.find("const MUG_TEMPLATES = [")
end_idx = app_js_content.find("// --- 1. SPA ROUTER ---")

if start_idx != -1 and end_idx != -1:
    app_js_content = app_js_content[:start_idx] + templates_block + "\n\n" + app_js_content[end_idx:]
else:
    print("Error: Could not locate MUG_TEMPLATES block in app.js!")

# Now replace renderMugsGrid method in app.js
render_start_marker = "renderMugsGrid() {"
# We will find the entire renderMugsGrid function block and replace it
# Let's search for renderMugsGrid() { up to the ending '}'
render_start_idx = app_js_content.find(render_start_marker)
if render_start_idx != -1:
    # Find closing brace of renderMugsGrid
    brace_count = 0
    render_end_idx = -1
    for idx in range(render_start_idx, len(app_js_content)):
        char = app_js_content[idx]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                render_end_idx = idx + 1
                break
                
    if render_end_idx != -1:
        new_render_method = r"""renderMugsGrid() {
    const grid = document.getElementById('mugs-templates-grid');
    if (!grid) return;

    grid.innerHTML = '';
    
    const filtered = MUG_TEMPLATES.filter(item => {
      const matchesCategory = this.activeMugFilter === 'all' || item.category === this.activeMugFilter;
      const matchesSearch = !this.mugSearchQuery || 
                            item.name.toLowerCase().includes(this.mugSearchQuery) || 
                            item.description.toLowerCase().includes(this.mugSearchQuery);
      return matchesCategory && matchesSearch;
    });

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--text-secondary);">
          <i class="fa-solid fa-folder-open" style="font-size: 2.5rem; color: rgba(255,255,255,0.1); margin-bottom: 15px; display: block;"></i>
          No templates found matching your search.
        </div>
      `;
      return;
    }

    filtered.forEach(item => {
      const cardHtml = `
        <div class="product-card glass-panel premium-mug-card" style="display: flex; flex-direction: column; justify-content: space-between;">
          <!-- Wide Wrap Design Banner -->
          <div class="mug-design-banner-container">
            <img src="${appRouter.getAssetUrl(item.wrapImage)}" alt="${item.name} Wrap Design" class="mug-design-banner">
            
            <!-- Category Badge -->
            <span class="mug-design-category-badge category-badge-${item.category}">
              ${item.category.toUpperCase()}
            </span>
            
            <!-- Floating Mockup overlay -->
            <div class="floating-mug-mockup-wrapper">
              <img src="${appRouter.getAssetUrl('assets/mug.png?v=2')}" class="floating-mug-base">
              <div class="floating-mug-overlay ${item.overlayClass}">
                ${item.overlayHtml.replace(/src="assets\//g, 'src="' + appRouter.getAssetUrl('assets/'))}
              </div>
            </div>
          </div>
          
          <div class="product-info" style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; padding: 18px;">
            <div>
              <span class="product-category" style="color: var(--accent-light); font-weight: 700; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 1px;">
                ${item.categoryLabel}
              </span>
              <h3 class="product-name" style="font-size: 1.15rem; margin-top: 6px; font-weight: 800; color: #ffffff; line-height: 1.3;">
                ${item.name}
              </h3>
              <p class="product-meta-desc" style="font-size: 0.8rem; line-height: 1.5; color: var(--text-secondary); margin-top: 8px; margin-bottom: 12px; height: 54px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">
                ${item.description}
              </p>
              
              <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
                <span style="font-size: 0.7rem; color: #e2e8f0; background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.04);">
                  <i class="fa-solid fa-expand" style="margin-right: 4px; color: #a855f7;"></i> 300 DPI Wrap
                </span>
                <span style="font-size: 0.7rem; color: #e2e8f0; background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.04);">
                  <i class="fa-solid fa-clock" style="margin-right: 4px; color: #10b981;"></i> 1-Day Dispatch
                </span>
              </div>
            </div>
            
            <div>
              <div class="product-price-row" style="margin-bottom: 14px; display: flex; align-items: baseline; gap: 8px;">
                <span class="price-current" style="font-size: 1.3rem; font-weight: 800; color: #ffffff;">₹${item.price}</span>
                <span class="price-original" style="font-size: 0.88rem; text-decoration: line-through; color: var(--text-secondary);">₹${item.originalPrice}</span>
                <span class="price-discount" style="font-size: 0.75rem; background: #dc2626; color: #ffffff; padding: 2px 6px; border-radius: 4px; font-weight: 700;">SAVE ${Math.round((item.originalPrice - item.price) / item.originalPrice * 100)}%</span>
              </div>
              
              <button class="btn-primary btn-card-order" onclick="productCatalog.openCustomizer(4, '${item.name.replace("'", "\\'")}')" style="width: 100%; justify-content: center; min-height: auto; padding: 11px 16px; border-radius: 30px; font-size: 0.85rem; font-weight: 700; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(168, 85, 247, 0.25);">
                Bespoke Customize & Order <i class="fa-solid fa-wand-magic-sparkles" style="margin-left: 6px;"></i>
              </button>
            </div>
          </div>
        </div>
      `;
      grid.insertAdjacentHTML('beforeend', cardHtml);
    });
  }"""
        app_js_content = app_js_content[:render_start_idx] + new_render_method + app_js_content[render_end_idx:]
        print("  app.js renderMugsGrid updated successfully!")
    else:
        print("  Error: Could not locate ending of renderMugsGrid function!")
else:
    print("  Error: Could not locate renderMugsGrid method in app.js!")

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(app_js_content)

# 3. Modify index.html
print("\nUpdating index.html category filter pills...")
with open(index_html_path, "r", encoding="utf-8") as f:
    index_html_content = f.read()

pills_target = """            <div class="template-filter-row" style="display: flex; gap: 10px; flex-wrap: wrap;">
              <button class="filter-pill active" onclick="productCatalog.filterMugs('all', event)">All Mugs</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('classic', event)">Classic Upload</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('birthday', event)">Birthdays</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('love', event)">Love & Anniversary</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('family', event)">Family & Parents</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('friends', event)">Friends</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('cats', event)">Cats</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('general', event)">General & Holiday</button>
            </div>"""

pills_replacement = """            <div class="template-filter-row" style="display: flex; gap: 10px; flex-wrap: wrap;">
              <button class="filter-pill active" onclick="productCatalog.filterMugs('all', event)">All Mugs</button>
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
    print("  index.html updated successfully (removed classic upload pill)!")
else:
    print("  Warning: Could not find template-filter-row in index.html!")

# 4. Append styles to index.css
print("\nAppending premium styles to index.css...")
premium_css = """
/* --- PREMIUM REDESIGNED MUGS CATALOG STYLES --- */
.premium-mug-card {
  background: rgba(15, 15, 20, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 16px !important;
  overflow: hidden !important;
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  position: relative;
}

.premium-mug-card:hover {
  transform: translateY(-8px) scale(1.02) !important;
  border-color: rgba(168, 85, 247, 0.4) !important;
  box-shadow: 0 12px 36px rgba(168, 85, 247, 0.15) !important;
}

.mug-design-banner-container {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: #09090d;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  justify-content: center;
  align-items: center;
}

.mug-design-banner {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.82;
  transition: all 0.5s ease;
}

.premium-mug-card:hover .mug-design-banner {
  opacity: 0.95;
  transform: scale(1.08);
}

.mug-design-category-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  font-size: 0.62rem;
  font-weight: 800;
  padding: 4px 8px;
  border-radius: 20px;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  z-index: 5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.category-badge-birthday { background: #db2777; color: #fff; }
.category-badge-cats { background: #eab308; color: #000; }
.category-badge-family { background: #0284c7; color: #fff; }
.category-badge-friends { background: #8b5cf6; color: #fff; }
.category-badge-love { background: #dc2626; color: #fff; }
.category-badge-general { background: #10b981; color: #fff; }

.floating-mug-mockup-wrapper {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 76px;
  height: 76px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(25, 25, 35, 0.95) 0%, rgba(10, 10, 15, 0.98) 100%);
  border: 1.5px solid rgba(255, 255, 255, 0.15);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
  z-index: 10;
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  overflow: hidden;
}

.premium-mug-card:hover .floating-mug-mockup-wrapper {
  transform: scale(1.18) rotate(4deg);
  border-color: rgba(168, 85, 247, 0.5);
  box-shadow: 0 10px 24px rgba(168, 85, 247, 0.3);
}

.floating-mug-base {
  height: 90%;
  width: auto;
  object-fit: contain;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,0.5));
}

.floating-mug-overlay {
  position: absolute;
  top: 24px;
  left: 51%;
  transform: translateX(-50%);
  width: 24px;
  height: 35px;
  border-radius: 1px;
  overflow: hidden;
  box-sizing: border-box;
  pointer-events: none;
}
"""

with open(index_css_path, "a", encoding="utf-8") as f:
    f.write(premium_css)
print("  index.css updated with premium redesigned classes!")

print("\nRedesign successfully finished!")
