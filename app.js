/**
 * INKIFY CREATIONS - CORE APPLICATION ENGINE
 * Pure Vanilla JavaScript Client-Side E-Commerce Architecture
 */

// --- GLOBAL ERROR LOGGING ---
window.onerror = function(message, source, lineno, colno, error) {
  try {
    const errorData = {
      message: message || '',
      source: source || '',
      lineno: lineno || 0,
      colno: colno || 0,
      stack: error ? error.stack : ''
    };
    const logUrl = '/api/log-error/';
    fetch(logUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(errorData)
    }).catch(err => {});
  } catch (e) {}
  return false;
};

// --- GLOBAL STATE ---

const STATE = {
  cart: [],
  currentUser: null,
  activeReferralCode: null,
  activeReferralUser: null,
  activePaymentMode: 'cod',
  useWalletCredit: false,
  walletUsedAmount: 0,
  orders: [],
  systemEmails: []
};

// When running the frontend as a separate static server (e.g. :8080),
// set the full backend URL so fetch() goes to the Django server.
const API_BASE_URL = window.API_BASE_URL || '/api';

// Get formatted delivery date string (D/M/YYYY)
function getDeliveryDateString(daysAhead = 5) {
  const date = new Date();
  date.setDate(date.getDate() + daysAhead);
  return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
}

// Premium custom modal dialog popup system
function showCustomDialog({ icon, title, message, actions }) {
  return new Promise((resolve) => {
    const overlay = document.getElementById('custom-dialog-overlay');
    const iconEl = document.getElementById('custom-dialog-icon');
    const titleEl = document.getElementById('custom-dialog-title');
    const messageEl = document.getElementById('custom-dialog-message');
    const actionsEl = document.getElementById('custom-dialog-actions');

    if (!overlay || !messageEl || !actionsEl) {
      resolve(null);
      return;
    }

    if (iconEl) {
      iconEl.innerHTML = icon || '<i class="fa-solid fa-circle-info"></i>';
    }
    if (titleEl) {
      titleEl.textContent = title || '';
      titleEl.style.display = title ? 'block' : 'none';
    }
    messageEl.innerHTML = message || '';
    actionsEl.innerHTML = '';

    actions.forEach(action => {
      const btn = document.createElement('button');
      btn.className = action.type === 'primary' ? 'btn-primary' : 'btn-outline';
      btn.style.padding = '10px 20px';
      btn.style.fontSize = '0.85rem';
      btn.style.minHeight = 'auto';
      btn.style.borderRadius = '8px';
      btn.innerHTML = action.label;
      btn.onclick = () => {
        overlay.classList.remove('active');
        resolve(action.value);
      };
      actionsEl.appendChild(btn);
    });

    overlay.classList.add('active');
  });
}

function customAlert(message, title = 'Notification') {
  return showCustomDialog({
    icon: '<i class="fa-solid fa-circle-info" style="color: var(--accent-light);"></i>',
    title: title,
    message: message,
    actions: [{ label: 'OK', value: 'ok', type: 'primary' }]
  });
}

