import os
import shutil
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Source and Target Directories
pictures_dir = r"C:\Users\anaka\OneDrive\Pictures\mugs design"
outputs_dir = os.path.join(pictures_dir, "outputs")
assets_designs_dir = r"c:\Users\anaka\Downloads\third app\third app\assets\mug_designs"
app_js_path = r"c:\Users\anaka\Downloads\third app\third app\app.js"
index_html_path = r"c:\Users\anaka\Downloads\third app\third app\index.html"

# Ensure target directory exists
os.makedirs(assets_designs_dir, exist_ok=True)

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

print("Processing outputs and copying designs:")
print("=" * 100)

item_count = 0
for folder in sorted(os.listdir(outputs_dir)):
    folder_path = os.path.join(outputs_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    
    # Check folder category
    folder_lower = folder.lower()
    if folder_lower not in category_map:
        print(f"Skipping folder (not mapped): {folder}")
        continue
        
    cat_key, cat_label = category_map[folder_lower]
    
    for filename in sorted(os.listdir(folder_path)):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        src_file = os.path.join(folder_path, filename)
        
        # Create a clean target filename: e.g. cats_cat_sleep.png
        clean_filename = f"{cat_key}_{filename.lower().replace(' ', '_').replace('&', 'and').replace('\'', '')}"
        dst_file = os.path.join(assets_designs_dir, clean_filename)
        
        # Copy to assets/mug_designs/
        shutil.copy2(src_file, dst_file)
        
        # Determine a human-readable name from filename
        # e.g. "cat sleep.png" -> "Cat Sleep Mug"
        base_name = os.path.splitext(filename)[0]
        # Capitalize words
        display_name = " ".join([w.capitalize() for w in base_name.split()])
        if "mug" not in display_name.lower():
            display_name = f"{display_name} Mug"
            
        unique_id = f"mug-{cat_key}-{item_count}"
        
        # Build description
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
        print(f"  [{folder}] Copied '{filename}' -> '{clean_filename}' | Added as ID: {unique_id}")

print("=" * 100)
print(f"Total templates added: {len(templates_js_list) - 1}")

# 2. Modify app.js
print("\nUpdating app.js templates catalog...")
with open(app_js_path, "r", encoding="utf-8") as f:
    app_js_content = f.read()

# Build the JS block
templates_block = "const MUG_TEMPLATES = [\n" + ",\n".join(templates_js_list) + "\n];"

# Find the replacement target in app.js
start_marker = "const MUG_TEMPLATES = ["
end_marker = "// --- 1. SPA ROUTER ---"

start_idx = app_js_content.find(start_marker)
end_idx = app_js_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # Replace the block
    new_app_js = app_js_content[:start_idx] + templates_block + "\n\n" + app_js_content[end_idx:]
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(new_app_js)
    print("  app.js updated successfully!")
else:
    print("  Error: Could not find MUG_TEMPLATES block in app.js!")

# 3. Modify index.html filter pills
print("\nUpdating index.html category filter pills...")
with open(index_html_path, "r", encoding="utf-8") as f:
    index_html_content = f.read()

# Target target HTML block
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

if pills_target in index_html_content:
    index_html_content = index_html_content.replace(pills_target, pills_replacement)
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(index_html_content)
    print("  index.html updated successfully!")
else:
    # Try with CRLF / LF variations
    pills_target_lf = pills_target.replace('\r\n', '\n')
    pills_replacement_lf = pills_replacement.replace('\r\n', '\n')
    if pills_target_lf in index_html_content:
        index_html_content = index_html_content.replace(pills_target_lf, pills_replacement_lf)
        with open(index_html_path, "w", encoding="utf-8") as f:
            f.write(index_html_content)
        print("  index.html updated successfully (LF match)!")
    else:
        print("  Warning: Could not find pills_target in index.html!")

print("\nProcessing finished successfully!")
