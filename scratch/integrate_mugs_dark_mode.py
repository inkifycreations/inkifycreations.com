import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

app_js_path = "app.js"
index_html_path = "index.html"
assets_designs_dir = "assets/mug_designs"

category_map = {
    'birthday': ('birthday', 'Drinkware - Birthday'),
    'cats': ('cats', 'Drinkware - Cats'),
    'family': ('family', 'Drinkware - Family'),
    'friends': ('friends', 'Drinkware - Friends'),
    'love': ('love', 'Drinkware - Love & Anniversary'),
    'general': ('general', 'Drinkware - General & Holiday')
}

# 1. Scan assets/mug_designs/ to get all composed designs
print("Scanning assets/mug_designs/ for templates...")
templates_js_list = []
item_count = 0

if not os.path.exists(assets_designs_dir):
    print(f"Error: designs directory {assets_designs_dir} does not exist!")
    sys.exit(1)

for filename in sorted(os.listdir(assets_designs_dir)):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    
    parts = filename.split('_', 1)
    if len(parts) != 2:
        continue
    cat_key = parts[0]
    rest = parts[1]
    
    if cat_key not in category_map:
        print(f"Skipping unknown category in file: {filename}")
        continue
        
    cat_label = category_map[cat_key][1]
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

# 2. Modify index.html
print("\nModifying index.html...")
with open(index_html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Add navigation menu link
nav_old = """      <nav class="nav-menu" id="nav-menu">
        <span class="nav-link active" data-view="home" onclick="appRouter.navigate('home')">Home</span>
        <span class="nav-link" data-view="products" onclick="appRouter.navigate('products')">Products</span>
        <span class="nav-link" data-view="about" onclick="appRouter.navigate('about')">About Us</span>
      </nav>"""

nav_new = """      <nav class="nav-menu" id="nav-menu">
        <span class="nav-link active" data-view="home" onclick="appRouter.navigate('home')">Home</span>
        <span class="nav-link" data-view="products" onclick="appRouter.navigate('products')">Products</span>
        <span class="nav-link" data-view="mugs" onclick="appRouter.navigate('mugs')">Photo Mugs</span>
        <span class="nav-link" data-view="about" onclick="appRouter.navigate('about')">About Us</span>
      </nav>"""

if nav_old in html_content:
    html_content = html_content.replace(nav_old, nav_new)
    print("  Header nav link added.")
else:
    nav_old_lf = nav_old.replace('\r\n', '\n')
    nav_new_lf = nav_new.replace('\r\n', '\n')
    if nav_old_lf in html_content:
        html_content = html_content.replace(nav_old_lf, nav_new_lf)
        print("  Header nav link added (LF).")
    else:
        print("  Warning: Nav menu pattern not found in index.html!")

# Update Slide 3 Carousel Button
slide3_old = """                  <button class="btn-primary" onclick="productCatalog.openCustomizer(4)">
                    Customize Mug <i class="fa-solid fa-mug-hot"></i>
                  </button>"""

slide3_new = """                  <button class="btn-primary" onclick="appRouter.navigate('mugs')">
                    Explore Mug Studio <i class="fa-solid fa-mug-saucer"></i>
                  </button>"""

if slide3_old in html_content:
    html_content = html_content.replace(slide3_old, slide3_new)
    print("  Slide 3 button updated to navigate to mugs page.")
else:
    slide3_old_lf = slide3_old.replace('\r\n', '\n')
    slide3_new_lf = slide3_new.replace('\r\n', '\n')
    if slide3_old_lf in html_content:
        html_content = html_content.replace(slide3_old_lf, slide3_new_lf)
        print("  Slide 3 button updated to navigate to mugs page (LF).")
    else:
        print("  Warning: Slide 3 button pattern not found in index.html!")

# Insert mugs-view section with black background
mugs_section_html = """    </section>
    
    <!-- 2.5 PHOTO MUGS VIEW -->
    <section id="mugs-view" class="view-section" style="background-color: #000000 !important; background: #000000 !important;">
      <div class="mugs-section" style="padding-top: 50px; padding-bottom: 50px;">
        <div class="container">
          <!-- Banner Section -->
          <div class="mug-studio-banner glass-panel" style="margin-bottom: 40px; padding: 40px; border-radius: 20px; background: linear-gradient(135deg, rgba(147, 51, 234, 0.12) 0%, rgba(30, 46, 115, 0.18) 100%); border: 1px solid rgba(255, 255, 255, 0.08); position: relative; overflow: hidden; display: flex; align-items: center; justify-content: space-between; gap: 24px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 280px; text-align: left;">
              <span class="section-subtitle" style="font-size: 0.85rem; font-weight: 700; color: var(--accent-light); text-transform: uppercase; letter-spacing: 2px;">Premium Print Studio</span>
              <h2 class="section-title" style="font-size: 2.25rem; font-weight: 800; margin-top: 10px; margin-bottom: 15px; color: #ffffff;">Personalized Coffee Mugs</h2>
              <p class="section-desc" style="max-width: 600px; font-size: 0.95rem; line-height: 1.6; color: var(--text-secondary); margin: 0 0 20px 0;">
                Create the perfect gift or custom desk accessory in 3 easy steps. Select a curated template design below, upload your favorite pictures, type quotes, and print your vibe on premium high-gloss ceramic mugs.
              </p>
            </div>
          </div>
          
          <!-- Filter & Search Controls -->
          <div style="display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap; margin-bottom: 30px; background: rgba(255,255,255,0.02); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);">
            <!-- Filter Pills -->
            <div class="template-filter-row" style="display: flex; gap: 10px; flex-wrap: wrap;">
              <button class="filter-pill active" onclick="productCatalog.filterMugs('all', event)">All Mugs</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('birthday', event)">Birthdays</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('love', event)">Love & Anniversary</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('family', event)">Family & Parents</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('friends', event)">Friends</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('cats', event)">Cats</button>
              <button class="filter-pill" onclick="productCatalog.filterMugs('general', event)">General & Holiday</button>
            </div>
            
            <!-- Search Bar -->
            <div style="position: relative; min-width: 260px;">
              <i class="fa-solid fa-magnifying-glass" style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-secondary); font-size: 0.85rem;"></i>
              <input type="text" id="mug-template-search" class="input-field" placeholder="Search templates..." oninput="productCatalog.searchMugs(this.value)" style="padding-left: 38px; border-radius: 30px; font-size: 0.85rem; height: 38px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);">
            </div>
          </div>
          
          <!-- Mug Grid -->
          <div class="product-grid" id="mugs-templates-grid">
            <!-- templates go here -->
          </div>
        </div>
      </div>
    </section>
    
    <!-- 3. ABOUT US VIEW -->"""

target_insert = """    </section>
    
    
    
    <!-- 3. ABOUT US VIEW -->"""

if target_insert in html_content:
    html_content = html_content.replace(target_insert, mugs_section_html)
    print("  Inserted mugs-view HTML section.")
else:
    # Try LF version
    target_insert_lf = target_insert.replace('\r\n', '\n')
    mugs_section_html_lf = mugs_section_html.replace('\r\n', '\n')
    if target_insert_lf in html_content:
        html_content = html_content.replace(target_insert_lf, mugs_section_html_lf)
        print("  Inserted mugs-view HTML section (LF).")
    else:
        # Check if multiple newlines caused it, try a regex
        pattern = r"<\/section>\s*<!-- 3\. ABOUT US VIEW -->"
        if re.search(pattern, html_content):
            html_content = re.sub(pattern, mugs_section_html_lf, html_content)
            print("  Inserted mugs-view HTML section (Regex match).")
        else:
            print("  Warning: Could not locate insertion point for mugs-view in index.html!")

with open(index_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)


# 3. Modify app.js
print("\nModifying app.js...")
with open(app_js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Restore MUG_TEMPLATES array before SPA ROUTER
templates_block = "const MUG_TEMPLATES = [\n" + ",\n".join(templates_js_list) + "\n];\n\n"
router_comment = "// --- 1. SPA ROUTER ---"

if router_comment in js_content:
    js_content = js_content.replace(router_comment, templates_block + router_comment)
    print("  Restored MUG_TEMPLATES array.")
else:
    print("  Warning: Router comment not found in app.js!")

# Restore 'mugs' in route segments
old_segments = "['home', 'products', 'about', 'cart', 'orders', 'success', 'tracking']"
new_segments = "['home', 'products', 'mugs', 'about', 'cart', 'orders', 'success', 'tracking']"

if old_segments in js_content:
    js_content = js_content.replace(old_segments, new_segments)
    print("  Restored 'mugs' route segment.")
else:
    print("  Warning: Old route segments list not found in app.js!")

# Restore mugs route handler in navigate()
old_handler_anchor = """    if (viewId === 'cart') {
      cartManager.renderCart();
    } else if (viewId === 'orders') {"""

new_handler = """    if (viewId === 'cart') {
      cartManager.renderCart();
    } else if (viewId === 'mugs') {
      productCatalog.renderMugsGrid();
    } else if (viewId === 'orders') {"""

if old_handler_anchor in js_content:
    js_content = js_content.replace(old_handler_anchor, new_handler)
    print("  Restored 'mugs' route handler.")
else:
    old_handler_anchor_lf = old_handler_anchor.replace('\r\n', '\n')
    new_handler_lf = new_handler.replace('\r\n', '\n')
    if old_handler_anchor_lf in js_content:
        js_content = js_content.replace(old_handler_anchor_lf, new_handler_lf)
        print("  Restored 'mugs' route handler (LF).")
    else:
        print("  Warning: Route handler anchor not found in app.js!")

# Restore this.renderMugsGrid() call in init()
old_init_grids = """    await this.fetchCatalog();
    this.renderGrids();"""

new_init_grids = """    await this.fetchCatalog();
    this.renderGrids();
    this.renderMugsGrid();"""

if old_init_grids in js_content:
    js_content = js_content.replace(old_init_grids, new_init_grids)
    print("  Restored this.renderMugsGrid() in init().")
else:
    old_init_grids_lf = old_init_grids.replace('\r\n', '\n')
    new_init_grids_lf = new_init_grids.replace('\r\n', '\n')
    if old_init_grids_lf in js_content:
        js_content = js_content.replace(old_init_grids_lf, new_init_grids_lf)
        print("  Restored this.renderMugsGrid() in init() (LF).")
    else:
        print("  Warning: Init grid pattern not found in app.js!")

# Restore openCustomizer redirect
old_customizer = """  openCustomizer(productId, templateName = null) {
    const product = CATALOG.find(p => p.id === productId);"""

new_customizer = """  openCustomizer(productId, templateName = null) {
    if (productId === 4 && !templateName) {
      appRouter.navigate('mugs');
      return;
    }

    const product = CATALOG.find(p => p.id === productId);"""

if old_customizer in js_content:
    js_content = js_content.replace(old_customizer, new_customizer)
    print("  Restored openCustomizer redirect.")
else:
    old_customizer_lf = old_customizer.replace('\r\n', '\n')
    new_customizer_lf = new_customizer.replace('\r\n', '\n')
    if old_customizer_lf in js_content:
        js_content = js_content.replace(old_customizer_lf, new_customizer_lf)
        print("  Restored openCustomizer redirect (LF).")
    else:
        print("  Warning: openCustomizer anchor not found in app.js!")

# Restore catalog methods at the end of productCatalog
old_catalog_end = """  updateTextContent(val) {
    // Canvas preview removed
  }
};"""

new_catalog_end = """  updateTextContent(val) {
    // Canvas preview removed
  },

  activeMugFilter: 'all',
  mugSearchQuery: '',

  filterMugs(category, event = null) {
    this.activeMugFilter = category;
    document.querySelectorAll('.filter-pill').forEach(pill => {
      pill.classList.remove('active');
    });
    const evt = event || (window.event ? window.event : null);
    if (evt && evt.currentTarget) {
      evt.currentTarget.classList.add('active');
    }
    this.renderMugsGrid();
  },

  searchMugs(query) {
    this.mugSearchQuery = query.toLowerCase().trim();
    this.renderMugsGrid();
  },

  renderMugsGrid() {
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
                <span class="price-current" style="font-size: 1.3rem; font-weight: 800; color: #ffffff;">₹\u20b9${item.price}</span>
                <span class="price-original" style="font-size: 0.88rem; text-decoration: line-through; color: var(--text-secondary);">₹\u20b9${item.originalPrice}</span>
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
  }
};"""

if old_catalog_end in js_content:
    js_content = js_content.replace(old_catalog_end, new_catalog_end)
    print("  Restored productCatalog properties, search, filter, and render methods.")
else:
    old_catalog_end_lf = old_catalog_end.replace('\r\n', '\n')
    new_catalog_end_lf = new_catalog_end.replace('\r\n', '\n')
    if old_catalog_end_lf in js_content:
        js_content = js_content.replace(old_catalog_end_lf, new_catalog_end_lf)
        print("  Restored productCatalog properties, search, filter, and render methods (LF).")
    else:
        print("  Warning: End of productCatalog object pattern not found in app.js!")

with open(app_js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("\nIntegration completed successfully!")