// --- SVG MOCKUPS ---
const SVG_MOCKUPS = {
  tshirt: {
    front: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="shirt-shading" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#2a2a32" />
          <stop offset="50%" stop-color="#16161a" />
          <stop offset="100%" stop-color="#09090b" />
        </radialGradient>
      </defs>
      <path d="M 124,50 C 134,58 166,58 176,50 L 228,62 C 233,63 236,68 234,73 L 214,120 C 212,125 206,126 202,122 L 194,114 Q 192,185 194,256 C 194,264 188,270 180,270 L 120,270 C 112,270 106,264 106,256 Q 108,185 106,114 L 98,122 C 94,126 88,125 86,120 L 66,73 C 64,68 67,63 72,62 Z" fill="url(#shirt-shading)" stroke="#222" stroke-width="1.5" id="shirt-body-path" />
      <path d="M 124,50 C 134,42 166,42 176,50 C 168,48 132,48 124,50 Z" fill="#18181f" stroke="#333" stroke-width="0.5" />
      <path d="M 124,50 C 134,58 166,58 176,50 C 174,54 126,54 124,50 Z" fill="none" stroke="#222" stroke-width="1.5" opacity="0.6" />
      <path d="M 106,120 C 114,130 126,136 138,140" fill="none" stroke="#000" stroke-width="1.2" opacity="0.18" />
      <path d="M 194,120 C 186,130 174,136 162,140" fill="none" stroke="#000" stroke-width="1.2" opacity="0.18" />
      <line x1="124" y1="50" x2="72" y2="62" stroke="#000" stroke-width="1" opacity="0.25" />
      <line x1="176" y1="50" x2="228" y2="62" stroke="#000" stroke-width="1" opacity="0.25" />
      <path d="M 66,73 L 86,120" stroke="#000" stroke-width="1" opacity="0.15" />
      <path d="M 234,73 L 214,120" stroke="#000" stroke-width="1" opacity="0.15" />
      <path d="M 72,102 L 91,108" fill="none" stroke="#000" stroke-width="1" opacity="0.25" />
      <path d="M 228,102 L 209,108" fill="none" stroke="#000" stroke-width="1" opacity="0.25" />
      <path d="M 115,190 Q 150,200 185,190" fill="none" stroke="#000" stroke-width="1.2" opacity="0.1" />
      <path d="M 120,230 Q 150,238 180,230" fill="none" stroke="#000" stroke-width="1.2" opacity="0.08" />
    </svg>`,
    back: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="shirt-shading" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#2a2a32" />
          <stop offset="50%" stop-color="#16161a" />
          <stop offset="100%" stop-color="#09090b" />
        </radialGradient>
      </defs>
      <path d="M 124,50 C 134,45 166,45 176,50 L 228,62 C 233,63 236,68 234,73 L 214,120 C 212,125 206,126 202,122 L 194,114 Q 192,185 194,256 C 194,264 188,270 180,270 L 120,270 C 112,270 106,264 106,256 Q 108,185 106,114 L 98,122 C 94,126 88,125 86,120 L 66,73 C 64,68 67,63 72,62 Z" fill="url(#shirt-shading)" stroke="#222" stroke-width="1.5" id="shirt-body-path" />
      <path d="M 124,50 C 134,53 166,53 176,50" fill="none" stroke="#222" stroke-width="1.5" opacity="0.6" />
      <path d="M 106,120 C 114,130 126,136 138,140" fill="none" stroke="#000" stroke-width="1.2" opacity="0.15" />
      <path d="M 194,120 C 186,130 174,136 162,140" fill="none" stroke="#000" stroke-width="1.2" opacity="0.15" />
      <line x1="124" y1="50" x2="72" y2="62" stroke="#000" stroke-width="1" opacity="0.2" />
      <line x1="176" y1="50" x2="228" y2="62" stroke="#000" stroke-width="1" opacity="0.2" />
      <path d="M 150,60 L 150,240" fill="none" stroke="#000" stroke-width="1.5" opacity="0.06" stroke-dasharray="3,6" />
      <path d="M 115,190 Q 150,198 185,190" fill="none" stroke="#000" stroke-width="1.2" opacity="0.08" />
    </svg>`,
    left: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="shirt-shading" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#2a2a32" />
          <stop offset="50%" stop-color="#16161a" />
          <stop offset="100%" stop-color="#09090b" />
        </radialGradient>
      </defs>
      <path d="M 115,50 C 125,50 145,55 150,60 L 175,90 L 170,260 C 170,265 165,270 158,270 L 112,270 C 105,270 100,265 100,260 L 100,80 Z" fill="url(#shirt-shading)" stroke="#222" stroke-width="1.5" id="shirt-body-path" />
      <path d="M 120,55 L 155,62 C 160,63 163,68 161,73 L 141,135 C 139,140 133,141 129,137 L 115,123 Z" fill="url(#shirt-shading)" stroke="#1a1a20" stroke-width="1.2" />
      <path d="M 118,126 L 138,133" stroke="#000" stroke-width="1" opacity="0.3" />
      <path d="M 110,140 Q 125,160 115,185" fill="none" stroke="#000" stroke-width="1.2" opacity="0.15" />
    </svg>`,
    right: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="shirt-shading" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#2a2a32" />
          <stop offset="50%" stop-color="#16161a" />
          <stop offset="100%" stop-color="#09090b" />
        </radialGradient>
      </defs>
      <path d="M 185,50 C 175,50 155,55 150,60 L 125,90 L 130,260 C 130,265 135,270 142,270 L 188,270 C 195,270 200,265 200,260 L 200,80 Z" fill="url(#shirt-shading)" stroke="#222" stroke-width="1.5" id="shirt-body-path" />
      <path d="M 180,55 L 145,62 C 140,63 137,68 139,73 L 159,135 C 161,140 167,141 171,137 L 185,123 Z" fill="url(#shirt-shading)" stroke="#1a1a20" stroke-width="1.2" />
      <path d="M 182,126 L 162,133" stroke="#000" stroke-width="1" opacity="0.3" />
      <path d="M 190,140 Q 175,160 185,185" fill="none" stroke="#000" stroke-width="1.2" opacity="0.15" />
    </svg>`
  },
  polo: {
    front: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="polo-shading" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#3b1d5a" />
          <stop offset="60%" stop-color="#1c0933" />
          <stop offset="100%" stop-color="#0a0314" />
        </radialGradient>
      </defs>
      <path d="M 124,52 C 134,59 166,59 176,52 L 228,64 C 233,65 236,70 234,75 L 214,122 C 212,127 206,128 202,124 L 194,116 Q 192,185 194,256 C 194,264 188,270 180,270 L 120,270 C 112,270 106,264 106,256 Q 108,185 106,116 L 98,124 C 94,128 88,127 86,122 L 66,75 C 64,70 67,65 72,64 Z" fill="url(#polo-shading)" stroke="#3a1c5d" stroke-width="1.5" id="polo-body-path" />
      <path d="M 124,52 C 134,44 166,44 176,52 Z" fill="#2d1247" stroke="#1c0933" stroke-width="0.5" />
      <path d="M 124,52 L 150,90 L 140,55 Z" fill="#2d1247" stroke="#1c0933" stroke-width="1" />
      <path d="M 176,52 L 150,90 L 160,55 Z" fill="#3b185c" stroke="#1c0933" stroke-width="1" />
      <path d="M 144,90 L 156,90 L 156,130 L 144,130 Z" fill="#150626" stroke="#2b1145" stroke-width="1" />
      <circle cx="150" cy="100" r="3" fill="#ffffff" opacity="0.9" />
      <circle cx="150" cy="115" r="3" fill="#ffffff" opacity="0.9" />
      <path d="M 72,106 L 91,112" fill="none" stroke="#2b1145" stroke-width="2.5" opacity="0.8" />
      <path d="M 228,106 L 209,112" fill="none" stroke="#2b1145" stroke-width="2.5" opacity="0.8" />
      <path d="M 106,122 C 114,132 126,138 138,142" fill="none" stroke="#000" stroke-width="1.2" opacity="0.18" />
      <path d="M 194,122 C 186,132 174,138 162,142" fill="none" stroke="#000" stroke-width="1.2" opacity="0.18" />
    </svg>`,
    back: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="polo-shading" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#3b1d5a" />
          <stop offset="60%" stop-color="#1c0933" />
          <stop offset="100%" stop-color="#0a0314" />
        </radialGradient>
      </defs>
      <path d="M 124,52 C 134,52 166,52 176,52 L 228,64 C 233,65 236,70 234,75 L 214,122 C 212,127 206,128 202,124 L 194,116 Q 192,185 194,256 C 194,264 188,270 180,270 L 120,270 C 112,270 106,264 106,256 Q 108,185 106,116 L 98,124 C 94,128 88,127 86,122 L 66,75 C 64,70 67,65 72,64 Z" fill="url(#polo-shading)" stroke="#3a1c5d" stroke-width="1.5" id="polo-body-path" />
      <path d="M 120,52 C 130,62 170,62 180,52 Z" fill="#2d1247" stroke="#1c0933" stroke-width="1" />
      <path d="M 124,52 C 134,55 166,55 176,52" stroke="#1c0933" stroke-width="1.5" fill="none" />
      <path d="M 72,106 L 91,112" fill="none" stroke="#2b1145" stroke-width="2.5" opacity="0.8" />
      <path d="M 228,106 L 209,112" fill="none" stroke="#2b1145" stroke-width="2.5" opacity="0.8" />
    </svg>`,
    left: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="polo-shading" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#3b1d5a" />
          <stop offset="60%" stop-color="#1c0933" />
          <stop offset="100%" stop-color="#0a0314" />
        </radialGradient>
      </defs>
      <path d="M 115,52 C 125,52 145,57 150,62 L 175,92 L 170,260 C 170,265 165,270 158,270 L 112,270 C 105,270 100,265 100,260 L 100,82 Z" fill="url(#polo-shading)" stroke="#3a1c5d" stroke-width="1.5" id="polo-body-path" />
      <path d="M 115,52 Q 130,55 140,70 L 125,72 Z" fill="#2d1247" stroke="#1c0933" stroke-width="1" />
      <path d="M 120,57 L 155,64 C 160,65 163,70 161,75 L 141,137 C 139,142 133,143 129,139 L 115,125 Z" fill="url(#polo-shading)" stroke="#1a1a20" stroke-width="1.2" />
      <path d="M 118,128 L 138,135" fill="none" stroke="#2b1145" stroke-width="2.5" opacity="0.8" />
    </svg>`,
    right: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="polo-shading" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#3b1d5a" />
          <stop offset="60%" stop-color="#1c0933" />
          <stop offset="100%" stop-color="#0a0314" />
        </radialGradient>
      </defs>
      <path d="M 185,52 C 175,52 155,57 150,62 L 125,92 L 130,260 C 130,265 135,270 142,270 L 188,270 C 195,270 200,265 200,260 L 200,82 Z" fill="url(#polo-shading)" stroke="#3a1c5d" stroke-width="1.5" id="polo-body-path" />
      <path d="M 185,52 Q 170,55 160,70 L 175,72 Z" fill="#2d1247" stroke="#1c0933" stroke-width="1" />
      <path d="M 180,57 L 145,64 C 140,65 137,70 139,75 L 159,137 C 161,142 167,143 171,139 L 185,125 Z" fill="url(#polo-shading)" stroke="#1a1a20" stroke-width="1.2" />
      <path d="M 182,128 L 162,135" fill="none" stroke="#2b1145" stroke-width="2.5" opacity="0.8" />
    </svg>`
  },
  bottle: {
    front: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="bottle-shading" cx="50%" cy="30%" r="60%">
          <stop offset="0%" stop-color="#2a2a32" />
          <stop offset="50%" stop-color="#16161a" />
          <stop offset="100%" stop-color="#09090b" />
        </radialGradient>
        <linearGradient id="bottle-cap" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#475569" />
          <stop offset="50%" stop-color="#1e293b" />
          <stop offset="100%" stop-color="#0f172a" />
        </linearGradient>
      </defs>
      <rect x="135" y="35" width="30" height="20" rx="3" fill="url(#bottle-cap)" stroke="#334155" stroke-width="1"/>
      <rect x="130" y="55" width="40" height="10" rx="2" fill="url(#bottle-cap)" />
      <path d="M 132,65 L 168,65 L 168,90 Q 168,110 190,120 L 190,250 C 190,260 180,265 170,265 L 130,265 C 120,265 110,260 110,250 L 110,120 Q 132,110 132,90 Z" fill="url(#bottle-shading)" stroke="#222" stroke-width="1.5" id="bottle-body-path" />
      <path d="M 118,130 L 118,245 C 118,252 122,255 125,255" fill="none" stroke="#ffffff" stroke-width="2.5" opacity="0.12" stroke-linecap="round" />
    </svg>`,
    back: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="bottle-shading" cx="50%" cy="30%" r="60%">
          <stop offset="0%" stop-color="#2a2a32" />
          <stop offset="50%" stop-color="#16161a" />
          <stop offset="100%" stop-color="#09090b" />
        </radialGradient>
        <linearGradient id="bottle-cap" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#475569" />
          <stop offset="50%" stop-color="#1e293b" />
          <stop offset="100%" stop-color="#0f172a" />
        </linearGradient>
      </defs>
      <rect x="135" y="35" width="30" height="20" rx="3" fill="url(#bottle-cap)" stroke="#334155" stroke-width="1"/>
      <rect x="130" y="55" width="40" height="10" rx="2" fill="url(#bottle-cap)" />
      <path d="M 132,65 L 168,65 L 168,90 Q 168,110 190,120 L 190,250 C 190,260 180,265 170,265 L 130,265 C 120,265 110,260 110,250 L 110,120 Q 132,110 132,90 Z" fill="url(#bottle-shading)" stroke="#222" stroke-width="1.5" id="bottle-body-path" />
    </svg>`,
    left: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="bottle-shading" cx="50%" cy="30%" r="60%">
          <stop offset="0%" stop-color="#2a2a32" />
          <stop offset="50%" stop-color="#16161a" />
          <stop offset="100%" stop-color="#09090b" />
        </radialGradient>
        <linearGradient id="bottle-cap" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#475569" />
          <stop offset="50%" stop-color="#1e293b" />
          <stop offset="100%" stop-color="#0f172a" />
        </linearGradient>
      </defs>
      <rect x="135" y="35" width="30" height="20" rx="3" fill="url(#bottle-cap)" stroke="#334155" stroke-width="1"/>
      <rect x="130" y="55" width="40" height="10" rx="2" fill="url(#bottle-cap)" />
      <path d="M 132,65 L 168,65 L 168,90 Q 168,110 190,120 L 190,250 C 190,260 180,265 170,265 L 130,265 C 120,265 110,260 110,250 L 110,120 Q 132,110 132,90 Z" fill="url(#bottle-shading)" stroke="#222" stroke-width="1.5" id="bottle-body-path" />
    </svg>`,
    right: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="bottle-shading" cx="50%" cy="30%" r="60%">
          <stop offset="0%" stop-color="#2a2a32" />
          <stop offset="50%" stop-color="#16161a" />
          <stop offset="100%" stop-color="#09090b" />
        </radialGradient>
        <linearGradient id="bottle-cap" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#475569" />
          <stop offset="50%" stop-color="#1e293b" />
          <stop offset="100%" stop-color="#0f172a" />
        </linearGradient>
      </defs>
      <rect x="135" y="35" width="30" height="20" rx="3" fill="url(#bottle-cap)" stroke="#334155" stroke-width="1"/>
      <rect x="130" y="55" width="40" height="10" rx="2" fill="url(#bottle-cap)" />
      <path d="M 132,65 L 168,65 L 168,90 Q 168,110 190,120 L 190,250 C 190,260 180,265 170,265 L 130,265 C 120,265 110,260 110,250 L 110,120 Q 132,110 132,90 Z" fill="url(#bottle-shading)" stroke="#222" stroke-width="1.5" id="bottle-body-path" />
    </svg>`
  },
  cap: {
    front: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="cap-dome" cx="50%" cy="30%" r="55%">
          <stop offset="0%" stop-color="#2d2d35" />
          <stop offset="70%" stop-color="#141419" />
          <stop offset="100%" stop-color="#08080a" />
        </radialGradient>
        <linearGradient id="cap-visor" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#18181f" />
          <stop offset="50%" stop-color="#0f0f13" />
          <stop offset="100%" stop-color="#020204" />
        </linearGradient>
      </defs>
      <path d="M 60,170 C 60,80 110,65 150,65 C 190,65 240,80 240,170 C 240,178 238,185 235,185 L 65,185 C 62,185 60,178 60,170 Z" fill="url(#cap-dome)" stroke="#1a1a22" stroke-width="1.5" />
      <ellipse cx="150" cy="65" rx="8" ry="4" fill="#6b21a8" stroke="#a855f7" stroke-width="1" />
      <path d="M 55,180 C 70,180 90,218 150,218 C 210,218 230,180 245,180 C 255,182 258,190 245,198 C 220,218 190,230 150,230 C 110,230 80,218 55,198 C 42,190 45,182 55,180 Z" fill="url(#cap-visor)" stroke="#222" stroke-width="1" />
    </svg>`,
    back: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="cap-dome" cx="50%" cy="30%" r="55%">
          <stop offset="0%" stop-color="#2d2d35" />
          <stop offset="70%" stop-color="#141419" />
          <stop offset="100%" stop-color="#08080a" />
        </radialGradient>
      </defs>
      <path d="M 60,170 C 60,80 110,65 150,65 C 190,65 240,80 240,170 C 240,178 238,185 235,185 L 65,185 C 62,185 60,178 60,170 Z" fill="url(#cap-dome)" stroke="#1a1a22" stroke-width="1.5" />
      <path d="M 110,185 C 110,140 190,140 190,185 Z" fill="#131317" stroke="#1a1a22" stroke-width="1.5" />
      <rect x="115" y="176" width="70" height="8" rx="2" fill="#0f0f13" stroke="#222" stroke-width="1" />
      <circle cx="130" cy="180" r="1.5" fill="#fff" opacity="0.6" />
      <circle cx="140" cy="180" r="1.5" fill="#fff" opacity="0.6" />
      <circle cx="150" cy="180" r="1.5" fill="#fff" opacity="0.6" />
      <circle cx="160" cy="180" r="1.5" fill="#fff" opacity="0.6" />
      <circle cx="170" cy="180" r="1.5" fill="#fff" opacity="0.6" />
    </svg>`,
    left: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="cap-dome" cx="50%" cy="30%" r="55%">
          <stop offset="0%" stop-color="#2d2d35" />
          <stop offset="70%" stop-color="#141419" />
          <stop offset="100%" stop-color="#08080a" />
        </radialGradient>
        <linearGradient id="cap-visor-side" x1="100%" y1="0%" x2="0%" y2="50%">
          <stop offset="0%" stop-color="#18181f" />
          <stop offset="100%" stop-color="#020204" />
        </linearGradient>
      </defs>
      <path d="M 120,170 C 120,80 170,65 210,65 C 230,65 250,80 250,170 C 250,178 245,185 240,185 L 125,185 Z" fill="url(#cap-dome)" stroke="#1a1a22" stroke-width="1.5" />
      <path d="M 125,175 C 90,175 60,185 50,195 C 45,200 55,205 90,200 C 115,196 125,185 125,175 Z" fill="url(#cap-visor-side)" stroke="#222" stroke-width="1" />
    </svg>`,
    right: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="cap-dome" cx="50%" cy="30%" r="55%">
          <stop offset="0%" stop-color="#2d2d35" />
          <stop offset="70%" stop-color="#141419" />
          <stop offset="100%" stop-color="#08080a" />
        </radialGradient>
        <linearGradient id="cap-visor-side-r" x1="0%" y1="0%" x2="100%" y2="50%">
          <stop offset="0%" stop-color="#18181f" />
          <stop offset="100%" stop-color="#020204" />
        </linearGradient>
      </defs>
      <path d="M 180,170 C 180,80 130,65 90,65 C 70,65 50,80 50,170 C 50,178 55,185 60,185 L 175,185 Z" fill="url(#cap-dome)" stroke="#1a1a22" stroke-width="1.5" />
      <path d="M 175,175 C 210,175 240,185 250,195 C 255,200 245,205 210,200 C 185,196 175,185 175,175 Z" fill="url(#cap-visor-side-r)" stroke="#222" stroke-width="1" />
    </svg>`
  },
  mug: {
    front: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <linearGradient id="mug-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ffffff" />
          <stop offset="10%" stop-color="#f3f4f6" />
          <stop offset="75%" stop-color="#e5e7eb" />
          <stop offset="100%" stop-color="#d1d5db" />
        </linearGradient>
      </defs>
      <path d="M 205,95 C 255,95 255,205 205,205" fill="none" stroke="#e5e7eb" stroke-width="22" stroke-linecap="round" />
      <path d="M 205,95 C 255,95 255,205 205,205" fill="none" stroke="#d1d5db" stroke-width="12" stroke-linecap="round" />
      <path d="M 85,70 L 205,70 L 205,220 C 205,235 190,245 175,245 L 115,245 C 100,245 85,235 85,220 Z" fill="url(#mug-gradient)" stroke="#cccccc" stroke-width="1" />
      <path d="M 93,75 L 99,75 L 99,215 C 99,225 96,230 93,230 Z" fill="#ffffff" opacity="0.6" />
    </svg>`,
    back: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <linearGradient id="mug-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ffffff" />
          <stop offset="10%" stop-color="#f3f4f6" />
          <stop offset="75%" stop-color="#e5e7eb" />
          <stop offset="100%" stop-color="#d1d5db" />
        </linearGradient>
      </defs>
      <path d="M 95,95 C 45,95 45,205 95,205" fill="none" stroke="#e5e7eb" stroke-width="22" stroke-linecap="round" />
      <path d="M 95,95 C 45,95 45,205 95,205" fill="none" stroke="#d1d5db" stroke-width="12" stroke-linecap="round" />
      <path d="M 95,70 L 215,70 L 215,220 C 215,235 200,245 185,245 L 125,245 C 110,245 95,235 95,220 Z" fill="url(#mug-gradient)" stroke="#cccccc" stroke-width="1" />
      <path d="M 103,75 L 109,75 L 109,215 C 109,225 106,230 103,230 Z" fill="#ffffff" opacity="0.6" />
    </svg>`,
    left: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <linearGradient id="mug-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ffffff" />
          <stop offset="10%" stop-color="#f3f4f6" />
          <stop offset="75%" stop-color="#e5e7eb" />
          <stop offset="100%" stop-color="#d1d5db" />
        </linearGradient>
      </defs>
      <path d="M 90,70 L 210,70 L 210,220 C 210,235 195,245 180,245 L 120,245 C 105,245 90,235 90,220 Z" fill="url(#mug-gradient)" stroke="#cccccc" stroke-width="1" />
      <rect x="135" y="95" width="30" height="110" rx="15" fill="none" stroke="#e5e7eb" stroke-width="22" />
      <rect x="135" y="95" width="30" height="110" rx="15" fill="none" stroke="#d1d5db" stroke-width="12" />
    </svg>`,
    right: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <linearGradient id="mug-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ffffff" />
          <stop offset="10%" stop-color="#f3f4f6" />
          <stop offset="75%" stop-color="#e5e7eb" />
          <stop offset="100%" stop-color="#d1d5db" />
        </linearGradient>
      </defs>
      <path d="M 90,70 L 210,70 L 210,220 C 210,235 195,245 180,245 L 120,245 C 105,245 90,235 90,220 Z" fill="url(#mug-gradient)" stroke="#cccccc" stroke-width="1" />
      <path d="M 98,75 L 104,75 L 104,215 C 104,225 101,230 98,230 Z" fill="#ffffff" opacity="0.6" />
    </svg>`
  },
  giftbox: {
    front: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="box-shading" cx="50%" cy="45%" r="60%">
          <stop offset="0%" stop-color="#581c87" />
          <stop offset="60%" stop-color="#3b0764" />
          <stop offset="100%" stop-color="#1e0036" />
        </radialGradient>
      </defs>
      <path d="M 60,110 L 240,110 L 220,240 C 220,245 210,250 200,250 L 100,250 C 90,250 80,245 80,240 Z" fill="url(#box-shading)" stroke="#222" stroke-width="1.5" id="box-body-path" />
      <path d="M 50,85 L 250,85 L 250,115 L 50,115 Z" fill="url(#box-shading)" stroke="#222" stroke-width="1.5" id="box-lid-path" />
      <path d="M 50,85 L 250,85 L 235,115 L 65,115 Z" fill="#fff" opacity="0.05" />
      <rect x="140" y="85" width="20" height="165" fill="#facc15" />
      <path d="M 150,85 C 130,55 110,65 140,85 C 170,65 150,55 150,85 Z" fill="#facc15" stroke="#ca8a04" stroke-width="1" />
    </svg>`,
    back: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="box-shading" cx="50%" cy="45%" r="60%">
          <stop offset="0%" stop-color="#581c87" />
          <stop offset="60%" stop-color="#3b0764" />
          <stop offset="100%" stop-color="#1e0036" />
        </radialGradient>
      </defs>
      <path d="M 60,110 L 240,110 L 220,240 C 220,245 210,250 200,250 L 100,250 C 90,250 80,245 80,240 Z" fill="url(#box-shading)" stroke="#222" stroke-width="1.5" id="box-body-path" />
      <path d="M 50,85 L 250,85 L 250,115 L 50,115 Z" fill="url(#box-shading)" stroke="#222" stroke-width="1.5" id="box-lid-path" />
    </svg>`,
    left: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="box-shading" cx="50%" cy="45%" r="60%">
          <stop offset="0%" stop-color="#581c87" />
          <stop offset="60%" stop-color="#3b0764" />
          <stop offset="100%" stop-color="#1e0036" />
        </radialGradient>
      </defs>
      <path d="M 90,110 L 210,110 L 200,240 C 200,245 190,250 180,250 L 120,250 C 110,250 100,245 100,240 Z" fill="url(#box-shading)" stroke="#222" stroke-width="1.5" id="box-body-path" />
      <path d="M 80,85 L 220,85 L 220,115 L 80,115 Z" fill="url(#box-shading)" stroke="#222" stroke-width="1.5" id="box-lid-path" />
      <rect x="140" y="85" width="20" height="165" fill="#facc15" opacity="0.8" />
    </svg>`,
    right: `<svg viewBox="0 0 300 300" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#131317;">
      <defs>
        <radialGradient id="box-shading" cx="50%" cy="45%" r="60%">
          <stop offset="0%" stop-color="#581c87" />
          <stop offset="60%" stop-color="#3b0764" />
          <stop offset="100%" stop-color="#1e0036" />
        </radialGradient>
      </defs>
      <path d="M 90,110 L 210,110 L 200,240 C 200,245 190,250 180,250 L 120,250 C 110,250 100,245 100,240 Z" fill="url(#box-shading)" stroke="#222" stroke-width="1.5" id="box-body-path" />
      <path d="M 80,85 L 220,85 L 220,115 L 80,115 Z" fill="url(#box-shading)" stroke="#222" stroke-width="1.5" id="box-lid-path" />
      <rect x="140" y="85" width="20" height="165" fill="#facc15" opacity="0.8" />
    </svg>`
  }
};

// --- PRODUCT CATALOG DATA ---
let CATALOG = [
  {
    id: 1,
    name: "Premium T-Shirt",
    category: "Apparel",
    originalPrice: 500,
    price: 399,
    image: "assets/tshirt.png",
    description: "Ultra-soft 220 GSM combed cotton. Shown customized with bold neon 'Inkify Creations' typography."
  },
  {
    id: 2,
    name: "Executive Polo T-Shirt",
    category: "Apparel",
    originalPrice: 650,
    price: 499,
    image: "assets/polo tshirt.png",
    description: "Smooth premium pique polo with custom embroidery-style print and breathable performance fabric."
  },
  {
    id: 3,
    name: "Structured Cap",
    category: "Accessories",
    originalPrice: 350,
    price: 249,
    image: "assets/cap.png",
    description: "Premium structured cap with custom front panel printing and reinforced stitching."
  },
  {
    id: 4,
    name: "Photo Print Mug",
    category: "Drinkware",
    originalPrice: 299,
    price: 239,
    image: "assets/mugcat.png",
    description: "High-gloss ceramic mug with vivid personal photo printing for your favorite mornings."
  },
  {
    id: 5,
    name: "The Purple Gifting Set",
    category: "Signature Bundle",
    originalPrice: 1500,
    price: 999,
    cartPrice: 1199,
    image: "assets/gift_box.jpg",
    description: "Premium velvet-feel signature gift box containing T-Shirt, Polo, Mug, & Cap printed with your story."
  }
];




// --- 1. SPA ROUTER ---
const appRouter = {
  activeView: 'home',

  getAssetUrl(relativePath) {
    if (!relativePath) return "";
    if (relativePath.startsWith('<svg') || relativePath.startsWith('data:') || relativePath.includes('://') || relativePath.startsWith('http://') || relativePath.startsWith('https://')) {
      return relativePath;
    }
    if (relativePath.startsWith('/media/') || relativePath.startsWith('media/')) {
      return relativePath.startsWith('/') ? relativePath : '/' + relativePath;
    }
    const staticBase = window.BASE_STATIC_URL || '/static/';
    const cleanRelative = relativePath.startsWith('/') ? relativePath.substring(1) : relativePath;
    return `${staticBase}${cleanRelative}`;
  },

  init() {
    // Resolve all static images in index.html dynamically on load
    document.querySelectorAll('img').forEach(img => {
      const src = img.getAttribute('src');
      if (src && src.startsWith('assets/')) {
        img.src = this.getAssetUrl(src);
      }
    });

    // Monitor popstate for browser back/forward buttons
    window.addEventListener('popstate', (event) => {
      const state = event.state;
      if (state && state.viewId) {
        this.navigate(state.viewId, false);
      } else {
        const segments = window.location.pathname.split('/');
        const lastSegment = segments[segments.length - 1];
        if (['home', 'products', 'about', 'cart', 'orders', 'success', 'tracking', 'design-studio'].includes(lastSegment)) {
          this.navigate(lastSegment, false);
        } else {
          this.navigate('home', false);
        }
      }
    });

    // Check pathname route on load
    const segments = window.location.pathname.split('/');
    const lastSegment = segments[segments.length - 1];
    if (['home', 'products', 'about', 'cart', 'orders', 'success', 'tracking', 'design-studio'].includes(lastSegment)) {
      this.navigate(lastSegment, false);
    } else {
      // Navigate to home and push initial state
      this.navigate('home', true);
    }

    // Monitor scroll for header shrink effect
    window.addEventListener('scroll', () => {
      const header = document.getElementById('main-header');
      if (window.scrollY > 50) {
        header.classList.add('header-scrolled');
      } else {
        header.classList.remove('header-scrolled');
      }
    });
  },

  navigate(viewId, pushToHistory = true) {
    // Update Active View state
    this.activeView = viewId;

    // Prevent accessing design-studio directly without a product context
    if (viewId === 'design-studio' && !designStudio.activeProductId) {
      viewId = 'products';
      this.activeView = viewId;
    }

    if (pushToHistory) {
      // Find the base path (without the trailing view ID if present)
      let basePath = window.location.pathname;
      const segments = basePath.split('/').filter(s => s !== '');
      const lastSegment = segments[segments.length - 1];
      if (['home', 'products', 'about', 'cart', 'orders', 'success', 'tracking', 'design-studio'].includes(lastSegment)) {
        segments.pop();
      }
      basePath = '/' + segments.join('/');

      // Clean up base path and append viewId
      let newPath = basePath;
      if (!newPath.endsWith('/')) {
        newPath += '/';
      }
      newPath += (viewId === 'home' ? '' : viewId);
      
      // If path is just "/" let's keep it clean, otherwise ensure no trailing double slashes
      if (newPath.startsWith('//')) {
        newPath = newPath.substring(1);
      }

      history.pushState({ viewId }, "", newPath + window.location.search + window.location.hash);
    }

    // Deactivate all views, activate target
    document.querySelectorAll('.view-section').forEach(section => {
      section.classList.remove('active');
    });

    const targetSection = document.getElementById(`${viewId}-view`);
    if (targetSection) {
      targetSection.classList.add('active');
    }

    // Update Nav Highlights
    document.querySelectorAll('.nav-link').forEach(link => {
      if (link.getAttribute('data-view') === viewId) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });

    // Mobile navigation panel drawer collapse
    document.getElementById('nav-menu').classList.remove('active');
    document.getElementById('mobile-menu-toggle').classList.remove('active');

    // Scroll smoothly to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Update view-specific elements if needed
    if (viewId === 'cart') {
      cartManager.renderCart();
    } else if (viewId === 'orders') {
      ordersManager.renderOrders();
    } else if (viewId === 'home') {
      if (!sessionStorage.getItem('referral_promo_seen')) {
        setTimeout(() => {
          const promoModal = document.getElementById('referral-job-modal-overlay');
          if (promoModal) {
            promoModal.classList.add('active');
            sessionStorage.setItem('referral_promo_seen', 'true');
          }
        }, 1200);
      }
    }
  },

  toggleMobileMenu() {
    const navMenu = document.getElementById('nav-menu');
    const menuToggle = document.getElementById('mobile-menu-toggle');
    navMenu.classList.toggle('active');
    menuToggle.classList.toggle('active');
  },

  showGlobalImagePreview(src, title = '', category = '') {
    const overlay = document.getElementById('design-preview-overlay');
    const nameEl = document.getElementById('design-preview-name');
    const categoryEl = document.getElementById('design-preview-category');
    const imgEl = document.getElementById('design-preview-image');

    if (overlay && nameEl && categoryEl && imgEl) {
      nameEl.textContent = title;
      nameEl.style.display = title ? 'block' : 'none';
      categoryEl.textContent = category;
      categoryEl.style.display = category ? 'block' : 'none';
      imgEl.src = src;
      imgEl.alt = title || 'Image Preview';
      overlay.classList.add('active');
    }
  }
};

// --- 2. HERO CAROUSEL CONTROLLER ---
const carousel = {
  currentSlide: 0,
  totalSlides: 4,
  timerId: null,

  init() {
    this.startTimer();

    // Pause carousel auto-play on mouse hover
    const container = document.querySelector('.hero-carousel-container');
    if (container) {
      container.addEventListener('mouseenter', () => this.stopTimer());
      container.addEventListener('mouseleave', () => this.startTimer());
    }
  },

  startTimer() {
    this.timerId = setInterval(() => this.next(), 6000);
  },

  stopTimer() {
    if (this.timerId) clearInterval(this.timerId);
  },

  update() {
    const slides = document.querySelectorAll('.carousel-slide');
    const dots = document.querySelectorAll('.carousel-dot');

    slides.forEach((slide, i) => {
      if (i === this.currentSlide) {
        slide.classList.add('active');
      } else {
        slide.classList.remove('active');
      }
    });

    dots.forEach((dot, i) => {
      if (i === this.currentSlide) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });
  },

  next() {
    this.currentSlide = (this.currentSlide + 1) % this.totalSlides;
    this.update();
  },

  prev() {
    this.currentSlide = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
    this.update();
  },

  goTo(index) {
    this.currentSlide = index;
    this.update();
  }
};

// --- 3. AUTHENTICATION MANAGER (MOBILE REGISTRATION) ---
const authManager = {
  activeTab: 'login', // 'login' or 'register'

  init() {
    // If login UI is removed, do not attempt to wire auth elements.
    const savedUser = localStorage.getItem('inkify_user');
    if (savedUser) {
      STATE.currentUser = JSON.parse(savedUser);
      this.updateHeaderUI();
    }
  },

  openModal() {
    const overlay = document.getElementById('auth-modal-overlay');
    if (overlay) {
      overlay.classList.add('active');
      this.switchTab('login');
    }
  },

  closeModal() {
    const overlay = document.getElementById('auth-modal-overlay');
    if (overlay) overlay.classList.remove('active');
  },

  switchTab(tab) {
    this.activeTab = tab;

    const loginTabBtn = document.getElementById('auth-tab-login');
    const registerTabBtn = document.getElementById('auth-tab-register');
    const loginPanel = document.getElementById('auth-panel-login');
    const registerPanel = document.getElementById('auth-panel-register');

    if (!loginTabBtn || !registerTabBtn || !loginPanel || !registerPanel) return;

    if (tab === 'login') {
      loginTabBtn.classList.add('active');
      registerTabBtn.classList.remove('active');
      loginPanel.classList.add('active');
      registerPanel.classList.remove('active');
    } else {
      loginTabBtn.classList.remove('active');
      registerTabBtn.classList.add('active');
      loginPanel.classList.remove('active');
      registerPanel.classList.add('active');
    }
  },

  handleAuthClick() {
    if (!STATE.currentUser) {
      this.openModal();
      return;
    }

    const dropdown = document.getElementById('auth-dropdown-menu');
    if (dropdown) {
      dropdown.classList.toggle('active');
    }
  },

  async handleLoginSubmit(event) {
    event.preventDefault();
    const mobileInput = document.getElementById('login-mobile-number').value.trim();
    const passwordInput = document.getElementById('login-password').value;

    if (!mobileInput || !/^\d{10}$/.test(mobileInput)) {
      customAlert("Please provide a valid 10-digit mobile number containing only digits", "Validation Error");
      return;
    }

    if (!passwordInput) {
      customAlert("Please enter your password", "Validation Error");
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mobile: mobileInput, password: passwordInput })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Login failed");
      }

      // Save user details with token
      STATE.currentUser = {
        mobile: data.user.mobile,
        name: data.user.name,
        age: data.user.age,
        email: data.user.email,
        address: data.user.address,
        wallet_balance: data.user.wallet_balance || 0,
        referral_code: data.user.referral_code || null,
        is_staff: data.user.is_staff || false,
        token: data.token
      };

      localStorage.setItem('inkify_user', JSON.stringify(STATE.currentUser));
      this.updateHeaderUI();
      this.closeModal();

      // Reset form
      document.getElementById('auth-login-form').reset();

      await showCustomDialog({
        icon: '<i class="fa-solid fa-circle-user" style="color: var(--accent-light);"></i>',
        title: 'Authentication Success',
        message: `Welcome back, <strong>${STATE.currentUser.name}</strong>!`,
        actions: [{ label: 'Continue', value: 'ok', type: 'primary' }]
      });
    } catch (err) {
      customAlert(`Login error: ${err.message}`, "Authentication Error");
    }
  },

  async handleRegisterSubmit(event) {
    event.preventDefault();
    const nameInput = document.getElementById('register-name').value.trim();
    const ageInput = document.getElementById('register-age').value.trim();
    const mobileInput = document.getElementById('register-mobile').value.trim();
    const emailInput = document.getElementById('register-email').value.trim();
    const addressInput = document.getElementById('register-address').value.trim();
    const passwordInput = document.getElementById('register-password').value;
    const passwordRepeatInput = document.getElementById('register-password-repeat').value;

    if (!nameInput || !/^[a-zA-Z\s.\'-]+$/.test(nameInput)) {
      customAlert("Please provide your full name (letters, spaces, dots, and hyphens only)", "Validation Error");
      return;
    }

    if (!ageInput || !/^\d+$/.test(ageInput) || parseInt(ageInput) <= 0 || parseInt(ageInput) > 120) {
      customAlert("Please provide a valid age between 1 and 120", "Validation Error");
      return;
    }

    if (!mobileInput || !/^\d{10}$/.test(mobileInput)) {
      customAlert("Please provide a valid 10-digit mobile number containing only digits", "Validation Error");
      return;
    }

    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailInput || !emailRegex.test(emailInput)) {
      customAlert("Please provide a valid email address (e.g. name@domain.com)", "Validation Error");
      return;
    }

    if (!addressInput || addressInput.length < 10) {
      customAlert("Please provide a complete shipping address (minimum 10 characters)", "Validation Error");
      return;
    }

    if (!passwordInput || passwordInput.length < 12) {
      customAlert("Password must be at least 12 characters long", "Validation Error");
      return;
    }

    const hasUpper = /[A-Z]/.test(passwordInput);
    const hasLower = /[a-z]/.test(passwordInput);
    const hasNumber = /[0-9]/.test(passwordInput);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(passwordInput);

    if (!hasUpper || !hasLower || !hasNumber || !hasSpecial) {
      customAlert("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special symbol (!@#$%^&* etc.).", "Validation Error");
      return;
    }

    if (passwordInput !== passwordRepeatInput) {
      customAlert("Passwords do not match. Please verify your password confirmation.", "Validation Error");
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mobile: mobileInput,
          name: nameInput,
          age: parseInt(ageInput),
          email: emailInput,
          address: addressInput,
          password: passwordInput
        })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Registration failed");
      }

      // Save user details with token
      STATE.currentUser = {
        mobile: data.user.mobile,
        name: data.user.name,
        age: data.user.age,
        email: data.user.email,
        address: data.user.address,
        wallet_balance: data.user.wallet_balance || 0,
        referral_code: data.user.referral_code || null,
        is_staff: data.user.is_staff || false,
        token: data.token
      };

      localStorage.setItem('inkify_user', JSON.stringify(STATE.currentUser));
      this.updateHeaderUI();
      this.closeModal();

      // Reset form
      document.getElementById('auth-register-form').reset();

      await showCustomDialog({
        icon: '<i class="fa-solid fa-user-plus" style="color: var(--accent-light);"></i>',
        title: 'Registration Success',
        message: `Welcome, <strong>${STATE.currentUser.name}</strong>!<br>Your emotional design playground is now unlocked.`,
        actions: [{ label: 'Let\'s Go', value: 'ok', type: 'primary' }]
      });
    } catch (err) {
      customAlert(`Registration error: ${err.message}`, "Registration Error");
    }
  },

  async logout() {
    const confirmLogout = await showCustomDialog({
      icon: '<i class="fa-solid fa-right-from-bracket" style="color: var(--accent-light);"></i>',
      title: 'Confirm Logout',
      message: 'Are you sure you want to log out?',
      actions: [
        { label: 'Yes', value: 'yes', type: 'primary' },
        { label: 'No', value: 'no', type: 'outline' },
        { label: 'Cancel', value: 'cancel', type: 'outline' }
      ]
    });

    if (confirmLogout === 'yes') {
      STATE.currentUser = null;
      localStorage.removeItem('inkify_user');
      this.updateHeaderUI();
      appRouter.navigate('home');
    }
  },

  updateHeaderUI() {
    const btnText = document.getElementById('auth-btn-text');
    const headerBtn = document.getElementById('header-auth-btn');
    const menu = document.getElementById('auth-dropdown-menu');
    const walletText = document.getElementById('wallet-balance-text');
    const authSummary = document.getElementById('auth-dropdown-summary');
    const staffLink = document.getElementById('staff-dashboard-link');

    if (STATE.currentUser) {
      if (btnText) btnText.textContent = STATE.currentUser.name;
      if (headerBtn) headerBtn.title = "Logged in (Click for options)";
      if (walletText) {
        const balance = Number(STATE.currentUser.wallet_balance || 0).toFixed(2);
        walletText.textContent = `₹${balance}`;
      }
      if (authSummary) {
        const referralText = STATE.currentUser.referral_code ? STATE.currentUser.referral_code : 'Will generate after your first purchase';
        authSummary.innerHTML = `<strong>Wallet:</strong> ₹${Number(STATE.currentUser.wallet_balance || 0).toFixed(2)}<br><strong>Referral Code:</strong> ${referralText}`;
        authSummary.style.display = 'block';
      }
      // Show Admin Dashboard link only for staff users
      if (staffLink) {
        staffLink.style.display = STATE.currentUser.is_staff ? 'flex' : 'none';
      }
    } else {
      if (btnText) btnText.textContent = "Sign In";
      if (headerBtn) headerBtn.title = "Sign In with Mobile";
      if (menu) menu.classList.remove('active');
      if (walletText) {
        walletText.textContent = '₹0.00';
      }
      if (authSummary) {
        authSummary.style.display = 'none';
      }
      if (staffLink) staffLink.style.display = 'none';
    }
  }
};

// --- 4. PRODUCT CATALOG & CUSTOMIZER POPUP ---
const productCatalog = {
  selectedProductId: null,
  customizationType: 'photo', // 'photo' or 'text'
  selectedFileBase64: null,
  selectedColor: 'Light Blue', // Default color state
  selectedSize: null, // Selected size state
  photoX: 0,
  photoY: 0,
  photoScale: 1.0,
  textX: 0,
  textY: 0,

  async init() {
    await this.fetchCatalog();
    this.renderGrids();

    

    // Wire up apparel color selector swatches
    document.querySelectorAll('.color-swatch-option').forEach(swatch => {
      swatch.addEventListener('click', () => {
        document.querySelectorAll('.color-swatch-option').forEach(s => s.classList.remove('active'));
        swatch.classList.add('active');
        this.selectedColor = swatch.getAttribute('data-color');
      });
    });

    // Wire up size selector swatches
    document.querySelectorAll('.size-swatch-option').forEach(swatch => {
      swatch.addEventListener('click', () => {
        document.querySelectorAll('.size-swatch-option').forEach(s => s.classList.remove('active'));
        swatch.classList.add('active');
        this.selectedSize = swatch.getAttribute('data-size');
      });
    });
  },

  async fetchCatalog() {
    try {
      const response = await fetch(`${API_BASE_URL}/products/`);
      if (response.ok) {
        const data = await response.json();
        // Convert decimal prices back to float/int
        CATALOG = data.map(p => ({
          id: p.id,
          name: p.name,
          category: p.category,
          originalPrice: parseFloat(p.original_price),
          price: parseFloat(p.price),
          cartPrice: p.cart_price ? parseFloat(p.cart_price) : null,
          image: p.image,
          description: p.description,
          average_rating: parseFloat(p.average_rating || 0),
          reviews_count: parseInt(p.reviews_count || 0)
        }));
      }
    } catch (err) {
      console.warn("Failed to load catalog from server, using local fallback.", err);
    }
  },

  renderGrids() {
    const featuredGrid = document.getElementById('featured-products-grid');
    const fullGrid = document.getElementById('full-products-grid');

    featuredGrid.innerHTML = '';
    fullGrid.innerHTML = '';

    CATALOG.forEach(product => {
      // 1. Core Card elements
      const isSet = product.id === 5;
      const ratingHtml = product.reviews_count > 0 ? `
        <span style="font-size: 0.8rem; color: #fbbf24; display: flex; align-items: center; gap: 4px; font-weight: 600;">
          <i class="fa-solid fa-star"></i> ${Number(product.average_rating).toFixed(1)} (${product.reviews_count})
        </span>
      ` : `
        <span style="font-size: 0.75rem; color: var(--text-muted); display: flex; align-items: center; gap: 4px;">
          <i class="fa-regular fa-star"></i> No reviews
        </span>
      `;

      const cardHtml = `
        <div class="product-card glass-panel ${isSet ? 'whole-set-card' : ''}">
          ${isSet ? `<div class="whole-set-image">${product.image.startsWith('<svg') ? product.image : `<img src="${appRouter.getAssetUrl(product.image)}" alt="${product.name}">`}</div>` : ''}
          
          ${isSet ? '<div class="whole-set-content">' : ''}
            ${!isSet ? `
              <div class="product-image-container">
                ${product.image.startsWith('<svg') ? product.image : `<img src="${appRouter.getAssetUrl(product.image)}" alt="${product.name}" class="product-image">`}
              </div>
            ` : ''}
            
            <div class="product-info">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span class="product-category">${product.category}</span>
                ${ratingHtml}
              </div>
              <h3 class="product-name">${product.name}</h3>
              <p class="product-meta-desc">${product.description}</p>
              
              <div class="product-delivery-date" style="font-size: 0.82rem; color: #10b981; font-weight: 600; margin: 8px 0; display: flex; align-items: center; gap: 6px;">
                <i class="fa-solid fa-truck-fast"></i> Delivery Date: ${getDeliveryDateString(5)}
              </div>
              
              <div class="product-price-row">
                <span class="price-current">₹${product.price}</span>
                <span class="price-original">₹${product.originalPrice}</span>
                <span class="price-discount">SAVE ${Math.round((product.originalPrice - product.price) / product.originalPrice * 100)}%</span>
              </div>
              
              <button class="btn-primary btn-card-order" onclick="productCatalog.openCustomizer(${product.id})">
                Customize & Order <i class="fa-solid fa-wand-magic-sparkles"></i>
              </button>
            </div>
          ${isSet ? '</div>' : ''}
        </div>
      `;

      // Home page featured displays everything
      featuredGrid.insertAdjacentHTML('beforeend', cardHtml);

      // Full catalog page displays standard grid cards
      if (!isSet) {
        const standardCardHtml = `
          <div class="product-card glass-panel">
            <div class="product-image-container">
              ${product.image.startsWith('<svg') ? product.image : `<img src="${appRouter.getAssetUrl(product.image)}" alt="${product.name}" class="product-image">`}
            </div>
            <div class="product-info">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span class="product-category">${product.category}</span>
                ${ratingHtml}
              </div>
              <h3 class="product-name">${product.name}</h3>
              <p class="product-meta-desc">${product.description}</p>
              <div class="product-delivery-date" style="font-size: 0.82rem; color: #10b981; font-weight: 600; margin: 8px 0; display: flex; align-items: center; gap: 6px;">
                <i class="fa-solid fa-truck-fast"></i> Delivery Date: ${getDeliveryDateString(5)}
              </div>
              <div class="product-price-row">
                <span class="price-current">₹${product.price}</span>
                <span class="price-original">₹${product.originalPrice}</span>
                <span class="price-discount">SAVE ${Math.round((product.originalPrice - product.price) / product.originalPrice * 100)}%</span>
              </div>
              <button class="btn-primary btn-card-order" onclick="productCatalog.openCustomizer(${product.id})">
                Customize & Order <i class="fa-solid fa-wand-magic-sparkles"></i>
              </button>
            </div>
          </div>
        `;
        fullGrid.insertAdjacentHTML('beforeend', standardCardHtml);
      } else {
        // Render Set separately at the bottom of full list in standard layout
        fullGrid.insertAdjacentHTML('beforeend', cardHtml);
      }
    });
  },

  openCustomizer(productId, templateName = null) {
    // Always open Design Studio first for design selection
    if (!templateName) {
      designStudio.open(productId);
      return;
    }

    const product = CATALOG.find(p => p.id === productId);
    if (!product) return;

    this.selectedProductId = productId;
    this.selectedFileBase64 = null;
    this.selectedTemplateName = templateName;

    // Set titles
    const titleText = templateName ? `Customize ${templateName}` : `Customize ${product.name}`;
    document.getElementById('customizer-product-title').innerHTML = titleText;

    const subText = document.getElementById('customizer-product-sub');
    const textInput = document.getElementById('customizer-text-input');

    textInput.value = '';

    if (productId === 1) {
      subText.innerHTML = "Print your brand manifesto or logo. Default placeholder: <strong>'Inkify Creations'</strong>.";
      textInput.placeholder = "e.g. Inkify Creations";
    } else if (productId === 2) {
      subText.innerHTML = "Embroider or print your signature. Default placeholder: <strong>'Your Name'</strong>.";
      textInput.placeholder = "e.g. Mukesh / Your Name";
    } else if (productId === 3) {
      subText.innerHTML = "Print your ultimate inspiration or name. Default placeholder: <strong>'Your Hero'</strong>.";
      textInput.placeholder = "e.g. Your Hero / Iron Vibe";
    } else if (productId === 4) {
      subText.innerHTML = "Upload Ghibli family photos or custom art. Default text: <strong>'Ghibli Family Vibe'</strong>.";
      textInput.placeholder = "e.g. Ghibli Family Vibe";
    } else {
      subText.innerHTML = "Customize all items in the velvet gift box with a unified personal storytelling theme.";
      textInput.placeholder = "e.g. Yours Story / My Vibe";
    }

    // Set default color state & highlights
    const isApparel = productId === 1 || productId === 2 || productId === 5;
    if (isApparel) {
      this.selectedColor = 'Light Blue';
    } else {
      this.selectedColor = null;
    }

    document.querySelectorAll('.color-swatch-option').forEach(el => {
      if (this.selectedColor && el.getAttribute('data-color') === this.selectedColor) {
        el.classList.add('active');
      } else {
        el.classList.remove('active');
      }
    });

    // Reset size state & highlights
    this.selectedSize = null;
    document.querySelectorAll('.size-swatch-option').forEach(el => {
      el.classList.remove('active');
    });

    // Toggle color/size containers visibility
    const colorContainer = document.getElementById('customizer-color-container');
    const sizeContainer = document.getElementById('customizer-size-container');
    if (colorContainer) colorContainer.style.display = isApparel ? 'block' : 'none';
    if (sizeContainer) sizeContainer.style.display = isApparel ? 'block' : 'none';

    // Reset state variables
    this.photoScale = 1.0;
    this.photoX = 0;
    this.photoY = 0;
    this.textX = 0;
    this.textY = 0;

    this.clearSelectedFile(null);
    this.switchTab('photo');

    // Set product details
    const descText = document.getElementById('customizer-product-desc');
    if (descText) descText.innerText = product.description;

    const priceText = document.getElementById('customizer-product-price');
    if (priceText) priceText.innerText = `₹${product.price}`;

    // Open Popup overlay
    document.getElementById('customizer-modal-overlay').classList.add('active');
  },

  closeCustomizer() {
    document.getElementById('customizer-modal-overlay').classList.remove('active');
  },

  switchTab(tabName) {
    this.customizationType = tabName; // 'photo', 'text', or 'both'

    // Update active class on tab buttons
    document.querySelectorAll('.custom-tab-btn').forEach(btn => {
      btn.classList.remove('active');
    });
    const targetBtn = document.getElementById(`tab-btn-${tabName}`);
    if (targetBtn) {
      targetBtn.classList.add('active');
    }

    // Toggle inputs visibility
    const uploadGroup = document.getElementById('form-group-upload');
    const textGroup = document.getElementById('form-group-text');

    if (uploadGroup) {
      uploadGroup.style.display = (tabName === 'photo' || tabName === 'both') ? 'block' : 'none';
    }
    if (textGroup) {
      textGroup.style.display = (tabName === 'text' || tabName === 'both') ? 'block' : 'none';
    }
  },



  handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      customAlert("Please upload a valid image file");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        const MAX_WIDTH = 1000;
        const MAX_HEIGHT = 1000;
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
          }
        } else {
          if (height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
          }
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);

        const compressedBase64 = canvas.toDataURL('image/jpeg', 0.75);
        this.selectedFileBase64 = compressedBase64;

        // Show photo preview info row
        const previewInfo = document.getElementById('customizer-photo-preview-info');
        const photoName = document.getElementById('customizer-photo-name');
        if (previewInfo) previewInfo.style.display = 'flex';
        if (photoName) photoName.textContent = file.name;
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  },

  clearSelectedFile(event) {
    if (event) event.stopPropagation();
    this.selectedFileBase64 = null;
    const fileInput = document.getElementById('customizer-file-input');
    if (fileInput) fileInput.value = '';
    
    // Hide photo preview info row
    const previewInfo = document.getElementById('customizer-photo-preview-info');
    if (previewInfo) previewInfo.style.display = 'none';
  },

  applyCustomization() {
    const originalProduct = CATALOG.find(p => p.id === this.selectedProductId);
    if (!originalProduct) return;
    const product = { ...originalProduct };

    const isApparel = this.selectedProductId === 1 || this.selectedProductId === 2 || this.selectedProductId === 5;

    // Enforce size selection and color for apparel
    if (isApparel) {
      if (!this.selectedColor) {
        customAlert("Please select a fabric color to proceed!");
        return;
      }
      if (!this.selectedSize) {
        customAlert("Please select a size (S, M, L, XL, XXL, XXXL) to proceed!");
        return;
      }
    }

    const textInput = document.getElementById('customizer-text-input');
    const textVal = textInput ? textInput.value.trim() : '';

    // Validate inputs based on customizationType
    if (this.customizationType === 'photo') {
      if (!this.selectedFileBase64) {
        customAlert("Please upload a photograph to proceed!");
        return;
      }
    } else if (this.customizationType === 'text') {
      if (!textVal) {
        customAlert("Please enter the custom text to proceed!");
        return;
      }
    } else if (this.customizationType === 'both') {
      if (!this.selectedFileBase64) {
        customAlert("Please upload a photograph to proceed!");
        return;
      }
      if (!textVal) {
        customAlert("Please enter the custom text to proceed!");
        return;
      }
    }

    const colorSuffix = isApparel ? ` [Color: ${this.selectedColor}, Size: ${this.selectedSize}]` : '';

    let customization = null;
    const templatePrefix = this.selectedTemplateName ? `${this.selectedTemplateName} ` : '';

    if (this.customizationType === 'both') {
      // Map both to 'photo' customization type for database compatibility.
      // Store the base64 photograph in 'data' and append the custom text to the summary.
      customization = {
        type: 'photo',
        data: this.selectedFileBase64,
        font: 'sans-serif',
        color: isApparel ? this.selectedColor : null,
        size: isApparel ? this.selectedSize : null,
        summary: `Customized Blueprint (${templatePrefix}Photo & Text: "${textVal}")${colorSuffix}`
      };
    } else if (this.customizationType === 'photo') {
      customization = {
        type: 'photo',
        data: this.selectedFileBase64,
        font: 'sans-serif',
        color: isApparel ? this.selectedColor : null,
        size: isApparel ? this.selectedSize : null,
        summary: `Customized Blueprint (${templatePrefix}Photograph)${colorSuffix}`
      };
    } else { // 'text'
      customization = {
        type: 'text',
        data: textVal,
        font: 'sans-serif',
        color: isApparel ? this.selectedColor : null,
        size: isApparel ? this.selectedSize : null,
        summary: `Customized Blueprint (${templatePrefix}Text: "${textVal}")${colorSuffix}`
      };
    }

    // Attach design metadata if selectedDesign is set
    if (designStudio.selectedDesign) {
      customization.designId = designStudio.selectedDesign.id;
      customization.designName = designStudio.selectedDesign.name;
      customization.designImageUrl = designStudio.selectedDesign.image_url;
      product.image = designStudio.selectedDesign.image_url;
      product.name = `${product.name} — ${designStudio.selectedDesign.name}`;
    }

    // Add item to Cart
    cartManager.addToCart(product, customization);
    if (designStudio.selectedDesign) {
      designStudio.selectedDesign = null;
    }
    this.closeCustomizer();
  },

  shareDesign() {
    const shareUrl = `${window.location.origin}/?product=${this.selectedProductId}`;
    navigator.clipboard.writeText(shareUrl).then(() => {
      alert("Custom design blueprint link copied to clipboard!");
    }).catch(err => {
      console.error("Failed to copy link: ", err);
      alert(`Link: ${shareUrl}`);
    });
  },

  updateTextContent(val) {
    // Canvas preview removed
  },

  getProductById(productId) {
    if (!productId) return null;
    return CATALOG.find(p => Number(p.id) === Number(productId)) || null;
  },
};



// --- 4.5 DESIGN STUDIO ---
const designStudio = {
  activeProductId: null,
  activeProductType: null,
  activeProductName: null,
  allDesigns: [],
  _designMap: {},
  activeCategory: 'all',
  selectedDesign: null,
  customPhotoBase64: null,
  customPhotoBothBase64: null,
  activeTab: 'photo',
  modalPhotoBase64: null,
  modalPhotoBothBase64: null,
  modalActiveTab: 'photo',

  FONT_MAP: {
    Classic: "'Playfair Display', Georgia, serif",
    Modern: "'Outfit', 'Inter', sans-serif",
    Script: "'Dancing Script', 'Alex Brush', cursive",
    Bold: "'Impact', 'Arial Black', sans-serif",
    Minimal: "'Courier New', Courier, monospace"
  },

  COLOR_MAP: {
    White: "#ffffff",
    Black: "#111111",
    Purple: "#a855f7",
    Gold: "#fbbf24",
    Red: "#ef4444",
    Blue: "#3b82f6"
  },

  MOCKUP_PLACEMENT: {
    tshirt: {
      photo: { top: '90px', left: '105px', width: '70px', height: '70px', borderRadius: '4px' },
      text: { top: '105px', left: '95px', width: '90px', fontSize: '0.8rem' }
    },
    polo: {
      photo: { top: '92px', left: '108px', width: '65px', height: '65px', borderRadius: '4px' },
      text: { top: '106px', left: '98px', width: '85px', fontSize: '0.75rem' }
    },
    cap: {
      photo: { top: '110px', left: '120px', width: '40px', height: '35px', borderRadius: '2px' },
      text: { top: '125px', left: '105px', width: '70px', fontSize: '0.65rem' }
    },
    bottle: {
      photo: { top: '125px', left: '120px', width: '45px', height: '75px', borderRadius: '2px' },
      text: { top: '145px', left: '112px', width: '60px', fontSize: '0.7rem' }
    },
    mug: {
      photo: { top: '90px', left: '105px', width: '65px', height: '90px', borderRadius: '4px' },
      text: { top: '115px', left: '98px', width: '80px', fontSize: '0.75rem' }
    },
    gift_set: {
      photo: { top: '125px', left: '108px', width: '65px', height: '65px', borderRadius: '6px' },
      text: { top: '142px', left: '98px', width: '85px', fontSize: '0.8rem' }
    }
  },

  updateMockupPreview() {
    const canvas = document.getElementById('ds-mockup-svg-canvas');
    const photoLayer = document.getElementById('ds-mockup-photo-layer');
    const textLayer = document.getElementById('ds-mockup-text-layer');
    if (!canvas || !photoLayer || !textLayer) return;

    // Render base SVG if not already matches
    const type = this.activeProductType || 'mug';
    const baseSvg = SVG_MOCKUPS[type]?.front || SVG_MOCKUPS['mug']?.front;
    if (canvas.getAttribute('data-loaded-type') !== type) {
      canvas.innerHTML = baseSvg;
      canvas.setAttribute('data-loaded-type', type);
    }

    // Get placement settings
    const placement = this.MOCKUP_PLACEMENT[type] || this.MOCKUP_PLACEMENT['mug'];

    // Get inputs based on active tab
    const tab = this.activeTab;
    let photoSrc = null;
    let textVal = '';
    let fontVal = 'Modern';
    let colorVal = 'White';

    if (this.selectedDesign) {
      photoSrc = this.selectedDesign.image_url;
    }

    if (tab === 'photo') {
      if (!photoSrc) {
        photoSrc = this.customPhotoBase64;
      }
      photoLayer.style.display = photoSrc ? 'block' : 'none';
      textLayer.style.display = 'none';
    } else if (tab === 'text') {
      photoLayer.style.display = 'none';
      textLayer.style.display = 'block';
      textVal = (document.getElementById('ds-custom-text')?.value || '').trim();
      fontVal = document.getElementById('ds-custom-font')?.value || 'Modern';
      colorVal = document.getElementById('ds-custom-color')?.value || 'White';
    } else { // both
      if (!photoSrc) {
        photoSrc = this.customPhotoBothBase64;
      }
      photoLayer.style.display = photoSrc ? 'block' : 'none';
      textLayer.style.display = 'block';
      textVal = (document.getElementById('ds-custom-text-both')?.value || '').trim();
      fontVal = document.getElementById('ds-custom-font-both')?.value || 'Modern';
      colorVal = document.getElementById('ds-custom-color-both')?.value || 'White';
    }

    // Apply Photo Layer Styling
    if (photoSrc) {
      photoLayer.src = photoSrc;
      photoLayer.style.top = placement.photo.top;
      photoLayer.style.left = placement.photo.left;
      photoLayer.style.width = placement.photo.width;
      photoLayer.style.height = placement.photo.height;
      photoLayer.style.borderRadius = placement.photo.borderRadius;
    }

    // Apply Text Layer Styling
    if (textVal) {
      textLayer.textContent = textVal;
      textLayer.style.top = placement.text.top;
      textLayer.style.left = placement.text.left;
      textLayer.style.width = placement.text.width;
      textLayer.style.fontSize = placement.text.fontSize;
      textLayer.style.fontFamily = this.FONT_MAP[fontVal] || fontVal;
      textLayer.style.color = this.COLOR_MAP[colorVal] || colorVal;
      textLayer.style.textShadow = colorVal === 'White' ? '0 2px 4px rgba(0,0,0,0.8)' : '0 2px 4px rgba(255,255,255,0.8)';
    } else {
      textLayer.style.display = 'none';
    }
  },

  PRODUCT_TYPE_MAP: {
    1: 'tshirt',
    2: 'polo',
    3: 'bottle',
    4: 'mug',
    5: 'gift_set',
  },

  PRODUCT_LABEL_MAP: {
    1: 'T-Shirt Designs',
    2: 'Polo T-Shirt Designs',
    3: 'Bottle Designs',
    4: 'Mug Designs',
    5: 'The Purple Gifting Set',
  },

  async open(productId) {
    this.activeProductId = productId;
    this.activeProductType = this.PRODUCT_TYPE_MAP[productId] || 'mug';
    this.activeProductName = this.PRODUCT_LABEL_MAP[productId] || 'Designs';
    this.selectedDesign = null;
    this.customPhotoBase64 = null;
    this.customPhotoBothBase64 = null;
    this.activeCategory = 'all';
    this.activeTab = 'photo';
    const summary = document.getElementById('ds-selected-design-summary');
    if (summary) summary.style.display = 'none';

    // Clear Custom Design Studio page inputs
    const fileIn = document.getElementById('ds-file-input');
    const fileInBoth = document.getElementById('ds-file-input-both');
    if (fileIn) fileIn.value = '';
    if (fileInBoth) fileInBoth.value = '';
    const preview = document.getElementById('ds-photo-preview');
    const previewBoth = document.getElementById('ds-photo-preview-both');
    if (preview) preview.style.display = 'none';
    if (previewBoth) previewBoth.style.display = 'none';
    const txt = document.getElementById('ds-custom-text');
    const txtBoth = document.getElementById('ds-custom-text-both');
    if (txt) txt.value = '';
    if (txtBoth) txtBoth.value = '';
    const font = document.getElementById('ds-custom-font');
    const fontBoth = document.getElementById('ds-custom-font-both');
    if (font) font.value = 'Modern';
    if (fontBoth) fontBoth.value = 'Modern';
    const color = document.getElementById('ds-custom-color');
    const colorBoth = document.getElementById('ds-custom-color-both');
    if (color) color.value = 'White';
    if (colorBoth) colorBoth.value = 'White';
    const status = document.getElementById('ds-custom-status');
    if (status) status.textContent = '';

    // Update page header
    const label = document.getElementById('ds-product-type-label');
    const title = document.getElementById('ds-page-title');
    if (label) label.textContent = this.PRODUCT_TYPE_MAP[productId]?.toUpperCase() + ' STUDIO';
    if (title) title.textContent = this.activeProductName;

    // Hide selected bar
    this.hideSelectedBar();

    // Show loading
    const grid = document.getElementById('ds-designs-grid');
    if (grid) grid.innerHTML = `<div class="ds-loading"><i class="fa-solid fa-spinner fa-spin" style="font-size:2rem;color:var(--accent-purple);"></i><p style="margin-top:12px;color:var(--text-secondary);">Loading designs…</p></div>`;

    // Clear filter bar
    const filterBar = document.getElementById('ds-filter-bar');
    if (filterBar) filterBar.innerHTML = '';

    // Reset custom tab
    this.switchTab('photo');

    // Wire up inputs for live preview
    const inputs = [
      'ds-custom-text', 'ds-custom-font', 'ds-custom-color',
      'ds-custom-text-both', 'ds-custom-font-both', 'ds-custom-color-both'
    ];
    inputs.forEach(id => {
      const el = document.getElementById(id);
      if (el && !el.getAttribute('data-has-listener')) {
        el.addEventListener('input', () => this.updateMockupPreview());
        el.addEventListener('change', () => this.updateMockupPreview());
        el.setAttribute('data-has-listener', 'true');
      }
    });

    // Render mockup preview
    this.updateMockupPreview();

    // Navigate to the view
    appRouter.navigate('design-studio');

    // Fetch designs from API
    try {
      const resp = await fetch(`/api/designs/?product_type=${this.activeProductType}`);
      const designs = await resp.json();
      this.allDesigns = designs;
      this.renderFilters(designs);
      this.renderDesigns(designs);
    } catch (e) {
      if (grid) grid.innerHTML = `<div class="ds-empty"><i class="fa-solid fa-triangle-exclamation"></i><p>Failed to load designs. Please try again.</p></div>`;
    }

    // Load product reviews
    reviewsController.loadReviews(productId);
  },

  close() {
    this.hideSelectedBar();
    appRouter.navigate('products');
  },

  renderFilters(designs) {
    const bar = document.getElementById('ds-filter-bar');
    if (!bar) return;

    // Collect unique categories
    const cats = ['all', ...new Set(designs.map(d => d.category))];
    const LABEL = {
      all: 'All Designs',
      birthday: 'Birthday',
      love: 'Love & Anniversary',
      family: 'Family & Parents',
      friends: 'Friends',
      cats: 'Cats & Pets',
      general: 'General & Holiday',
      motivational: 'Motivational',
      custom: 'Custom / Other',
    };

    bar.innerHTML = cats.map(cat =>
      `<button class="ds-filter-pill ${cat === this.activeCategory ? 'active' : ''}" onclick="designStudio.filterByCategory('${cat}')">${LABEL[cat] || cat}</button>`
    ).join('');
  },

  filterByCategory(cat) {
    this.activeCategory = cat;
    document.querySelectorAll('.ds-filter-pill').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.ds-filter-pill').forEach(p => {
      if (p.textContent.trim() === (cat === 'all' ? 'All Designs' : p.textContent.trim()) && p.getAttribute('onclick').includes(`'${cat}'`)) p.classList.add('active');
    });
    const filtered = cat === 'all' ? this.allDesigns : this.allDesigns.filter(d => d.category === cat);
    this.renderDesigns(filtered);
  },

  renderDesigns(designs) {
    const grid = document.getElementById('ds-designs-grid');
    if (!grid) return;

    if (!designs || designs.length === 0) {
      grid.innerHTML = `<div class="ds-empty"><i class="fa-solid fa-palette"></i><p>No designs found for this category.<br>Try another filter or create your own below!</p></div>`;
      return;
    }

    // Build a lookup map so we can retrieve design objects by id without
    // embedding JSON.stringify in inline onclick attributes (which breaks on
    // names/categories containing quotes or apostrophes).
    designs.forEach(d => { this._designMap[d.id] = d; });

    grid.innerHTML = designs.map(d => {
      const save = Math.round((d.original_price - d.price) / d.original_price * 100);
      const isSelected = this.selectedDesign && this.selectedDesign.id === d.id;
      return `
        <div class="ds-card ${isSelected ? 'ds-selected' : ''}" id="ds-card-${d.id}" onclick="designStudio.selectDesignById(${d.id})">
          <div class="ds-selected-badge"><i class="fa-solid fa-check"></i></div>
          <img class="ds-card-img" src="${d.image_url}" alt="${d.name}" loading="lazy" onerror="this.style.background='#1a1a2e';this.alt='Design'" onclick="event.stopPropagation(); designStudio.showDesignPreviewById(${d.id});" style="cursor: pointer;">
          <div class="ds-card-info">
            <p class="ds-card-category">${d.category_label}</p>
            <h3 class="ds-card-name">${d.name}</h3>
            <div class="ds-card-price-row">
              <span class="ds-card-price">₹${d.price}</span>
              <span class="ds-card-original">₹${d.original_price}</span>
              <span class="ds-card-save">SAVE ${save}%</span>
            </div>
            <button class="ds-card-select-btn">${isSelected ? '<i class="fa-solid fa-check"></i> Selected' : 'Select This Design'}</button>
          </div>
        </div>
      `;
    }).join('');
  },

  showDesignPreview(designJson) {
    const design = typeof designJson === 'string' ? JSON.parse(designJson) : designJson;
    appRouter.showGlobalImagePreview(design.image_url, design.name, design.category_label || design.category);
  },

  showDesignPreviewById(id) {
    const design = this._designMap[id];
    if (design) this.showDesignPreview(design);
  },

  selectDesignById(id) {
    const design = this._designMap[id];
    if (design) this.selectDesign(design);
  },

  selectDesign(designJson) {
    const design = typeof designJson === 'string' ? JSON.parse(designJson) : designJson;
    this.selectedDesign = design;

    // Update all cards
    document.querySelectorAll('.ds-card').forEach(card => {
      card.classList.remove('ds-selected');
      const btn = card.querySelector('.ds-card-select-btn');
      if (btn) btn.innerHTML = 'Select This Design';
    });
    const selected = document.getElementById(`ds-card-${design.id}`);
    if (selected) {
      selected.classList.add('ds-selected');
      const btn = selected.querySelector('.ds-card-select-btn');
      if (btn) btn.innerHTML = '<i class="fa-solid fa-check"></i> Selected';
    }

    // Update mockup preview with selected design
    this.updateMockupPreview();

    // Show preview popup of the selected design
    this.showDesignPreview(design);

    // Show bottom bar and guide the customer to upload photo/text
    this.showSelectedBar(design);
    this.promptCustomForSelectedDesign();
  },

  promptCustomForSelectedDesign() {
    if (!this.selectedDesign) return;
    this.openCustomModal(this.selectedDesign);
  },

  openCustomModal(design) {
    // Reset state
    this.modalPhotoBase64 = null;
    this.modalPhotoBothBase64 = null;
    this.modalActiveTab = 'photo';

    // Populate header
    const img = document.getElementById('ds-modal-design-img');
    const name = document.getElementById('ds-modal-design-name');
    if (img) { img.src = design.image_url; img.alt = design.name; }
    if (name) name.textContent = design.name;

    // Reset tabs to photo
    this.switchModalTab('photo');

    // Clear all inputs
    const fileIn = document.getElementById('ds-modal-file-input');
    const fileInBoth = document.getElementById('ds-modal-file-input-both');
    if (fileIn) fileIn.value = '';
    if (fileInBoth) fileInBoth.value = '';
    const preview = document.getElementById('ds-modal-photo-preview');
    const previewBoth = document.getElementById('ds-modal-photo-preview-both');
    if (preview) preview.style.display = 'none';
    if (previewBoth) previewBoth.style.display = 'none';
    const txt = document.getElementById('ds-modal-custom-text');
    const txtBoth = document.getElementById('ds-modal-custom-text-both');
    if (txt) txt.value = '';
    if (txtBoth) txtBoth.value = '';
    const status = document.getElementById('ds-modal-status');
    if (status) status.textContent = '';

    // Open overlay
    const overlay = document.getElementById('ds-customization-modal-overlay');
    if (overlay) overlay.classList.add('active');
  },

  closeCustomModal() {
    const overlay = document.getElementById('ds-customization-modal-overlay');
    if (overlay) overlay.classList.remove('active');
  },

  switchModalTab(tab) {
    this.modalActiveTab = tab;
    const tabs = ['photo', 'text', 'both'];
    tabs.forEach(t => {
      const btn = document.getElementById(`ds-modal-tab-${t}`);
      const panel = document.getElementById(`ds-modal-panel-${t}`);
      if (t === tab) {
        if (btn) {
          btn.style.border = '1.5px solid rgba(168,85,247,0.4)';
          btn.style.background = 'rgba(168,85,247,0.15)';
          btn.style.color = '#fff';
        }
        if (panel) panel.style.display = 'block';
      } else {
        if (btn) {
          btn.style.border = '1.5px solid rgba(255,255,255,0.1)';
          btn.style.background = 'rgba(255,255,255,0.04)';
          btn.style.color = 'var(--text-secondary)';
        }
        if (panel) panel.style.display = 'none';
      }
    });
    const status = document.getElementById('ds-modal-status');
    if (status) status.textContent = '';
  },

  handleModalPhotoUpload(input) {
    const file = input.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      this.modalPhotoBase64 = e.target.result;
      const preview = document.getElementById('ds-modal-photo-preview');
      const img = document.getElementById('ds-modal-photo-preview-img');
      const nameLbl = document.getElementById('ds-modal-photo-name');
      if (preview) preview.style.display = 'block';
      if (img) img.src = e.target.result;
      if (nameLbl) nameLbl.textContent = file.name;
    };
    reader.readAsDataURL(file);
  },

  handleModalPhotoUploadBoth(input) {
    const file = input.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      this.modalPhotoBothBase64 = e.target.result;
      const preview = document.getElementById('ds-modal-photo-preview-both');
      const img = document.getElementById('ds-modal-photo-preview-img-both');
      if (preview) preview.style.display = 'block';
      if (img) img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  },

  clearModalPhoto() {
    this.modalPhotoBase64 = null;
    const fileIn = document.getElementById('ds-modal-file-input');
    if (fileIn) fileIn.value = '';
    const preview = document.getElementById('ds-modal-photo-preview');
    if (preview) preview.style.display = 'none';
  },

  addCustomFromModal() {
    const status = document.getElementById('ds-modal-status');
    const tab = this.modalActiveTab || 'photo';
    let customizationType = 'text';
    let customizationData = '';
    let font = '';
    let color = '';
    let summary = '';

    if (tab === 'photo') {
      if (!this.modalPhotoBase64) {
        if (status) status.textContent = '⚠ Please upload a photo first.';
        return;
      }
      customizationType = 'photo';
      customizationData = this.modalPhotoBase64;
      summary = 'Custom photo upload';
    } else if (tab === 'text') {
      const text = (document.getElementById('ds-modal-custom-text')?.value || '').trim();
      if (!text) {
        if (status) status.textContent = '⚠ Please enter your message or name.';
        return;
      }
      font = document.getElementById('ds-modal-custom-font')?.value || 'Modern';
      color = document.getElementById('ds-modal-custom-color')?.value || 'White';
      customizationType = 'text';
      customizationData = text;
      summary = `Text: "${text.substring(0, 40)}" | Font: ${font} | Color: ${color}`;
    } else { // both
      const text = (document.getElementById('ds-modal-custom-text-both')?.value || '').trim();
      if (!this.modalPhotoBothBase64 && !text) {
        if (status) status.textContent = '⚠ Please upload a photo or enter text (or both).';
        return;
      }
      font = document.getElementById('ds-modal-custom-font-both')?.value || 'Modern';
      color = document.getElementById('ds-modal-custom-color-both')?.value || 'White';
      if (this.modalPhotoBothBase64) {
        customizationType = 'photo';
        customizationData = this.modalPhotoBothBase64;
      } else {
        customizationType = 'text';
        customizationData = text;
      }
      summary = text
        ? `Photo + Text: "${text.substring(0, 30)}" | Font: ${font} | Color: ${color}`
        : 'Custom photo upload';
    }

    const activeId = Number(this.activeProductId);
    const catalogProduct = productCatalog.getProductById(activeId);
    const selected = this.selectedDesign;
    const productName = selected
      ? `${this.activeProductName?.replace(' Designs', '') || 'Product'} — ${selected.name}`
      : `Custom ${this.activeProductName?.replace(' Designs', '') || 'Product'}`;
    const productImage = selected ? selected.image_url : (catalogProduct?.image || '');

    const product = {
      id: activeId,
      name: productName,
      price: selected ? (parseFloat(selected.price) || catalogProduct?.price || 219) : (catalogProduct?.price || 219),
      originalPrice: selected ? (parseFloat(selected.original_price) || catalogProduct?.originalPrice || 299) : (catalogProduct?.originalPrice || 299),
      image: productImage,
      category: this.PRODUCT_TYPE_MAP[activeId] || 'mug',
      cartPrice: catalogProduct?.cartPrice || null,
    };

    const customization = {
      type: customizationType,
      data: customizationData,
      font,
      color,
      size: '',
      summary: selected ? `${summary} | Design: ${selected.name}` : summary,
      designId: selected?.id,
      designName: selected?.name,
      designImageUrl: selected?.image_url,
    };

    this.closeCustomModal();
    this.hideSelectedBar();
    cartManager.addToCart(product, customization);
  },

  showSelectedBar(design) {
    let bar = document.getElementById('ds-selected-bar');
    if (!bar) {
      bar = document.createElement('div');
      bar.id = 'ds-selected-bar';
      bar.className = 'ds-selected-bar';
      bar.innerHTML = `
        <div class="ds-selected-bar-info">
          <img class="ds-selected-bar-img" id="ds-bar-img" src="" alt="">
          <div class="ds-selected-bar-text">
            <p>Selected Design</p>
            <h4 id="ds-bar-name"></h4>
          </div>
        </div>
        <div style="display:flex;gap:12px;align-items:center;">
          <span id="ds-bar-price" style="font-size:1.1rem;font-weight:800;color:#fff;"></span>
          <button class="btn-primary" onclick="designStudio.promptCustomForSelectedDesign()" style="padding:12px 28px;font-size:0.9rem;font-weight:700;border-radius:25px;">
            Use with Upload/Text <i class="fa-solid fa-arrow-right" style="margin-left:6px;"></i>
          </button>
        </div>
      `;
      document.body.appendChild(bar);
    }

    document.getElementById('ds-bar-img').src = design.image_url;
    document.getElementById('ds-bar-img').alt = design.name;
    document.getElementById('ds-bar-name').textContent = design.name;
    document.getElementById('ds-bar-price').textContent = `₹${design.price}`;

    requestAnimationFrame(() => bar.classList.add('visible'));
  },

  hideSelectedBar() {
    const bar = document.getElementById('ds-selected-bar');
    if (bar) bar.classList.remove('visible');
  },

  resetState() {
    this.selectedDesign = null;
    this.customPhotoBase64 = null;
    this.customPhotoBothBase64 = null;
    this.hideSelectedBar();
    // Hide the selected design summary block if present
    const summary = document.getElementById('ds-selected-design-summary');
    if (summary) summary.style.display = 'none';
    const status = document.getElementById('ds-custom-status');
    if (status) status.textContent = '';
    this.updateMockupPreview();
  },

  addDesignToCart() {
    if (!this.selectedDesign) return;
    const d = this.selectedDesign;
    const activeId = Number(this.activeProductId);
    const catalogProduct = productCatalog.getProductById(activeId);
    const product = {
      id: activeId,
      name: `${this.activeProductName.replace(' Designs', '')} — ${d.name}`,
      price: parseFloat(d.price) || 219,
      originalPrice: parseFloat(d.original_price) || 299,
      image: d.image_url,
      category: this.PRODUCT_TYPE_MAP[activeId] || 'mug',
      cartPrice: catalogProduct?.cartPrice || null,
    };
    const customization = {
      type: 'photo',
      data: d.image_url,
      font: '',
      color: '',
      size: '',
      summary: `Design: ${d.name} (${d.category_label})`,
      designId: d.id,
      designName: d.name,
      designImageUrl: d.image_url,
    };
    cartManager.addToCart(product, customization);
    this.hideSelectedBar();
    appRouter.navigate('cart');
  },

  switchTab(tab) {
    this.activeTab = tab;
    document.querySelectorAll('.ds-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.ds-tab-panel').forEach(p => p.classList.remove('active'));
    const activeTabEl = document.querySelector(`.ds-tab[data-tab="${tab}"]`);
    const activePanelEl = document.getElementById(`ds-tab-${tab}`);
    if (activeTabEl) activeTabEl.classList.add('active');
    if (activePanelEl) activePanelEl.classList.add('active');
    this.updateMockupPreview();
  },

  handlePhotoUpload(input) {
    const file = input.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      this.customPhotoBase64 = e.target.result;
      const preview = document.getElementById('ds-photo-preview');
      const img = document.getElementById('ds-photo-preview-img');
      const name = document.getElementById('ds-photo-name');
      if (preview) preview.style.display = 'block';
      if (img) img.src = e.target.result;
      if (name) name.textContent = file.name;
      this.updateMockupPreview();
    };
    reader.readAsDataURL(file);
  },

  handlePhotoUploadBoth(input) {
    const file = input.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      this.customPhotoBothBase64 = e.target.result;
      const preview = document.getElementById('ds-photo-preview-both');
      const img = document.getElementById('ds-photo-preview-img-both');
      if (preview) preview.style.display = 'block';
      if (img) img.src = e.target.result;
      this.updateMockupPreview();
    };
    reader.readAsDataURL(file);
  },

  addCustomToCart() {
    const tab = this.activeTab;
    const status = document.getElementById('ds-custom-status');
    let customizationType = 'text';
    let customizationData = '';
    let font = '';
    let color = '';
    let summary = '';

    if (tab === 'photo') {
      if (!this.customPhotoBase64) {
        if (status) status.textContent = '⚠ Please upload a photo first.';
        return;
      }
      customizationType = 'photo';
      customizationData = this.customPhotoBase64;
      summary = 'Custom photo upload';
    } else if (tab === 'text') {
      const text = (document.getElementById('ds-custom-text')?.value || '').trim();
      if (!text) {
        if (status) status.textContent = '⚠ Please enter your message or name.';
        return;
      }
      font = document.getElementById('ds-custom-font')?.value || 'Modern';
      color = document.getElementById('ds-custom-color')?.value || 'White';
      customizationType = 'text';
      customizationData = text;
      summary = `Text: "${text.substring(0, 40)}" | Font: ${font} | Color: ${color}`;
    } else { // both
      const text = (document.getElementById('ds-custom-text-both')?.value || '').trim();
      if (!this.customPhotoBothBase64 && !text) {
        if (status) status.textContent = '⚠ Please upload a photo or enter text.';
        return;
      }
      font = document.getElementById('ds-custom-font-both')?.value || 'Modern';
      color = document.getElementById('ds-custom-color-both')?.value || 'White';
      if (this.customPhotoBothBase64) {
        customizationType = 'photo';
        customizationData = this.customPhotoBothBase64;
      } else {
        customizationType = 'text';
        customizationData = text;
      }
      summary = text
        ? `Photo + Text: "${text.substring(0, 30)}" | Font: ${font} | Color: ${color}`
        : 'Custom photo upload';
    }

    if (status) status.textContent = '';

    const activeId = Number(this.activeProductId);
    const catalogProduct = productCatalog.getProductById(activeId);
    const selected = this.selectedDesign;
    const productName = selected
      ? `${this.activeProductName?.replace(' Designs', '') || 'Product'} — ${selected.name}`
      : `Custom ${this.activeProductName?.replace(' Designs', '') || 'Product'}`;
    const productImage = selected ? selected.image_url : (catalogProduct?.image || '');

    const product = {
      id: activeId,
      name: productName,
      price: catalogProduct?.price || 219,
      originalPrice: catalogProduct?.originalPrice || 299,
      image: productImage,
      category: this.PRODUCT_TYPE_MAP[activeId] || 'mug',
      cartPrice: catalogProduct?.cartPrice || null,
    };

    const customization = {
      type: customizationType,
      data: customizationData,
      font,
      color,
      size: '',
      summary: selected ? `${summary} | Design: ${selected.name}` : summary,
      designId: selected?.id,
      designName: selected?.name,
      designImageUrl: selected?.image_url,
    };

    cartManager.addToCart(product, customization);
    appRouter.navigate('cart');
  },
};

// --- 5. CART & CHECKOUT MANAGER ---
const cartManager = {
  init() {
    // Load existing cart items
    const savedCart = localStorage.getItem('inkify_cart');
    if (savedCart) {
      STATE.cart = JSON.parse(savedCart);
      this.updateBadge();
    }
  },

  async addToCart(product, customization) {
    // Add item to global cart with customization attributes
    STATE.cart.push({
      cartItemId: `cart-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      product: { ...product },
      customization: customization,
      quantity: 1
    });

    this.saveCart();
    this.updateBadge();

    // Navigate directly to cart page
    appRouter.navigate('cart');
  },

  saveCart() {
    localStorage.setItem('inkify_cart', JSON.stringify(STATE.cart));
  },

  updateBadge() {
    const totalQty = STATE.cart.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('cart-badge-count').textContent = totalQty;
  },

  updateQuantity(cartItemId, delta) {
    const item = STATE.cart.find(i => i.cartItemId === cartItemId);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
      STATE.cart = STATE.cart.filter(i => i.cartItemId !== cartItemId);
    }

    this.saveCart();
    this.updateBadge();
    this.renderCart();
  },

  removeItem(cartItemId) {
    STATE.cart = STATE.cart.filter(i => i.cartItemId !== cartItemId);
    this.saveCart();
    this.updateBadge();
    this.renderCart();
  },

  toggleDeliveryType() {
    const radioSaved = document.getElementById('delivery-type-saved');
    const inputContainer = document.getElementById('checkout-shipping-input-fields');
    if (!inputContainer) return;

    const inputs = ['shipping-name', 'shipping-phone', 'shipping-email', 'shipping-street', 'shipping-city', 'shipping-pincode'];

    if (radioSaved && radioSaved.checked && STATE.currentUser && STATE.currentUser.address) {
      inputContainer.style.display = 'none';
      inputs.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.required = false;
      });
    } else {
      inputContainer.style.display = 'block';
      inputs.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.required = true;
          if (id === 'shipping-email' && STATE.currentUser && !el.value) {
            el.value = STATE.currentUser.email || '';
          }
          if (id === 'shipping-name' && STATE.currentUser && !el.value) {
            el.value = STATE.currentUser.name || '';
          }
          if (id === 'shipping-phone' && STATE.currentUser && !el.value) {
            el.value = STATE.currentUser.mobile || '';
          }
        }
      });
    }
  },

  editSavedAddress() {
    const savedRadio = document.getElementById('delivery-type-saved');
    const otherRadio = document.getElementById('delivery-type-other');
    const inputContainer = document.getElementById('checkout-shipping-input-fields');
    const actionBar = document.getElementById('checkout-address-action-bar');
    const inputs = ['shipping-name', 'shipping-phone', 'shipping-email', 'shipping-street', 'shipping-city', 'shipping-pincode'];

    if (savedRadio) savedRadio.checked = false;
    if (otherRadio) otherRadio.checked = true;
    if (inputContainer) inputContainer.style.display = 'block';
    if (actionBar) actionBar.style.display = 'none';

    inputs.forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      if (id === 'shipping-email' && STATE.currentUser && !el.value) {
        el.value = STATE.currentUser.email || '';
      }
      if (id === 'shipping-name' && STATE.currentUser && !el.value) {
        el.value = STATE.currentUser.name || '';
      }
      if (id === 'shipping-phone' && STATE.currentUser && !el.value) {
        el.value = STATE.currentUser.mobile || '';
      }
      if (id === 'shipping-street' && STATE.currentUser && STATE.currentUser.address && !el.value) {
        el.value = STATE.currentUser.address;
      }
      el.required = true;
    });

    this.toggleDeliveryType();
    const firstField = document.getElementById('shipping-street');
    if (firstField) firstField.focus();
  },

  async applyCoupon() {
    const couponInput = document.getElementById('checkout-coupon');
    const msg = document.getElementById('coupon-msg');
    const code = couponInput.value.trim().toUpperCase();

    if (!code) {
      msg.textContent = "Please enter a valid coupon code.";
      msg.className = "coupon-status-msg error";
      msg.style.display = "block";
      return;
    }

    // Check if they have the Whole Set in their cart
    const hasWholeSet = STATE.cart.some(item => item.product.id === 5);

    if (!hasWholeSet) {
      msg.textContent = "Referral code active! Add 'The Purple Gifting Set' to unlock ₹100 discount + ₹50 wallet credit!";
      msg.className = "coupon-status-msg error";
      msg.style.display = "block";
      return;
    }

    msg.textContent = "Verifying coupon code...";
    msg.className = "coupon-status-msg info";
    msg.style.display = "block";

    try {
      const response = await fetch(`${API_BASE_URL}/referrals/verify/${code}/`);
      const data = await response.json();

      if (response.ok && data.valid) {
        STATE.activeReferralCode = code;
        STATE.activeReferralUser = data.referrer;

        msg.innerHTML = `<i class="fa-solid fa-square-check"></i> Code Applied! You pay ₹1149 for the Whole Set. Buyer & Referrer earn ₹50 back.`;
        msg.className = "coupon-status-msg success";
        msg.style.display = "block";

        this.calculateTotals();
      } else {
        throw new Error(data.error || "Invalid coupon code.");
      }
    } catch (err) {
      msg.textContent = err.message || "Invalid coupon code. Try using your friend's affiliate referral code (e.g., SARA99).";
      msg.className = "coupon-status-msg error";
      msg.style.display = "block";

      STATE.activeReferralCode = null;
      STATE.activeReferralUser = null;
      this.calculateTotals();
    }
  },

  selectPayment(mode) {
    STATE.activePaymentMode = mode;

    // Toggle active classes on cards
    document.querySelectorAll('.payment-card').forEach(card => {
      if (card.getAttribute('data-payment') === mode) {
        card.classList.add('active');
      } else {
        card.classList.remove('active');
      }
    });

    this.calculateTotals();
  },

  toggleWalletUse() {
    STATE.useWalletCredit = !STATE.useWalletCredit;
    this.calculateTotals();
  },

  calculateTotals() {
    let subtotal = 0;
    let referralDiscount = 0;
    let walletCredit = 0;
    STATE.walletUsedAmount = 0;

    STATE.cart.forEach(item => {
      // Custom business pricing rule: Set is ₹1199 in cart
      let price = Number(item.product.id) === 5 ? (item.product.cartPrice || 1199) : item.product.price;
      price = parseFloat(price);
      if (isNaN(price)) {
        price = Number(item.product.id) === 5 ? 1199 : 219;
      }
      subtotal += price * item.quantity;

      if (Number(item.product.id) === 5 && STATE.activeReferralCode) {
        referralDiscount += 50 * item.quantity; // ₹50 direct discount when a valid referral code applies to the Whole Set
        walletCredit += 50 * item.quantity; // buyer earns ₹50 into wallet
      }
    });

    let grandTotal = subtotal - referralDiscount;
    if (STATE.currentUser && STATE.useWalletCredit && Number(STATE.currentUser.wallet_balance) > 0) {
      STATE.walletUsedAmount = Math.min(Number(STATE.currentUser.wallet_balance), grandTotal);
      grandTotal -= STATE.walletUsedAmount;
    }

    // Update summary labels
    document.getElementById('summary-items-subtotal').textContent = `₹${subtotal}`;
    document.getElementById('summary-grand-total').textContent = `₹${grandTotal}`;

    const discRow = document.getElementById('summary-referral-discount-row');
    const discVal = document.getElementById('summary-referral-discount-val');
    const walletRow = document.getElementById('summary-wallet-credit-row');
    const walletVal = document.getElementById('summary-wallet-credit-val');
    const walletUseRow = document.getElementById('summary-wallet-use-row');
    const walletUseVal = document.getElementById('summary-wallet-use-val');

    if (referralDiscount > 0) {
      discVal.textContent = `-₹${referralDiscount}`;
      discRow.style.display = 'flex';
      walletVal.textContent = `+₹${walletCredit}`;
      walletRow.style.display = 'flex';
    } else {
      discRow.style.display = 'none';
      walletRow.style.display = 'none';
    }

    if (STATE.walletUsedAmount > 0) {
      walletUseVal.textContent = `-₹${STATE.walletUsedAmount}`;
      walletUseRow.style.display = 'flex';
    } else {
      walletUseRow.style.display = 'none';
    }

    return grandTotal;
  },

  renderCart() {
    const listContainer = document.getElementById('cart-items-list-container');
    const addressContainer = document.getElementById('cart-shipping-address-container');
    const summaryPanel = document.getElementById('cart-summary-checkout-panel');
    const countIndicator = document.getElementById('cart-items-count-indicator');

    listContainer.innerHTML = '';

    if (STATE.cart.length === 0) {
      listContainer.innerHTML = `
        <div class="empty-cart-message">
          <i class="fa-solid fa-basket-shopping"></i>
          <h3>Your shopping bag is completely empty</h3>
          <p style="margin-top: 10px; margin-bottom: 24px;">Explore our premium custom canvases to build your vibe blueprints.</p>
          <button class="btn-primary" onclick="appRouter.navigate('products')">Browse Products</button>
        </div>
      `;
      addressContainer.style.display = 'none';
      summaryPanel.style.display = 'none';
      countIndicator.textContent = '(0 items)';
      return;
    }

    addressContainer.style.display = 'block';
    summaryPanel.style.display = 'block';
    countIndicator.textContent = `(${STATE.cart.reduce((sum, item) => sum + item.quantity, 0)} items)`;

    // Sync Referral Coupon UI state based on active global coupon and cart contents
    const hasWholeSet = STATE.cart.some(item => item.product.id === 5);
    const couponInput = document.getElementById('checkout-coupon');
    const couponMsg = document.getElementById('coupon-msg');
    const walletPanel = document.getElementById('wallet-usage-panel');
    const walletAvailable = document.getElementById('checkout-wallet-available');
    const walletCheckbox = document.getElementById('wallet-use-checkbox');

    if (!hasWholeSet) {
      STATE.activeReferralCode = null;
      STATE.activeReferralUser = null;
    }

    if (STATE.activeReferralCode) {
      couponInput.value = STATE.activeReferralCode;
      couponMsg.innerHTML = `<i class="fa-solid fa-square-check"></i> Code Applied! You pay ₹1099 for the Whole Set and earn ₹50 back into your wallet.`;
      couponMsg.className = "coupon-status-msg success";
      couponMsg.style.display = "block";
    } else {
      couponInput.value = "";
      couponMsg.textContent = "";
      couponMsg.className = "coupon-status-msg";
      couponMsg.style.display = "none";
    }

    if (STATE.currentUser && Number(STATE.currentUser.wallet_balance) > 0) {
      walletPanel.style.display = 'block';
      walletAvailable.textContent = Number(STATE.currentUser.wallet_balance).toFixed(2);
      walletCheckbox.checked = STATE.useWalletCredit;
    } else if (walletPanel) {
      walletPanel.style.display = 'none';
      if (walletCheckbox) walletCheckbox.checked = false;
      STATE.useWalletCredit = false;
    }

    // Toggle delivery mode selector dynamically
    const modeSelector = document.getElementById('checkout-delivery-mode');
    const savedDisplay = document.getElementById('checkout-saved-details-display');
    const inputFields = document.getElementById('checkout-shipping-input-fields');

    const addressActionBar = document.getElementById('checkout-address-action-bar');
    if (STATE.currentUser && STATE.currentUser.address) {
      if (modeSelector) modeSelector.style.display = 'block';
      if (addressActionBar) {
        addressActionBar.style.display = 'none';
        addressActionBar.innerHTML = '';
      }
      if (savedDisplay) {
        savedDisplay.innerHTML = `
          <button class="btn-secondary" onclick="cartManager.editSavedAddress()" style="margin-bottom: 12px;">Change Address</button>
          <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
            <div style="margin-bottom: 4px;"><strong>Recipient Name:</strong> ${STATE.currentUser.name || '-'}</div>
            <div style="margin-bottom: 4px;"><strong>Contact Mobile:</strong> +91-${STATE.currentUser.mobile || '-'}</div>
            <div style="margin-bottom: 4px;"><strong>Email Address:</strong> ${STATE.currentUser.email || '-'}</div>
            <div><strong>Shipping Address:</strong> ${STATE.currentUser.address || '-'}</div>
          </div>
        `;
      }
      this.toggleDeliveryType();
    } else {
      if (modeSelector) modeSelector.style.display = 'none';
      if (addressActionBar) {
        addressActionBar.style.display = 'block';
        addressActionBar.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; background: rgba(255,255,255,0.02); padding: 14px 16px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.04);">
            <div style="font-size: 0.92rem; color: var(--text-secondary);">
              ${STATE.currentUser ? 'No saved shipping address found. Add your delivery address below.' : 'Enter your shipping information below to proceed.'}
            </div>
            ${STATE.currentUser ? '<button class="btn-secondary" onclick="cartManager.editSavedAddress()">Add Address</button>' : ''}
          </div>
        `;
      }
      if (inputFields) inputFields.style.display = 'block';
      const inputs = ['shipping-name', 'shipping-phone', 'shipping-email', 'shipping-street', 'shipping-city', 'shipping-pincode'];
      inputs.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.required = true;
      });
    }

    STATE.cart.forEach(item => {
      let price = Number(item.product.id) === 5 ? (item.product.cartPrice || 1199) : item.product.price;
      price = parseFloat(price);
      if (isNaN(price)) {
        price = Number(item.product.id) === 5 ? 1199 : 219;
      }
      const colorBadge = item.customization.color
        ? `<span style="display:inline-block; font-size:0.75rem; background:rgba(255,255,255,0.08); padding:2px 6px; border-radius:4px; margin-top:6px; color:var(--text-secondary);"><i class="fa-solid fa-palette" style="color:var(--accent-light); margin-right:4px;"></i> Fabric Color: <strong>${item.customization.color}</strong></span>`
        : '';

      let designBadge = '';
      if (item.customization.designName) {
        designBadge = `
          <div class="cart-item-design-badge" style="display:flex; align-items:center; gap:8px; margin-bottom:8px; background:rgba(108,99,255,0.08); border:1px solid rgba(108,99,255,0.15); padding:6px 12px; border-radius:6px; max-width: fit-content;">
            <img src="${item.customization.designImageUrl}" style="width:28px; height:28px; border-radius:4px; object-fit:cover;" alt="${item.customization.designName}">
            <span style="font-size:0.8rem; color:#fff;">Design: <strong>${item.customization.designName}</strong></span>
          </div>
        `;
      }

      const customSpec = item.customization.type === 'photo'
        ? `${designBadge}<span>📸 Custom Photograph Printed</span><img src="${item.customization.data}" class="cart-item-custom-img">${colorBadge}`
        : `${designBadge}<span style="font-family: ${item.customization.font}; font-size: 0.95rem; font-weight: 700; color: white;">Printed: "${item.customization.data}"</span>${colorBadge}`;

      const itemHtml = `
        <div class="cart-item-row">
          <div class="cart-item-thumb">
            ${item.product.image.startsWith('<svg') ? item.product.image : `<img src="${appRouter.getAssetUrl(item.product.image)}" alt="${item.product.name}">`}
          </div>
          <div class="custom photograph printed">
            <h4>${item.product.name}</h4>
            <div class="cart-item-customization">
              ${customSpec}
            </div>
          </div>
          <div class="cart-item-qty">
            <span class="qty-btn" onclick="cartManager.updateQuantity('${item.cartItemId}', -1)">-</span>
            <span>${item.quantity}</span>
            <span class="qty-btn" onclick="cartManager.updateQuantity('${item.cartItemId}', 1)">+</span>
          </div>
          <div class="cart-item-price">
            ₹${price * item.quantity}
            <i class="fa-regular fa-trash-can cart-item-remove" onclick="cartManager.removeItem('${item.cartItemId}')" title="Delete product"></i>
          </div>
        </div>
      `;
      listContainer.insertAdjacentHTML('beforeend', itemHtml);
    });

    this.calculateTotals();
  },

  async placeOrder() {
    // 1. Validate Shipping Forms
    const radioSaved = document.getElementById('delivery-type-saved');
    const useSaved = radioSaved && radioSaved.checked && STATE.currentUser && STATE.currentUser.address;

    if (!useSaved) {
      const name = document.getElementById('shipping-name').value.trim();
      const phone = document.getElementById('shipping-phone').value.trim();
      const email = document.getElementById('shipping-email').value.trim();
      const street = document.getElementById('shipping-street').value.trim();
      const city = document.getElementById('shipping-city').value.trim();
      const pincode = document.getElementById('shipping-pincode').value.trim();

      if (!name || !phone || !email || !street || !city || !pincode) {
        alert("Please fill in all the required recipient and shipping address fields (*)");
        return;
      }

      if (!/^\d{10}$/.test(phone)) {
        alert("Contact Mobile Number must be precisely 10 digits containing only digits");
        return;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        alert("Please provide a valid email address");
        return;
      }

      if (!/^\d{6}$/.test(pincode)) {
        alert("PIN Code must be precisely 6 digits containing only digits");
        return;
      }
    }

    const finalAmount = this.calculateTotals();

    if (STATE.activePaymentMode === 'cod') {
      await this.placeOrderConfirm();
    } else {
      paymentGatewayManager.openGateway(finalAmount);
    }
  },

  async placeOrderConfirm() {
    const radioSaved = document.getElementById('delivery-type-saved');
    const useSaved = radioSaved && radioSaved.checked && STATE.currentUser && STATE.currentUser.address;

    let finalName = "";
    let finalPhone = "";
    let finalEmail = "";
    let shippingAddress = "";

    if (useSaved) {
      finalName = STATE.currentUser.name;
      finalPhone = STATE.currentUser.mobile;
      finalEmail = STATE.currentUser.email;
      shippingAddress = STATE.currentUser.address;
    } else {
      finalName = document.getElementById('shipping-name').value.trim();
      finalPhone = document.getElementById('shipping-phone').value.trim();
      finalEmail = document.getElementById('shipping-email').value.trim();
      
      const street = document.getElementById('shipping-street').value.trim();
      const city = document.getElementById('shipping-city').value.trim();
      const pincode = document.getElementById('shipping-pincode').value.trim();
      shippingAddress = `${street}, ${city} - ${pincode}`;
    }

    const finalAmount = this.calculateTotals();
    const estDelivery = getDeliveryDateString(5);

    const itemsPayload = STATE.cart.map(item => {
      let price = Number(item.product.id) === 5 ? (item.product.cartPrice || 1199) : item.product.price;
      price = parseFloat(price);
      if (isNaN(price)) {
        price = Number(item.product.id) === 5 ? 1199 : 219;
      }
      return {
        product_id: item.product.id,
        quantity: item.quantity,
        price: price,
        customization: {
          type: item.customization.type,
          data: item.customization.data,
          font: item.customization.font || null,
          color: item.customization.color || null,
          size: item.customization.size || null,
          summary: item.customization.summary
        }
      };
    });

    const orderPayload = {
      customer_name: finalName,
      customer_phone: finalPhone,
      customer_email: finalEmail,
      shipping_address: shippingAddress,
      amount: finalAmount,
      payment_mode: STATE.activePaymentMode === 'cod'
        ? 'Cash on Delivery'
        : STATE.activePaymentMode === 'upi'
          ? 'Online Payment (UPI)'
          : 'Online Payment (Card)',
      referral_code: STATE.activeReferralCode,
      wallet_used: STATE.walletUsedAmount || 0,
      est_delivery: estDelivery,
      items: itemsPayload
    };

    try {
      const headers = { 'Content-Type': 'application/json' };
      if (STATE.currentUser && STATE.currentUser.token) {
        headers['Authorization'] = `Token ${STATE.currentUser.token}`;
      }

      const response = await fetch(`${API_BASE_URL}/orders/`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(orderPayload)
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Order placement failed");
      }

      if (data.user) {
        STATE.currentUser.wallet_balance = data.user.wallet_balance || STATE.currentUser.wallet_balance || 0;
        STATE.currentUser.referral_code = data.user.referral_code || STATE.currentUser.referral_code || null;
        localStorage.setItem('inkify_user', JSON.stringify(STATE.currentUser));
        authManager.updateHeaderUI();
      }

      // Purge cart states
      STATE.cart = [];
      this.saveCart();
      this.updateBadge();

      STATE.activeReferralCode = null;
      STATE.activeReferralUser = null;

      // Show success view
      document.getElementById('success-tracking-id-text').textContent = data.tracking_id;
      document.getElementById('success-delivery-date-text').textContent = data.est_delivery;
      // Reset design studio selection so the bar doesn't persist on success screen
      designStudio.resetState();
      appRouter.navigate('success');
    } catch (err) {
      alert(`Checkout error: ${err.message}`);
    }
  }
};

// --- 6. ORDER TRACKING MANAGER ---
const trackingManager = {
  async searchOrder() {
    const inputId = document.getElementById('tracking-input-id').value.trim().toUpperCase();
    if (!inputId) {
      alert("Please input a valid Reference Order Tracking ID");
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/orders/track/${inputId}/`);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error(`No active order found with Reference ID: ${inputId}`);
        }
        throw new Error("Failed to fetch order details from server");
      }

      const data = await response.json();
      // Map database order format to frontend format
      const frontOrder = {
        trackingId: data.tracking_id,
        paymentMode: data.payment_mode,
        estDelivery: data.est_delivery,
        status: data.status,
        items: data.items.map(item => ({
          product: {
            id: item.product_id,
            name: item.product_name,
            image: item.product_image
          },
          quantity: item.quantity,
          customization: {
            type: item.customization_type,
            data: item.customization_data,
            font: item.customization_font,
            color: item.customization_color,
            summary: item.customization_summary
          }
        }))
      };

      this.renderDashboard(frontOrder);
    } catch (err) {
      alert(err.message);
    }
  },

  async directTrackFromSuccess() {
    const trackingId = document.getElementById('success-tracking-id-text').textContent;
    try {
      const response = await fetch(`${API_BASE_URL}/orders/track/${trackingId}/`);
      if (response.ok) {
        const data = await response.json();
        const frontOrder = {
          trackingId: data.tracking_id,
          paymentMode: data.payment_mode,
          estDelivery: data.est_delivery,
          status: data.status,
          items: data.items.map(item => ({
            product: {
              id: item.product_id,
              name: item.product_name,
              image: item.product_image
            },
            quantity: item.quantity,
            customization: {
              type: item.customization_type,
              data: item.customization_data,
              font: item.customization_font,
              color: item.customization_color,
              summary: item.customization_summary
            }
          }))
        };
        this.renderDashboard(frontOrder);
        appRouter.navigate('tracking');
      }
    } catch (err) {
      console.error("Direct track error", err);
    }
  },

  renderDashboard(order) {
    const dashboard = document.getElementById('tracking-dashboard');
    dashboard.style.display = 'block';

    // Populate header specs
    document.getElementById('track-id-val').textContent = order.trackingId;
    document.getElementById('track-delivery-val').textContent = order.estDelivery;
    document.getElementById('track-payment-val').textContent = order.paymentMode;

    // Map order timeline status to index (Placed: 0, Printing: 1, Dispatched: 2, OutForDelivery: 3)
    let statusIndex = 0;
    let statusStr = "Order Placed";

    if (order.status === 'Placed') {
      statusIndex = 0;
      statusStr = "Ordered Locked";
    } else if (order.status === 'Printing') {
      statusIndex = 1;
      statusStr = "Printing Blueprint";
    } else if (order.status === 'Dispatched') {
      statusIndex = 2;
      statusStr = "Dispatched Cargo";
    } else if (order.status === 'Delivery') {
      statusIndex = 3;
      statusStr = "Out for Delivery";
    }

    document.getElementById('track-status-val').textContent = statusStr;

    // Configure Stepper node highlights
    const steps = [0, 1, 2, 3];
    steps.forEach(index => {
      const node = document.getElementById(`step-${index}`);
      node.className = "step-node"; // reset

      if (index < statusIndex) {
        node.classList.add('completed');
      } else if (index === statusIndex) {
        node.classList.add('active');
      }
    });

    // Stepper line fill percent
    const lineFill = document.getElementById('track-stepper-fill');
    if (window.innerWidth <= 768) {
      // Mobile vertical stepper line
      const percent = (statusIndex / 3) * 80;
      lineFill.style.height = `${percent}%`;
      lineFill.style.width = `4px`;
    } else {
      // Desktop horizontal stepper line
      const percent = (statusIndex / 3) * 80 + 10;
      lineFill.style.width = `${percent}%`;
      lineFill.style.height = `4px`;
    }

    // Render blueprint spec designs
    const specsContainer = document.getElementById('tracking-spec-items-container');
    specsContainer.innerHTML = '';

    order.items.forEach(item => {
      const colorBadge = item.customization.color
        ? `<br><span style="display:inline-block; font-size:0.75rem; background:rgba(255,255,255,0.08); padding:2px 6px; border-radius:4px; margin-top:6px; color:var(--text-secondary);"><i class="fa-solid fa-palette" style="color:var(--accent-light); margin-right:4px;"></i> Fabric Color: <strong>${item.customization.color}</strong></span>`
        : '';
      const customSpec = item.customization.type === 'photo'
        ? `<span>ðŸ“¸ Custom Photograph Printed</span><br><img src="${item.customization.data}" class="cart-item-custom-img" style="margin-top: 8px; width: 80px; height: 80px;">${colorBadge}`
        : `<span style="font-family: ${item.customization.font}; font-size: 1.1rem; font-weight: 700; color: white;">Printed: "${item.customization.data}"</span>${colorBadge}`;

      const specHtml = `
        <div class="tracking-summary-card">
          ${item.product.image.startsWith('<svg') ? `<div class="tracking-summary-img-svg" style="width: 60px; height: 60px; border-radius: 8px; overflow: hidden; border:1px solid rgba(255,255,255,0.05);">${item.product.image}</div>` : `<img src="${appRouter.getAssetUrl(item.product.image)}" alt="${item.product.name}" class="tracking-summary-img">`}
          <div>
            <h4 style="font-weight: 700; font-family: var(--font-display); font-size: 1.05rem; margin-bottom: 4px;">${item.product.name} (x${item.quantity})</h4>
            <div style="font-size: 0.8rem; color: var(--accent-light); margin-top: 6px;">
              ${customSpec}
            </div>
          </div>
        </div>
      `;
      specsContainer.insertAdjacentHTML('beforeend', specHtml);
    });
  }
};

