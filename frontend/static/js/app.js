// ── API BASE URL ──────────────────────────────────────────────
const API = '/api';

// ── TOAST NOTIFICATIONS ───────────────────────────────────────
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type] || icons.info}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(60px)'; setTimeout(() => toast.remove(), 300); }, 3000);
}

// ── FETCH WRAPPER ─────────────────────────────────────────────
async function apiFetch(url, options = {}) {
  try {
    const res = await fetch(API + url, {
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      ...options
    });
    if (res.status === 401) {
      window.location.href = '/login';
      return null;
    }
    const data = await res.json();
    return { ok: res.ok, data, status: res.status };
  } catch (e) {
    showToast('Network error. Is the server running?', 'error');
    return null;
  }
}

// ── AUTH CHECK ────────────────────────────────────────────────
async function checkAuth() {
  const r = await apiFetch('/check-auth');
  if (!r || !r.ok) {
    window.location.href = '/login';
    return null;
  }
  // Set username in UI
  const el = document.getElementById('username-display');
  if (el) el.textContent = r.data.username;
  return r.data;
}

// ── LOGOUT ────────────────────────────────────────────────────
async function logout() {
  await apiFetch('/logout', { method: 'POST' });
  window.location.href = '/login';
}

// ── FORMAT CURRENCY ───────────────────────────────────────────
function formatCurrency(amount) {
  return '₹' + parseFloat(amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// ── FORMAT DATE ───────────────────────────────────────────────
function formatDate(dateStr) {
  if (!dateStr) return '-';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function formatDateTime(dateStr) {
  if (!dateStr) return '-';
  const d = new Date(dateStr);
  return d.toLocaleString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}

// ── SET ACTIVE NAV ────────────────────────────────────────────
function setActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(item => {
    const href = item.getAttribute('href') || '';
    if (href && path.startsWith(href)) {
      item.classList.add('active');
    }
  });
}

// ── MODAL HELPERS ─────────────────────────────────────────────
function openModal(id) { document.getElementById(id).classList.add('open'); }
function closeModal(id) { document.getElementById(id).classList.remove('open'); }

// Click outside to close
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('open');
  }
});

// ── TABLE SEARCH ──────────────────────────────────────────────
function filterTable(inputId, tableId) {
  const input = document.getElementById(inputId);
  const table = document.getElementById(tableId);
  if (!input || !table) return;
  input.addEventListener('input', () => {
    const val = input.value.toLowerCase();
    table.querySelectorAll('tbody tr').forEach(row => {
      row.style.display = row.textContent.toLowerCase().includes(val) ? '' : 'none';
    });
  });
}

// ── STOCK BADGE ───────────────────────────────────────────────
function stockBadge(qty, threshold) {
  if (qty <= 0) return `<span class="badge badge-danger">Out of Stock</span>`;
  if (qty <= threshold) return `<span class="badge badge-warning">⚠ Low: ${qty}</span>`;
  return `<span class="badge badge-success">${qty}</span>`;
}

// ── MOBILE SIDEBAR TOGGLE ─────────────────────────────────────
function toggleSidebar() {
  document.querySelector('.sidebar').classList.toggle('open');
}

// Init on load
document.addEventListener('DOMContentLoaded', () => {
  setActiveNav();
});
