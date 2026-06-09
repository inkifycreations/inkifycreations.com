const fs = require('fs');

// Mock browser globals
global.window = {
  location: {
    pathname: '/mugs',
    search: '',
    hash: ''
  },
  addEventListener: (name, cb) => {
    console.log(`[window] addEventListener: ${name}`);
  },
  scrollTo: (opts) => {
    console.log(`[window] scrollTo:`, opts);
  },
  history: {
    pushState: (state, title, url) => {
      console.log(`[window.history] pushState:`, { state, title, url });
    }
  }
};

global.history = global.window.history;

const mockElement = {
  classList: {
    add: (cls) => console.log(`[classList] add: ${cls}`),
    remove: (cls) => console.log(`[classList] remove: ${cls}`)
  },
  addEventListener: (name, cb) => {
    console.log(`[element] addEventListener: ${name}`);
  },
  setAttribute: (name, val) => {
    console.log(`[element] setAttribute: ${name}=${val}`);
  },
  getAttribute: (name) => {
    console.log(`[element] getAttribute: ${name}`);
    return null;
  },
  removeAttribute: (name) => {
    console.log(`[element] removeAttribute: ${name}`);
  },
  style: {}
};

global.document = {
  querySelector: (selector) => {
    console.log(`[document] querySelector: ${selector}`);
    return mockElement;
  },
  querySelectorAll: (selector) => {
    console.log(`[document] querySelectorAll: ${selector}`);
    return [mockElement];
  },
  getElementById: (id) => {
    console.log(`[document] getElementById: ${id}`);
    if (id === 'mugs-templates-grid') {
      return {
        innerHTML: '',
        insertAdjacentHTML: (pos, html) => {
          console.log(`[DOM] grid.insertAdjacentHTML: pos=${pos}`);
        }
      };
    }
    return mockElement;
  },
  addEventListener: (name, cb) => {
    console.log(`[document] addEventListener: ${name}`);
  }
};

global.sessionStorage = {
  getItem: (name) => {
    console.log(`[sessionStorage] getItem: ${name}`);
    return null;
  },
  setItem: (name, val) => {
    console.log(`[sessionStorage] setItem: ${name}=${val}`);
  }
};

global.localStorage = {
  getItem: (name) => {
    console.log(`[localStorage] getItem: ${name}`);
    return null;
  },
  setItem: (name, val) => {
    console.log(`[localStorage] setItem: ${name}=${val}`);
  }
};

global.fetch = (url) => {
  console.log(`[fetch]: ${url}`);
  return Promise.resolve({
    ok: true,
    json: () => Promise.resolve([])
  });
};

global.setInterval = (cb, time) => {
  console.log(`[setInterval] registered`);
  return 123;
};

global.setTimeout = (cb, time) => {
  console.log(`[setTimeout] registered`);
  cb(); // Call it immediately for testing
  return 456;
};

// Load app.js
try {
  const appJsCode = fs.readFileSync('app.js', 'utf8');
  // Run app.js code
  eval(appJsCode + `
    console.log("--- Initializing App via DOMContentLoaded callback ---");
    appRouter.init();
    carousel.init();
    authManager.init();
    productCatalog.init();
    cartManager.init();
    ordersManager.init();
  `);
  console.log("Full initialization mock completed successfully.");
} catch (err) {
  console.error("Initialization error:", err);
}