const walletManager = {
  async fetchProfile() {
    if (!STATE.currentUser || !STATE.currentUser.token) return;
    try {
      const response = await fetch(`${API_BASE_URL}/user/profile/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${STATE.currentUser.token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        STATE.currentUser.wallet_balance = data.wallet_balance || 0;
        STATE.currentUser.referral_code = data.referral_code || null;
        localStorage.setItem('inkify_user', JSON.stringify(STATE.currentUser));
        authManager.updateHeaderUI();
      }
    } catch (err) {
      console.warn("Failed to fetch user profile", err);
    }
  },

  async openModal() {
    if (!STATE.currentUser) {
      authManager.openModal();
      return;
    }
    const modal = document.getElementById('wallet-modal-overlay');
    if (modal) modal.classList.add('active');
    this.renderModal();
    await this.fetchProfile();
    this.renderModal();
  },

  closeModal() {
    const modal = document.getElementById('wallet-modal-overlay');
    if (modal) modal.classList.remove('active');
  },

  renderModal() {
    const balanceEl = document.getElementById('wallet-modal-balance');
    const progressTextEl = document.getElementById('wallet-progress-text');
    const progressFillEl = document.getElementById('wallet-progress-fill');
    const actionAreaEl = document.getElementById('wallet-withdraw-action-area');
    const refCodeEl = document.getElementById('wallet-modal-refcode');

    if (!STATE.currentUser) return;

    const balance = Number(STATE.currentUser.wallet_balance || 0);
    balanceEl.textContent = `₹${balance.toFixed(2)}`;
    
    // Referral code display
    if (refCodeEl) {
      refCodeEl.textContent = STATE.currentUser.referral_code || 'Will generate after first purchase';
    }

    // Progress to withdrawal (500rs)
    const progressPercent = Math.min((balance / 500) * 100, 100);
    if (progressFillEl) progressFillEl.style.width = `${progressPercent}%`;
    if (progressTextEl) progressTextEl.textContent = `₹${balance.toFixed(2)} / ₹500`;

    if (actionAreaEl) {
      if (balance >= 500) {
        actionAreaEl.innerHTML = `
          <button class="btn-primary" style="width: 100%; justify-content: center; padding: 14px; box-shadow: var(--shadow-purple);" onclick="walletManager.requestWithdraw()">
            Withdraw Wallet Balance <i class="fa-solid fa-money-bill-transfer"></i>
          </button>
        `;
      } else {
        actionAreaEl.innerHTML = `
          <div class="wallet-locked-badge" style="background: rgba(255, 255, 255, 0.03); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px; font-size: 0.82rem; color: var(--text-secondary); text-align: center;">
            <i class="fa-solid fa-lock" style="margin-right: 6px;"></i> Withdrawal unlocks at ₹500. Keep sharing your code or use your balance on checkout.
          </div>
        `;
      }
    }
  },

  copyReferralCode() {
    if (!STATE.currentUser || !STATE.currentUser.referral_code) {
      alert("Referral code is not available yet.");
      return;
    }
    navigator.clipboard.writeText(STATE.currentUser.referral_code)
      .then(() => {
        alert("Referral code copied to clipboard!");
      })
      .catch(err => {
        console.error("Copy failed", err);
      });
  },

  async requestWithdraw() {
    if (!STATE.currentUser || !STATE.currentUser.token) {
      alert('Please sign in to access your wallet.');
      return;
    }

    if (Number(STATE.currentUser.wallet_balance) < 500) {
      alert('Withdrawals are available once your wallet balance reaches ₹500.');
      return;
    }

    // Step 1: Confirmation dialog
    const confirmWithdraw = await showCustomDialog({
      icon: '<i class="fa-solid fa-circle-question" style="color: var(--accent-light);"></i>',
      title: 'Confirm Withdrawal',
      message: 'Are you sure you want to withdraw money?',
      actions: [
        { label: 'Yes, Withdraw', value: 'yes', type: 'primary' },
        { label: 'Cancel', value: 'no', type: 'outline' }
      ]
    });

    if (confirmWithdraw !== 'yes') return;

    // Step 2: Open Bank Details Modal
    this.closeModal();

    // Populate user's name if available
    document.getElementById('withdraw-bank-holder').value = STATE.currentUser.name || '';
    document.getElementById('withdraw-bank-name').value = '';
    document.getElementById('withdraw-bank-account').value = '';
    document.getElementById('withdraw-bank-ifsc').value = '';

    const bankModal = document.getElementById('withdraw-bank-modal-overlay');
    if (bankModal) {
      bankModal.classList.add('active');
    }
  },

  closeBankModal() {
    const bankModal = document.getElementById('withdraw-bank-modal-overlay');
    if (bankModal) {
      bankModal.classList.remove('active');
    }
  },

  async submitBankDetails(event) {
    event.preventDefault();

    const holder = document.getElementById('withdraw-bank-holder').value.trim();
    const bankName = document.getElementById('withdraw-bank-name').value.trim();
    const accountNo = document.getElementById('withdraw-bank-account').value.trim();
    const ifsc = document.getElementById('withdraw-bank-ifsc').value.trim().toUpperCase();

    if (!holder || !bankName || !accountNo || !ifsc) {
      alert('All fields are required.');
      return;
    }

    if (!/^\d{9,20}$/.test(accountNo)) {
      alert('Account number must be between 9 and 20 digits containing only digits.');
      return;
    }

    if (!/^[A-Z0-9]{11}$/.test(ifsc)) {
      alert('IFSC code must be precisely 11 alphanumeric characters.');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/wallet/withdraw/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${STATE.currentUser.token}`
        },
        body: JSON.stringify({
          account_number: accountNo,
          account_holder_name: holder,
          bank_name: bankName,
          ifsc_code: ifsc
        })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Unable to withdraw wallet funds.');
      }

      this.closeBankModal();

      STATE.currentUser.wallet_balance = Number(data.wallet_balance);
      localStorage.setItem('inkify_user', JSON.stringify(STATE.currentUser));
      authManager.updateHeaderUI();

      // Show success dialog
      await showCustomDialog({
        icon: '<i class="fa-solid fa-circle-check" style="color: var(--accent-light);"></i>',
        title: 'Withdrawal Initiated',
        message: 'Within 2 days money will be deposited to your bank account.',
        actions: [{ label: 'OK', value: 'ok', type: 'primary' }]
      });

      this.renderModal();
      ordersManager.renderOrders();
    } catch (err) {
      alert(`Wallet withdraw error: ${err.message}`);
    }
  }
};

