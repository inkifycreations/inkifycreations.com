// Mock environment
global.window = {};
global.document = {
  getElementById: (id) => {
    console.log("getElementById called for id:", id);
    if (id === 'mugs-templates-grid') {
      return {
        innerHTML: '',
        insertAdjacentHTML: (position, html) => {
          console.log("insertAdjacentHTML called at position:", position);
        }
      };
    }
    return null;
  }
};

const appRouter = {
  getAssetUrl: (path) => {
    return "/static/" + path;
  }
};
global.appRouter = appRouter;

const getDeliveryDateString = (daysAhead) => "10/06/2026";
global.getDeliveryDateString = getDeliveryDateString;

const MUG_TEMPLATES = [
  {
    id: "mug-classic",
    name: "Classic Photo Mug",
    category: "classic",
    categoryLabel: "Drinkware - Classic",
    description: "Classic high-gloss ceramic mug. Fill it with a single, bold portrait or family photograph.",
    originalPrice: 299,
    price: 219,
    overlayClass: "classic-overlay",
    overlayHtml: `<div>Upload Photo</div>`
  }
];
global.MUG_TEMPLATES = MUG_TEMPLATES;

const productCatalog = {
  activeMugFilter: 'all',
  mugSearchQuery: '',
  renderMugsGrid() {
    const grid = document.getElementById('mugs-templates-grid');
    if (!grid) {
      console.log("Grid not found!");
      return;
    }

    grid.innerHTML = '';
    
    const filtered = MUG_TEMPLATES.filter(item => {
      const matchesCategory = this.activeMugFilter === 'all' || item.category === this.activeMugFilter;
      const matchesSearch = !this.mugSearchQuery || 
                            item.name.toLowerCase().includes(this.mugSearchQuery) || 
                            item.description.toLowerCase().includes(this.mugSearchQuery);
      return matchesCategory && matchesSearch;
    });

    console.log("Filtered count:", filtered.length);

    filtered.forEach(item => {
      const cardHtml = `
        <div class="product-card glass-panel mug-template-card" style="display: flex; flex-direction: column; justify-content: space-between;">
          <div class="product-image-container mug-card-image-container" style="position: relative; overflow: hidden; background: radial-gradient(circle, rgba(255,255,255,0.02) 0%, rgba(0,0,0,0) 70%); display: flex; justify-content: center; align-items: center; padding: 20px; height: 200px;">
            <img src="${appRouter.getAssetUrl('assets/mug.png')}" alt="${item.name}" class="product-image" style="height: 100%; width: auto; object-fit: contain; filter: drop-shadow(0 6px 16px rgba(0,0,0,0.45));">
            <div class="mug-card-overlay ${item.overlayClass}" style="position: absolute; top: 62px; left: 51%; transform: translateX(-50%); width: 56px; height: 82px; border-radius: 2px; border: 1.2px dashed rgba(255, 255, 255, 0.25); background: rgba(0, 0, 0, 0.4); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 4px; box-sizing: border-box; pointer-events: none;">
              ${item.overlayHtml}
            </div>
          </div>
          <div class="product-info" style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <span class="product-category">${item.categoryLabel}</span>
              <h3 class="product-name" style="font-size: 1.05rem; margin-top: 4px; font-weight: 700; color: #ffffff;">${item.name}</h3>
              <p class="product-meta-desc" style="font-size: 0.8rem; line-height: 1.4; color: var(--text-secondary); margin-top: 6px; margin-bottom: 12px; height: 50px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">${item.description}</p>
              
              <div class="product-delivery-date" style="font-size: 0.78rem; color: #10b981; font-weight: 600; margin-bottom: 12px; display: flex; align-items: center; gap: 6px;">
                <i class="fa-solid fa-truck-fast"></i> Delivery Date: ${getDeliveryDateString(5)}
              </div>
            </div>
            
            <div>
              <div class="product-price-row" style="margin-bottom: 12px;">
                <span class="price-current">₹${item.price}</span>
                <span class="price-original">₹${item.originalPrice}</span>
                <span class="price-discount">SAVE ${Math.round((item.originalPrice - item.price) / item.originalPrice * 100)}%</span>
              </div>
              
              <button class="btn-primary btn-card-order" onclick="productCatalog.openCustomizer(4, '${item.name}')" style="width: 100%; justify-content: center; min-height: auto; padding: 10px 14px;">
                Customize Now <i class="fa-solid fa-wand-magic-sparkles" style="margin-left: 6px;"></i>
              </button>
            </div>
          </div>
        </div>
      `;
      grid.insertAdjacentHTML('beforeend', cardHtml);
    });
  }
};

try {
  productCatalog.renderMugsGrid();
  console.log("Success! No exception thrown.");
} catch (e) {
  console.error("Exception thrown:", e);
}
