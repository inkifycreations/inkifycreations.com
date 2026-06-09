with open("app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# 1. Route Handler in navigate()
old_route_anchor = """    if (viewId === 'cart') {
      cartManager.renderCart();

    } else if (viewId === 'orders') {"""

new_route_handler = """    if (viewId === 'cart') {
      cartManager.renderCart();
    } else if (viewId === 'mugs') {
      productCatalog.renderMugsGrid();
    } else if (viewId === 'orders') {"""

if old_route_anchor in js_content:
    js_content = js_content.replace(old_route_anchor, new_route_handler)
    print("Successfully restored route handler.")
else:
    # Try with LF newlines
    old_route_anchor_lf = old_route_anchor.replace('\r\n', '\n')
    new_route_handler_lf = new_route_handler.replace('\r\n', '\n')
    if old_route_anchor_lf in js_content:
        js_content = js_content.replace(old_route_anchor_lf, new_route_handler_lf)
        print("Successfully restored route handler (LF).")
    else:
        print("Error: Route handler anchor not found!")


# 2. openCustomizer redirect
old_customizer_anchor = """  openCustomizer(productId, templateName = null) {


    const product = CATALOG.find(p => p.id === productId);"""

new_customizer_code = """  openCustomizer(productId, templateName = null) {
    if (productId === 4 && !templateName) {
      appRouter.navigate('mugs');
      return;
    }

    const product = CATALOG.find(p => p.id === productId);"""

if old_customizer_anchor in js_content:
    js_content = js_content.replace(old_customizer_anchor, new_customizer_code)
    print("Successfully restored openCustomizer redirect.")
else:
    # Try with LF newlines
    old_customizer_anchor_lf = old_customizer_anchor.replace('\r\n', '\n')
    new_customizer_code_lf = new_customizer_code.replace('\r\n', '\n')
    if old_customizer_anchor_lf in js_content:
        js_content = js_content.replace(old_customizer_anchor_lf, new_customizer_code_lf)
        print("Successfully restored openCustomizer redirect (LF).")
    else:
        # Check if there is only 1 blank line or something
        # Let's use a regex to replace
        import re
        pattern = r"openCustomizer\(productId,\s*templateName\s*=\s*null\)\s*\{\s*const\s+product\s*=\s*CATALOG"
        # wait, let's keep it simple and check other variants
        print("Error: openCustomizer anchor not found!")


# 3. Restore catalog methods at the end of productCatalog
old_catalog_end = """  updateTextContent(val) {
    // Canvas preview removed
  },

  
};"""

# We define the methods block
new_methods = """  updateTextContent(val) {
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
                ${item.overlayHtml.replace(/src=\\\\"assets\\\\//g, 'src="' + appRouter.getAssetUrl('assets/'))}
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
  }
};"""

if old_catalog_end in js_content:
    js_content = js_content.replace(old_catalog_end, new_methods)
    print("Successfully restored catalog methods.")
else:
    # Try with LF newlines
    old_catalog_end_lf = old_catalog_end.replace('\r\n', '\n')
    new_methods_lf = new_methods.replace('\r\n', '\n')
    if old_catalog_end_lf in js_content:
        js_content = js_content.replace(old_catalog_end_lf, new_methods_lf)
        print("Successfully restored catalog methods (LF).")
    else:
        print("Error: Catalog methods boundary not found!")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(js_content)