const paymentGatewayManager = {
  openGateway(amount) {
    const gatewayModal = document.getElementById('payment-gateway-modal-overlay');
    if (!gatewayModal) return;

    document.getElementById('gateway-total-amount').textContent = amount;
    document.getElementById('gateway-tab-upi').classList.remove('active');
    document.getElementById('gateway-tab-card').classList.remove('active');
    document.getElementById('gateway-panel-upi').style.display = 'none';
    document.getElementById('gateway-panel-card').style.display = 'none';

    // Activate correct tab based on current payment mode
    if (STATE.activePaymentMode === 'upi') {
      document.getElementById('gateway-tab-upi').classList.add('active');
      document.getElementById('gateway-panel-upi').style.display = 'block';
    } else {
      document.getElementById('gateway-tab-card').classList.add('active');
      document.getElementById('gateway-panel-card').style.display = 'block';
    }

    // Reset fields
    document.getElementById('gateway-upi-id').value = '';
    document.getElementById('gateway-card-number').value = '';
    document.getElementById('gateway-card-name').value = '';
    document.getElementById('gateway-card-expiry').value = '';
    document.getElementById('gateway-card-cvv').value = '';

    // Reset loading/success view
    document.getElementById('gateway-processing-view').style.display = 'none';
    document.getElementById('gateway-success-view').style.display = 'none';
    document.getElementById('gateway-main-view').style.display = 'block';

    gatewayModal.classList.add('active');
  },

  closeGateway() {
    const gatewayModal = document.getElementById('payment-gateway-modal-overlay');
    if (gatewayModal) gatewayModal.classList.remove('active');
  },

  switchTab(mode) {
    document.getElementById('gateway-tab-upi').classList.remove('active');
    document.getElementById('gateway-tab-card').classList.remove('active');
    document.getElementById('gateway-panel-upi').style.display = 'none';
    document.getElementById('gateway-panel-card').style.display = 'none';

    if (mode === 'upi') {
      document.getElementById('gateway-tab-upi').classList.add('active');
      document.getElementById('gateway-panel-upi').style.display = 'block';
      STATE.activePaymentMode = 'upi';
    } else {
      document.getElementById('gateway-tab-card').classList.add('active');
      document.getElementById('gateway-panel-card').style.display = 'block';
      STATE.activePaymentMode = 'card';
    }
    cartManager.selectPayment(STATE.activePaymentMode);
  },

  async handlePaymentSubmit() {
    // Validate fields based on mode
    if (STATE.activePaymentMode === 'upi') {
      const upiId = document.getElementById('gateway-upi-id').value.trim();
      if (!upiId || !upiId.includes('@')) {
        alert("Please enter a valid UPI ID (e.g. name@upi)");
        return;
      }
    } else {
      const cardNo = document.getElementById('gateway-card-number').value.replace(/\s+/g, '');
      const cardName = document.getElementById('gateway-card-name').value.trim();
      const cardExp = document.getElementById('gateway-card-expiry').value.trim();
      const cardCvv = document.getElementById('gateway-card-cvv').value.trim();

      if (cardNo.length < 15 || cardNo.length > 19 || isNaN(cardNo)) {
        alert("Please enter a valid Card Number (15 to 19 digits)");
        return;
      }
      if (!cardName) {
        alert("Please enter Cardholder Name");
        return;
      }
      if (!cardExp || !cardExp.includes('/') || cardExp.length !== 5) {
        alert("Please enter expiry in MM/YY format");
        return;
      }
      if (cardCvv.length < 3 || cardCvv.length > 4 || isNaN(cardCvv)) {
        alert("Please enter a valid CVV (3 or 4 digits)");
        return;
      }
    }

    // Switch to processing view
    document.getElementById('gateway-main-view').style.display = 'none';
    document.getElementById('gateway-processing-view').style.display = 'flex';

    // Simulate 2-second processing
    setTimeout(() => {
      // Switch to success view
      document.getElementById('gateway-processing-view').style.display = 'none';
      document.getElementById('gateway-success-view').style.display = 'flex';

      // Wait 1.5 seconds and call placeOrderConfirm
      setTimeout(async () => {
        this.closeGateway();
        await cartManager.placeOrderConfirm();
      }, 1500);
    }, 2000);
  }
};

