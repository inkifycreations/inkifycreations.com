import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

assets_designs_dir = r"c:\Users\anaka\Downloads\third app\third app\assets\mug_designs"
app_js_path = r"c:\Users\anaka\Downloads\third app\third app\app.js"
index_html_path = r"c:\Users\anaka\Downloads\third app\third app\index.html"
index_css_path = r"c:\Users\anaka\Downloads\third app\third app\index.css"

category_map = {
    'birthday': ('birthday', 'Drinkware - Birthday'),
    'cats': ('cats', 'Drinkware - Cats'),
    'family': ('family', 'Drinkware - Family'),
    'friends': ('friends', 'Drinkware - Friends'),
    'love': ('love', 'Drinkware - Love & Anniversary'),
    'general': ('general', 'Drinkware - General & Holiday')
}

# 1. Scan assets/mug_designs/ to get all cleaned filenames
print("Scanning assets/mug_designs/ for clean filenames...")
templates_js_list = []
item_count = 0

if not os.path.exists(assets_designs_dir):
    print(f"Error: designs directory {assets_designs_dir} does not exist!")
    sys.exit(1)

for filename in sorted(os.listdir(assets_designs_dir)):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    
    # Filename structure is: [category]_[name].png
    parts = filename.split('_', 1)
    if len(parts) != 2:
        continue
    cat_key = parts[0]
    rest = parts[1]
    
    if cat_key not in category_map:
        print(f"Skipping unknown category in file: {filename}")
        continue
        
    cat_label = category_map[cat_key][1]
    
    # Format a display name
    base_name = os.path.splitext(rest)[0]
    display_name = " ".join([w.capitalize() for w in base_name.split('_')])
    if "mug" not in display_name.lower():
        display_name = f"{display_name} Mug"
        
    unique_id = f"mug-{cat_key}-{item_count}"
    
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
        
    # We build the overlay HTML with the correct category overlay class
    template_js = f"""  {{
    id: "{unique_id}",
    name: "{display_name}",
    category: "{cat_key}",
    categoryLabel: "{cat_label}",
    description: "{desc}",
    originalPrice: 299,
    price: 219,
    wrapImage: "assets/mug_designs/{filename}?v=2",
    overlayClass: "{cat_key}-overlay",
    overlayHtml: `
      <img src="assets/mug_designs/{filename}?v=2" style="width: calc(100% + 8px); height: calc(100% + 8px); margin: -4px; object-fit: cover; border-radius: 1px;" alt="{display_name} Preview">
    `
  }}"""
    templates_js_list.append(template_js)
    item_count += 1

print(f"Total template catalog size: {len(templates_js_list)}")

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

# Replace renderMugsGrid method
render_start_marker = "renderMugsGrid() {"
render_start_idx = app_js_content.find(render_start_marker)
if render_start_idx != -1:
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
        new_render_method = """renderMugsGrid() {
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
                ${item.overlayHtml.replace(/src=\\"assets\\//g, 'src="' + appRouter.getAssetUrl('assets/'))}
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
              
              <button class="btn-primary btn-card-order" onclick="productCatalog.openCustomizer(4, '${item.name.replace("'", "\\\\'")}')" style="width: 100%; justify-content: center; min-height: auto; padding: 11px 16px; border-radius: 30px; font-size: 0.85rem; font-weight: 700; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(168, 85, 247, 0.25);">
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

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(app_js_content)

# 3. Modify index.html (ensure classic upload is removed, and all category pills are updated)
print("\nUpdating index.html category filter pills...")
with open(index_html_path, "r", encoding="utf-8") as f:
    index_html_content = f.read()

# We look for template-filter-row and replace the pills
filter_row_pattern = r"(<div class=\"template-filter-row\"[^>]*>)(.*?)(<\/div>)"
new_pills = """
              <button class="filter-pill active" onclick="productCatalog.filterMugs('all', event)">All Mugs</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('birthday', event)">Birthdays</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('love', event)">Love & Anniversary</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('family', event)">Family & Parents</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('friends', event)">Friends</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('cats', event)">Cats</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('general', event)">General & Holiday</button>
            """

match = re.search(filter_row_pattern, index_html_content, re.DOTALL)
if match:
    index_html_content = index_html_content[:match.start(2)] + new_pills + index_html_content[match.end(2):]
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(index_html_content)
    print("  index.html updated with filter pills!")
else:
    print("  Warning: Could not find template-filter-row in index.html!")

# 4. Append premium CSS to index.css if not already present
print("\nChecking and appending premium CSS in index.css...")
with open(index_css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

if "PREMIUM REDESIGNED MUGS CATALOG STYLES" not in css_content:
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
    print("  index.css updated with premium CSS classes!")
else:
    print("  Premium CSS is already present in index.css.")

print("\nRedesign successfully finished!")