// --- 6.5. ORDER LIST MANAGER ---
const ordersManager = {
  init() {
    // Optional initialization
  },

  navigateToOrders() {
    appRouter.navigate('orders');
  },

  async renderOrders() {
    const container = document.getElementById('orders-list-container');
    if (!container) return;

    if (!STATE.currentUser) {
      container.innerHTML = `
        <div class="order-card-empty">
          <i class="fa-solid fa-info-circle"></i>
          <h3>Guest Order History</h3>
          <p>Order history is available for registered users. Guests can still place orders and track them using your tracking ID.</p>
          <p style="margin-top: 12px; color: var(--text-secondary);">Use the tracking section to check order status after purchase.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
        <i class="fa-solid fa-spinner fa-spin" style="font-size: 2rem; color: var(--accent-light); margin-bottom: 15px; display: block;"></i>
        Fetching your customized blueprints...
      </div>
    `;

    try {
      const response = await fetch(`${API_BASE_URL}/orders/my/`, {
        headers: {
          'Authorization': `Token ${STATE.currentUser.token}`
        }
      });

      if (!response.ok) {
        throw new Error("Failed to load orders");
      }

      const orders = await response.json();

      const withdrawActionHtml = Number(STATE.currentUser.wallet_balance || 0) >= 500
        ? `<button class="btn-primary" style="margin-top: 14px;" onclick="walletManager.requestWithdraw()">Withdraw Available Wallet Funds</button>`
        : `<p style="margin-top: 14px; color: var(--text-secondary); font-size: 0.92rem;">Withdraw becomes available once your wallet balance reaches ₹500. You can also use wallet credit during checkout on your next order.</p>`;

      const accountSummaryHtml = `
        <div class="glass-panel" style="padding: 22px 24px; margin-bottom: 24px; border: 1px solid rgba(255,255,255,0.08);">
          <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px;">
            <div>
              <span style="display:block; color: var(--text-secondary); font-size:0.85rem; letter-spacing:0.06em;">Your Wallet Balance</span>
              <h3 style="margin:8px 0 0; font-size:1.6rem; color: var(--accent-light);">₹${Number(STATE.currentUser.wallet_balance || 0).toFixed(2)}</h3>
            </div>
            <div>
              <span style="display:block; color: var(--text-secondary); font-size:0.85rem; letter-spacing:0.06em;">Your Referral Code</span>
              <h3 style="margin:8px 0 0; font-size:1.6rem; color: var(--accent-light);">${STATE.currentUser.referral_code || 'Will be created after your first order'}</h3>
            </div>
          </div>
          ${withdrawActionHtml}
          <p style="margin-top: 14px; color: var(--text-secondary); font-size: 0.92rem;">Share your referral code with friends. When they buy the Purple Gift Set using your code, they get ₹50 off plus ₹50 in wallet, and you earn ₹50 into your wallet.</p>
        </div>
      `;
      container.innerHTML = accountSummaryHtml;

      if (orders.length === 0) {
        container.innerHTML = `
          <div class="order-card-empty">
            <i class="fa-solid fa-box-open"></i>
            <h3>No Custom Orders Yet</h3>
            <p>You haven't customized any premium canvases yet. Get started and build your vibe today!</p>
            <button class="btn-primary" onclick="appRouter.navigate('products')" style="margin: 0 auto;">Browse Canvas Products</button>
          </div>
        `;
        return;
      }

      container.innerHTML = accountSummaryHtml;

      orders.forEach(order => {
        let itemsHtml = '';
        order.items.forEach(item => {
          const customSpec = item.customization_type === 'photo'
            ? `<span>ðŸ“¸ Custom Photograph Printed</span><br><img src="${item.customization_data}" class="cart-item-custom-img" style="margin-top: 8px; width: 60px; height: 60px; border-radius: 6px; object-fit: cover;">`
            : `<span style="font-family: ${item.customization_font}; font-size: 0.95rem; font-weight: 700; color: white;">Printed: "${item.customization_data}"</span>`;

          itemsHtml += `
            <div class="tracking-summary-card" style="margin-top: 12px; background: rgba(255, 255, 255, 0.01); border-color: rgba(255, 255, 255, 0.03);">
              ${item.product_image.startsWith('<svg')
              ? `<div class="tracking-summary-img-svg" style="width: 50px; height: 50px; border-radius: 6px; overflow: hidden; border:1px solid rgba(255,255,255,0.05);">${item.product_image}</div>`
              : `<img src="${appRouter.getAssetUrl(item.product_image)}" alt="${item.product_name}" class="tracking-summary-img" style="width: 50px; height: 50px;">`
            }
              <div>
                <h5 style="font-weight: 600; font-size: 0.95rem; margin-bottom: 2px;">${item.product_name} (x${item.quantity})</h5>
                <div style="font-size: 0.75rem; color: var(--accent-light); margin-top: 4px;">
                  ${customSpec}
                </div>
              </div>
            </div>
          `;
        });

        let statusLabel = order.status;
        if (order.status === 'Placed') statusLabel = 'Order Placed';
        else if (order.status === 'Printing') statusLabel = 'Printing Blueprint';
        else if (order.status === 'Dispatched') statusLabel = 'Dispatched Cargo';
        else if (order.status === 'Delivery') statusLabel = 'Out for Delivery';

        const orderHtml = `
          <div class="order-card glass-panel" style="margin-bottom: 24px; padding: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 16px;">
              <div>
                <span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 4px;">Order Date</span>
                <span style="font-weight: 600; font-size: 0.95rem;">${new Date(order.created_at).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
              </div>
              <div>
                <span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 4px;">Tracking ID</span>
                <span style="font-weight: 700; font-size: 1.05rem; color: var(--accent-light);">${order.tracking_id}</span>
              </div>
              <div>
                <span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 4px;">Grand Total</span>
                <span style="font-weight: 700; font-size: 1.05rem;">₹${parseFloat(order.amount).toFixed(0)}</span>
              </div>
              <div>
                <span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; display: block; margin-bottom: 4px;">Status</span>
                <span class="step-label" style="display: inline-block; padding: 4px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; background: rgba(147, 51, 234, 0.15); color: var(--accent-light); border: 1px solid rgba(147, 51, 234, 0.3); text-shadow: 0 0 8px rgba(168, 85, 247, 0.4);">${statusLabel}</span>
              </div>
            </div>
            
            <div style="margin-top: 16px;">
              <h4 style="font-weight: 600; font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 10px;">Bespoke Blueprints</h4>
              ${itemsHtml}
            </div>
          </div>
        `;
        container.insertAdjacentHTML('beforeend', orderHtml);
      });
    } catch (err) {
      container.innerHTML = `
        <div class="order-card-empty">
          <i class="fa-solid fa-triangle-exclamation" style="color: var(--error);"></i>
          <h3>Failed to Load Orders</h3>
          <p>${err.message}</p>
          <button class="btn-primary" onclick="ordersManager.renderOrders()" style="margin: 0 auto;">Retry</button>
        </div>
      `;
    }
  },

  async trackOrder(trackingId) {
    try {
      const response = await fetch(`${API_BASE_URL}/orders/track/${trackingId}/`);
      if (response.ok) {
        const data = await response.json();
        const frontOrder = {
          trackingId: data.tracking_id,
          paymentMode: data.payment_mode,
          estDelivery: data.est_delivery,
          status: data.status,
          items: data.items.map(item => ({
            product: {
              id: item.product_id,
              name: item.product_name,
              image: item.product_image
            },
            quantity: item.quantity,
            customization: {
              type: item.customization_type,
              data: item.customization_data,
              font: item.customization_font,
              color: item.customization_color,
              summary: item.customization_summary
            }
          }))
        };
        trackingManager.renderDashboard(frontOrder);
        appRouter.navigate('tracking');
      }
    } catch (err) {
      alert("Error tracking order: " + err.message);
    }
  },

  directTrackFromSuccess() {
    this.trackOrder(document.getElementById('success-tracking-id-text').textContent);
  }
};

// --- 7. NOTIFICATION EMAIL TRIGGER SIMULATOR (DEV VIEW) ---
const emailSimulator = {
  unreadCount: 0,

  init() {
    // Load existing messages
    const savedLogs = localStorage.getItem('inkify_emails');
    if (savedLogs) {
      STATE.systemEmails = JSON.parse(savedLogs);
      this.renderInbox();
    }
  },

  toggleInbox() {
    const panel = document.getElementById('dev-inbox-panel');
    panel.classList.toggle('active');

    if (panel.classList.contains('active')) {
      this.unreadCount = 0;
      this.updateTriggerBadge();
    }
  },

  clearLogs() {
    STATE.systemEmails = [];
    localStorage.removeItem('inkify_emails');
    this.renderInbox();
    this.unreadCount = 0;
    this.updateTriggerBadge();
  },

  updateTriggerBadge() {
    const badge = document.getElementById('dev-inbox-badge-count');
    if (this.unreadCount > 0) {
      badge.textContent = this.unreadCount;
      badge.style.display = 'flex';
    } else {
      badge.style.display = 'none';
    }
  },

  triggerEmails(order) {
    const timestamp = new Date().toLocaleTimeString();

    // --- 1. CUSTOMER RECEIPT EMAIL ---
    let itemsRows = '';
    order.items.forEach(item => {
      const price = item.product.id === 5 ? item.product.cartPrice : item.product.price;
      itemsRows += `
        <tr>
          <td style="padding: 4px 0;"><strong>${item.product.name}</strong> x${item.quantity}</td>
          <td style="text-align: right;">₹${price * item.quantity}</td>
        </tr>
      `;
    });

    const customerEmail = {
      id: `email-cust-${Date.now()}`,
      type: 'customer',
      title: `Order Confirmed - Receipt #${order.trackingId}`,
      timestamp: timestamp,
      content: `
        <div>
          <p>Hi <strong>${order.customer.name}</strong>,</p>
          <p>Thank you for choosing <strong>Inkify Creations</strong>! We've locked in your custom printing blueprints and queued them into our print warehouse.</p>
          
          <table style="width:100%; border-collapse: collapse; font-size: 0.8rem; margin: 12px 0; border-top: 1px dashed rgba(255,255,255,0.1); border-bottom: 1px dashed rgba(255,255,255,0.1); padding: 8px 0;">
            <thead>
              <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--accent-light);">
                <th style="text-align: left; padding-bottom: 6px;">Product Specs</th>
                <th style="text-align: right; padding-bottom: 6px;">Subtotal</th>
              </tr>
            </thead>
            <tbody>
              ${itemsRows}
            </tbody>
          </table>
          
          <div style="display:flex; justify-content: space-between; font-weight:700; margin-bottom: 12px;">
            <span>Grand Total Paid:</span>
            <span style="color:var(--accent-light);">₹${order.amount}</span>
          </div>
          
          <p>ðŸšš Your shipping address is: <strong>${order.customer.address}</strong>.</p>
          <p>You can track your order printing blueprint using reference: <strong style="color:var(--accent-glow); font-family:var(--font-display);">${order.trackingId}</strong>.</p>
        </div>
      `
    };

    // --- 2. SELLER PRODUCTION TICKETS ---
    let blueprintsHtml = '';
    order.items.forEach((item, index) => {
      const colorSpecHtml = item.customization.color
        ? `<div style="margin-top: 6px; font-size: 0.8rem; color: var(--text-secondary);"><i class="fa-solid fa-palette" style="color: var(--accent-light); margin-right: 4px;"></i> Fabric Color Selected: <strong>${item.customization.color}</strong></div>`
        : '';
      const blueprintSpec = item.customization.type === 'photo'
        ? `
          <div style="margin-top: 8px;">
            <span style="color:var(--accent-light); font-weight:600;">Custom Photo Uploaded:</span><br>
            <img src="${item.customization.data}" style="width: 80px; height: 80px; object-fit:cover; border-radius: 6px; border: 1px solid var(--accent-purple); margin-top:4px;">
            ${colorSpecHtml}
          </div>
        `
        : `
          <div style="margin-top: 8px;">
            <span style="color:var(--accent-light); font-weight:600;">Custom Printed Text:</span><br>
            <span style="font-family: ${item.customization.font}; font-size: 1.1rem; font-weight: 700; background:rgba(0,0,0,0.3); padding:4px 8px; border-radius:4px; display:inline-block; margin-top:4px;">"${item.customization.data}"</span>
            ${colorSpecHtml}
          </div>
        `;

      blueprintsHtml += `
        <div style="background:rgba(255,255,255,0.02); padding:10px; border-radius:8px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.04);">
          <strong>Item #${index + 1}: ${item.product.name} (Quantity: ${item.quantity})</strong>
          ${blueprintSpec}
        </div>
      `;
    });

    let referrerLedgerHtml = '';
    if (order.referralApplied) {
      referrerLedralHtml = `
        <div class="email-log-payout-box">
          ðŸ’° REFERRAL LEDGER DETECTED!<br>
          Code: <strong>${order.referralApplied.code}</strong><br>
          Credit <strong>₹${order.referralApplied.payoutAmount}</strong> Cash Back to partner <strong>${order.referralApplied.referrer}</strong> on delivery!
        </div>
      `;
    }

    const sellerEmail = {
      id: `email-sell-${Date.now()}`,
      type: 'seller',
      title: `âš¡ Production Ticket - Order #${order.trackingId}`,
      timestamp: timestamp,
      content: `
        <div>
          <p><strong>Inkify Factory Alert!</strong> New production blueprint locked in.</p>
          <p><strong>Customer Name:</strong> ${order.customer.name} (Contact: +91-${order.customer.phone})</p>
          <p><strong>Shipping Warehouse Destination:</strong> ${order.customer.address}</p>
          
          <h5 style="margin-top:14px; margin-bottom:8px; font-weight:700; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom:4px;">Bespoke Blueprint Specs:</h5>
          ${blueprintsHtml}
          
          ${referrerLedgerHtml ? referrerLedgerHtml : ''}
          
          <p style="margin-top:14px; font-size:0.75rem; color:var(--text-muted);">Please route this print blueprint ticket to the DTF/Sublimation printing conveyor instantly.</p>
        </div>
      `
    };

    // Save to logs
    STATE.systemEmails.unshift(sellerEmail, customerEmail); // newest first
    localStorage.setItem('inkify_emails', JSON.stringify(STATE.systemEmails));

    // Update Badge
    this.unreadCount += 2;
    this.updateTriggerBadge();
    this.renderInbox();

    // Simulate active timeline stepper updates
    this.simulateLogisticsPipeline(order.trackingId);
  },

  simulateLogisticsPipeline(trackingId) {
    // Automatically advance order tracking states in localDB to make the web app feel alive!
    // Placed -> (30s) -> Printing -> (60s) -> Dispatched -> (90s) -> Delivery
    setTimeout(() => this.updateOrderStatus(trackingId, 'Printing'), 15000);
    setTimeout(() => this.updateOrderStatus(trackingId, 'Dispatched'), 35000);
    setTimeout(() => this.updateOrderStatus(trackingId, 'Delivery'), 60000);
  },

  updateOrderStatus(trackingId, nextStatus) {
    const savedOrders = localStorage.getItem('inkify_orders') ? JSON.parse(localStorage.getItem('inkify_orders')) : [];
    const orderIndex = savedOrders.findIndex(o => o.trackingId === trackingId);

    if (orderIndex !== -1) {
      savedOrders[orderIndex].status = nextStatus;
      localStorage.setItem('inkify_orders', JSON.stringify(savedOrders));

      // Generate email logs for logistics updates!
      const timestamp = new Date().toLocaleTimeString();
      const statusTitle = nextStatus === 'Printing' ? 'Custom Printing Initiated' : nextStatus === 'Dispatched' ? 'Order Dispatched' : 'Out for Delivery';
      const statusDesc = nextStatus === 'Printing' ? 'Our designers have loaded your bespoke photo/text templates into the conveyor.' : nextStatus === 'Dispatched' ? 'Your package is on its way via Express Cargo.' : 'Our courier partner is arriving at your doorstep today!';

      const updateEmail = {
        id: `email-update-${Date.now()}`,
        type: 'customer',
        title: `ðŸšš Shipping Alert: ${statusTitle} - #${trackingId}`,
        timestamp: timestamp,
        content: `
          <div>
            <p>Hi <strong>${savedOrders[orderIndex].customer.name}</strong>,</p>
            <p>Great news! Your customized printed gear has transitioned to stage: <strong>${nextStatus}</strong>.</p>
            <p>${statusDesc}</p>
            <p>Live track your parcel using Reference ID: <strong style="color:var(--accent-glow);">${trackingId}</strong>.</p>
          </div>
        `
      };

      STATE.systemEmails.unshift(updateEmail);
      localStorage.setItem('inkify_emails', JSON.stringify(STATE.systemEmails));

      this.unreadCount += 1;
      this.updateTriggerBadge();
      this.renderInbox();

      // If user is currently viewing this tracking screen, re-render it instantly!
      if (appRouter.activeView === 'tracking') {
        const inputId = document.getElementById('tracking-input-id').value.trim();
        if (inputId.toUpperCase() === trackingId.toUpperCase()) {
          trackingManager.renderDashboard(savedOrders[orderIndex]);
        }
      }
    }
  },

  renderInbox() {
    const container = document.getElementById('dev-inbox-logs-container');
    container.innerHTML = '';

    if (STATE.systemEmails.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; color: var(--text-muted); font-size: 0.8rem; margin: auto 0; padding: 20px;">
          <i class="fa-solid fa-circle-info" style="font-size: 1.5rem; color: var(--accent-dark); margin-bottom: 10px; display: block;"></i>
          Developer Debug System Ready.<br>Place an order to trigger the customer invoice receipt and the seller's blueprint production email ticket!
        </div>
      `;
      return;
    }

    STATE.systemEmails.forEach(email => {
      const typeClass = email.type === 'seller' ? 'seller-ticket' : 'customer-receipt';
      const typeLabel = email.type === 'seller' ? 'Seller production Ticket' : 'Customer Email Receipt';

      const logHtml = `
        <div class="email-log-item ${typeClass}">
          <span class="email-log-tag">${typeLabel}</span>
          <div class="email-log-title">${email.title}</div>
          <div class="email-log-meta"><i class="fa-regular fa-clock"></i> Timestamp: ${email.timestamp}</div>
          <div class="email-log-content">
            ${email.content}
          </div>
        </div>
      `;
      container.insertAdjacentHTML('beforeend', logHtml);
    });
  }
};

// --- INITIALIZE APPLICATION ON LOAD ---
/* =========================================================
   TRENDING POPUP CONTROLLER
   ========================================================= */
const trendingPopup = {
  overlay: null,
  hasShown: false,

  init() {
    this.overlay = document.getElementById('trending-popup-overlay');
    // Safety: always clear any stale scroll lock from previous state
    this._resetBodyScroll();
    if (!this.overlay) return;

    // Show every time on page load / reload
    this._fetchAndRender().then(() => {
      setTimeout(() => this.open(), 600);
    });
  },

  open() {
    if (!this.overlay) return;
    this.overlay.classList.add('active');
    document.body.classList.add('no-scroll');
    this.hasShown = true;
  },

  close() {
    // Always reset scroll even if overlay ref is stale
    this._resetBodyScroll();
    if (this.overlay) this.overlay.classList.remove('active');
  },

  _resetBodyScroll() {
    document.body.classList.remove('no-scroll');
  },

  async _fetchAndRender() {
    const grid = document.getElementById('trending-products-grid');
    if (!grid) return;

    try {
      const res = await fetch('/api/trending-products/');
      if (!res.ok) throw new Error('API error');
      const products = await res.json();

      if (!products || products.length === 0) {
        grid.innerHTML = `
          <div style="grid-column:1/-1;text-align:center;padding:40px 0;">
            <i class="fa-solid fa-fire" style="font-size:2.5rem;color:var(--accent-purple);display:block;margin-bottom:12px;"></i>
            <p style="color:var(--text-secondary);font-size:1rem;">No trending products right now. Check back soon!</p>
          </div>`;
        return;
      }

      grid.innerHTML = products.map(p => {
        const imgSrc = p.trending_image_url || p.image || '';
        const tagline = p.trending_tagline || p.description || 'Premium quality, made to order.';
        const price = p.price ? `₹${parseFloat(p.price).toFixed(2)}` : '';
        return `
          <div class="trending-card" onclick="trendingPopup._onCardClick(${p.id})" title="Customize ${p.name}">
            <span class="trending-badge"><i class="fa-solid fa-fire" style="margin-right:4px;"></i>Trending</span>
            <div class="trending-img-container">
              ${imgSrc
                ? `<img class="trending-img" src="${imgSrc}" alt="${p.name}" loading="lazy" onerror="this.parentElement.innerHTML='<i class=\\'fa-solid fa-image\\' style=\\'font-size:3rem;color:rgba(255,255,255,0.1)\\'></i>'">`
                : `<i class="fa-solid fa-image" style="font-size:3rem;color:rgba(255,255,255,0.1);"></i>`}
            </div>
            <div class="trending-name">${p.name}</div>
            <div class="trending-tagline">${tagline}</div>
            ${price ? `<div style="font-size:1rem;font-weight:800;color:var(--accent-light);margin-bottom:14px;">${price}</div>` : ''}
            <button class="trending-action-btn" onclick="event.stopPropagation();trendingPopup._onCardClick(${p.id})">
              <i class="fa-solid fa-wand-magic-sparkles"></i> Customize Now
            </button>
          </div>`;
      }).join('');

    } catch (err) {
      grid.innerHTML = `
        <div style="grid-column:1/-1;text-align:center;padding:40px 0;">
          <i class="fa-solid fa-triangle-exclamation" style="font-size:2rem;color:var(--error);display:block;margin-bottom:12px;"></i>
          <p style="color:var(--text-secondary);">Couldn't load trending products. Please try again later.</p>
        </div>`;
      console.warn('[TrendingPopup] Fetch error:', err);
    }
  },

  _onCardClick(productId) {
    this.close();
    // Navigate to the products page, optionally highlight / pre-select the product
    setTimeout(() => {
      appRouter.navigate('products');
      // Give the products page a moment to render then scroll to the selected product card
      setTimeout(() => {
        const card = document.querySelector(`[data-product-id="${productId}"]`);
        if (card) {
          card.scrollIntoView({ behavior: 'smooth', block: 'center' });
          card.classList.add('product-highlight');
          setTimeout(() => card.classList.remove('product-highlight'), 2000);
        }
      }, 600);
    }, 350);
  }
};

const reviewsController = {
  productId: null,
  avgRating: 0.0,
  totalCount: 0,
  distribution: {},
  reviews: [],
  currentFilters: {
    star: null,
    verified: false,
    sort: 'most_recent'
  },
  writeRating: 5,
  writeImageFile: null,

  async loadReviews(productId) {
    this.productId = productId;
    this.currentFilters = {
      star: null,
      verified: false,
      sort: 'most_recent'
    };
    
    // Reset inputs
    const verifiedFilter = document.getElementById('review-verified-filter');
    if (verifiedFilter) verifiedFilter.checked = false;
    const sortSelect = document.getElementById('review-sort-select');
    if (sortSelect) sortSelect.value = 'most_recent';

    await this.fetchAndRender();
  },

  async fetchAndRender() {
    if (!this.productId) return;
    
    try {
      let url = `/api/products/${this.productId}/reviews/?sort=${this.currentFilters.sort}`;
      if (this.currentFilters.verified) {
        url += '&verified=true';
      }
      if (this.currentFilters.star) {
        url += `&rating=${this.currentFilters.star}`;
      }

      const headers = {};
      if (STATE.currentUser && STATE.currentUser.token) {
        headers['Authorization'] = `Token ${STATE.currentUser.token}`;
      }

      const res = await fetch(url, { headers });
      if (!res.ok) throw new Error("Failed to load reviews");
      
      const data = await res.json();
      this.avgRating = data.average_rating || 0.0;
      this.totalCount = data.total || 0;
      this.distribution = data.distribution || {};
      this.reviews = data.reviews || [];

      this.renderDashboard();
      this.renderFilterBadges();
      this.renderReviewsList();
    } catch (e) {
      console.error(e);
    }
  },

  renderDashboard() {
    // 1. Avg rating
    const avgRatingText = document.getElementById('reviews-avg-rating');
    if (avgRatingText) avgRatingText.textContent = Number(this.avgRating).toFixed(1);

    // 2. Avg stars
    const avgStarsContainer = document.getElementById('reviews-avg-stars');
    if (avgStarsContainer) {
      avgStarsContainer.innerHTML = this.getStarsHtml(this.avgRating);
    }

    // 3. Total count
    const totalCountText = document.getElementById('reviews-total-count');
    if (totalCountText) {
      totalCountText.textContent = `${this.totalCount} ratings`;
    }

    // 4. Progress bars distribution
    for (let star = 1; star <= 5; star++) {
      const distData = this.distribution[String(star)] || { count: 0, percent: 0 };
      const fillBar = document.getElementById(`dist-fill-${star}`);
      const percentText = document.getElementById(`dist-percent-${star}`);
      const row = document.getElementById(`dist-row-${star}`);
      
      if (fillBar) fillBar.style.width = `${distData.percent}%`;
      if (percentText) percentText.textContent = `${Math.round(distData.percent)}%`;
      
      // Toggle active class on rows
      if (row) {
        if (this.currentFilters.star === star) {
          row.classList.add('active');
        } else {
          row.classList.remove('active');
        }
      }
    }
  },

  renderFilterBadges() {
    const container = document.getElementById('reviews-active-filters');
    if (!container) return;
    
    container.innerHTML = '';
    if (this.currentFilters.star) {
      const badge = document.createElement('div');
      badge.className = 'review-filter-badge';
      badge.innerHTML = `
        <span>Rating: ${this.currentFilters.star} Star</span>
        <i class="fa-solid fa-xmark" onclick="reviewsController.toggleStarFilter(${this.currentFilters.star})"></i>
      `;
      container.appendChild(badge);
    }
  },

  renderReviewsList() {
    const container = document.getElementById('product-reviews-list');
    if (!container) return;

    if (this.reviews.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 40px 0; color: var(--text-secondary);">
          <i class="fa-solid fa-comments" style="font-size: 2.5rem; display: block; margin-bottom: 12px; opacity: 0.4;"></i>
          <p>No reviews matching selected filters.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = this.reviews.map(review => {
      const formattedDate = new Date(review.created_at).toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      });

      const userDisplay = review.username ? `${review.username} (${review.user_mobile})` : review.user_mobile;
      const avatarLetter = (review.username || review.user_mobile || 'U')[0].toUpperCase();

      return `
        <div class="review-card">
          <div class="review-card-header">
            <div class="review-user-info">
              <div class="review-user-avatar">${avatarLetter}</div>
              <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span class="review-user-name">${userDisplay}</span>
                  ${review.is_verified ? `
                    <span class="review-verified-badge" title="Verified Buyer">
                      <i class="fa-solid fa-circle-check"></i> Verified Purchase
                    </span>
                  ` : ''}
                </div>
                <span class="review-meta-date">Reviewed on ${formattedDate}</span>
              </div>
            </div>
            
            <div class="review-card-rating">
              ${this.getStarsHtml(review.rating)}
            </div>
          </div>
          
          <div class="review-card-body">
            <h4 class="review-card-title">${review.title}</h4>
            <p class="review-card-comment">${review.comment}</p>
            ${review.image_url ? `
              <div class="review-card-image">
                <img src="${review.image_url}" alt="Review photo" onclick="appRouter.showGlobalImagePreview('${review.image_url}', '${review.title}')">
              </div>
            ` : ''}
          </div>
          
          <div class="review-card-footer">
            <span>Was this review helpful?</span>
            <button class="btn-review-helpful ${review.has_marked_helpful ? 'active' : ''}" onclick="reviewsController.toggleHelpful(${review.id})">
              <i class="fa-regular fa-thumbs-up"></i> Helpful (${review.helpful_count || 0})
            </button>
          </div>
        </div>
      `;
    }).join('');
  },

  getStarsHtml(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStar;
    
    let html = '';
    for (let i = 0; i < fullStars; i++) {
      html += '<i class="fa-solid fa-star"></i>';
    }
    if (halfStar) {
      html += '<i class="fa-solid fa-star-half-stroke"></i>';
    }
    for (let i = 0; i < emptyStars; i++) {
      html += '<i class="fa-regular fa-star"></i>';
    }
    return html;
  },

  toggleStarFilter(star) {
    if (this.currentFilters.star === star) {
      this.currentFilters.star = null;
    } else {
      this.currentFilters.star = star;
    }
    this.fetchAndRender();
  },

  toggleVerifiedFilter() {
    const checkbox = document.getElementById('review-verified-filter');
    this.currentFilters.verified = checkbox ? checkbox.checked : false;
    this.fetchAndRender();
  },

  changeSort() {
    const select = document.getElementById('review-sort-select');
    this.currentFilters.sort = select ? select.value : 'most_recent';
    this.fetchAndRender();
  },

  async toggleHelpful(reviewId) {
    if (!STATE.currentUser) {
      customAlert("Please sign in to vote a review as helpful.", "Authentication Required");
      return;
    }

    try {
      const res = await fetch(`/api/reviews/${reviewId}/helpful/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${STATE.currentUser.token}`
        }
      });
      if (res.ok) {
        // Toggle client-side state of that specific review in our list
        const review = this.reviews.find(r => r.id === reviewId);
        if (review) {
          const data = await res.json();
          review.helpful_count = data.helpful_count;
          review.has_marked_helpful = data.has_marked_helpful;
          this.renderReviewsList();
        }
      }
    } catch (e) {
      console.error(e);
    }
  },

  openWriteModal() {
    if (!STATE.currentUser) {
      customAlert("Please sign in to write a review.", "Authentication Required");
      return;
    }

    // Reset form fields
    const form = document.getElementById('write-review-form');
    if (form) form.reset();
    
    this.writeRating = 5;
    this.setWriteRating(5);
    this.clearWriteImage();
    
    const statusText = document.getElementById('write-review-status');
    if (statusText) statusText.textContent = '';

    document.getElementById('write-review-modal-overlay').classList.add('active');
  },

  closeWriteModal() {
    document.getElementById('write-review-modal-overlay').classList.remove('active');
  },

  setWriteRating(rating) {
    this.writeRating = rating;
    const ratingInput = document.getElementById('write-review-rating-val');
    if (ratingInput) ratingInput.value = rating;

    const stars = document.querySelectorAll('#review-stars-select i');
    stars.forEach(star => {
      const r = parseInt(star.getAttribute('data-rating'));
      if (r <= rating) {
        star.classList.add('selected');
      } else {
        star.classList.remove('selected');
      }
    });
  },

  handleWriteImageSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      customAlert("File size must be less than 5MB.", "File Too Large");
      return;
    }

    this.writeImageFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
      const previewContainer = document.getElementById('write-review-image-preview-container');
      const previewImg = document.getElementById('write-review-image-preview-img');
      const nameText = document.getElementById('write-review-image-name');
      
      if (previewContainer) previewContainer.style.display = 'flex';
      if (previewImg) previewImg.src = e.target.result;
      if (nameText) nameText.textContent = file.name;
    };
    reader.readAsDataURL(file);
  },

  clearWriteImage(event) {
    if (event) event.stopPropagation();
    this.writeImageFile = null;
    const input = document.getElementById('write-review-image-input');
    if (input) input.value = '';
    const previewContainer = document.getElementById('write-review-image-preview-container');
    if (previewContainer) previewContainer.style.display = 'none';
  },

  async submitReview(event) {
    event.preventDefault();
    if (!this.productId) return;

    const title = document.getElementById('write-review-title').value.trim();
    const comment = document.getElementById('write-review-comment').value.trim();
    const rating = this.writeRating;
    const statusText = document.getElementById('write-review-status');

    if (!title || !comment || !rating) {
      if (statusText) statusText.textContent = "Please fill in all required fields.";
      return;
    }

    try {
      const formData = new FormData();
      formData.append('rating', rating);
      formData.append('title', title);
      formData.append('comment', comment);
      if (this.writeImageFile) {
        formData.append('image', this.writeImageFile);
      }

      if (statusText) statusText.textContent = "Submitting review...";

      const res = await fetch(`/api/products/${this.productId}/reviews/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${STATE.currentUser.token}`
        },
        body: formData
      });

      if (res.ok) {
        this.closeWriteModal();
        customAlert("Your review has been submitted successfully!", "Review Submitted");
        
        // Refresh reviews list
        await this.fetchAndRender();
      } else {
        const errorData = await res.json();
        if (statusText) statusText.textContent = errorData.error || "Failed to submit review.";
      }
    } catch (e) {
      console.error(e);
      if (statusText) statusText.textContent = "An error occurred. Please try again.";
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  appRouter.init();
  carousel.init();
  authManager.init();
  productCatalog.init();
  cartManager.init();
  ordersManager.init();
  trendingPopup.init();
  trackingManager.searchOrder = trackingManager.searchOrder.bind(trackingManager);

  // Global click event listener for previewing content images
  document.addEventListener('click', (event) => {
    const target = event.target.closest('img');
    if (!target) return;

    // Ignore decorative, UI elements or images that shouldn't be previewed
    if (
      target.closest('.logo') ||
      target.closest('.social-icons') ||
      target.closest('.payment-options') ||
      target.closest('.dev-inbox-trigger') ||
      target.closest('.modal-close-btn') ||
      target.closest('.design-preview-close') ||
      target.closest('.success-icon-badge') ||
      target.closest('.slide-bg') ||
      target.id === 'dev-inbox-logs-container'
    ) {
      return;
    }

    // Stop propagation so that clicking the image does not trigger parent actions
    // (e.g. adding item to cart, opening configuration modals, etc.)
    event.preventDefault();
    event.stopPropagation();

    const src = target.src;
    let title = target.alt || '';
    let category = '';

    // Extrapolate rich context (title and category) based on image placement
    const productCard = target.closest('.product-card');
    if (productCard) {
      const nameEl = productCard.querySelector('.product-name');
      const catEl = productCard.querySelector('.product-category');
      if (nameEl) title = nameEl.textContent.trim();
      if (catEl) category = catEl.textContent.trim();
    }

    const dsCard = target.closest('.ds-card');
    if (dsCard) {
      const nameEl = dsCard.querySelector('.ds-card-name');
      const catEl = dsCard.querySelector('.ds-card-category');
      if (nameEl) title = nameEl.textContent.trim();
      if (catEl) category = catEl.textContent.trim();
    }

    const cartItem = target.closest('.cart-item-row') || target.closest('.cart-item') || target.closest('.cart-item-thumb') || target.closest('tr');
    if (cartItem) {
      const nameEl = cartItem.querySelector('.cart-item-name') || cartItem.querySelector('.product-name') || cartItem.querySelector('.cart-item-title') || cartItem.querySelector('h4');
      if (nameEl) title = nameEl.textContent.trim();
    }

    const trackingCard = target.closest('.tracking-summary-card');
    if (trackingCard) {
      const labelEl = trackingCard.querySelector('span') || trackingCard.querySelector('h4');
      if (labelEl) title = labelEl.textContent.trim();
    }

    appRouter.showGlobalImagePreview(src, title, category);
  });
});
