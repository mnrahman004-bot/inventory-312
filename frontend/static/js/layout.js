// Shared sidebar HTML
function getSidebar(activePage) {
  const navItems = [
    { href: '/dashboard', icon: '📊', label: 'Dashboard', section: null },
    { href: '/products', icon: '📦', label: 'Products', section: 'Inventory' },
    { href: '/inventory', icon: '🗄️', label: 'Stock Control', section: null },
    { href: '/sales', icon: '💳', label: 'Sales', section: 'Transactions' },
    { href: '/suppliers', icon: '🏭', label: 'Suppliers', section: null },
    { href: '/reports', icon: '📈', label: 'Reports', section: 'Analytics' },
    { href: '/predict', icon: '🤖', label: 'AI Prediction', section: null },
  ];

  let nav = '';
  let lastSection = null;
  navItems.forEach(item => {
    if (item.section && item.section !== lastSection) {
      nav += `<div class="nav-section">${item.section}</div>`;
      lastSection = item.section;
    }
    const active = activePage === item.href ? 'active' : '';
    nav += `<a href="${item.href}" class="nav-item ${active}">
      <span class="icon">${item.icon}</span>
      <span>${item.label}</span>
    </a>`;
  });

  return `
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-brand">
      <div class="brand-icon">📦</div>
      <div>
        <div class="brand-name">StockSense</div>
        <div class="brand-sub">IMS v1.0</div>
      </div>
    </div>
    <nav class="sidebar-nav">${nav}</nav>
    <div class="sidebar-footer">
      <button class="nav-item" onclick="logout()" style="color: var(--danger);">
        <span class="icon">🚪</span>
        <span>Logout</span>
      </button>
    </div>
  </aside>`;
}

function getTopbar(title) {
  return `
  <div class="topbar">
    <div style="display:flex;align-items:center;gap:12px;">
      <button class="menu-toggle" onclick="toggleSidebar()">☰</button>
      <div class="topbar-title">${title}</div>
    </div>
    <div class="topbar-right">
      <div class="user-badge">
        <div class="user-avatar">A</div>
        <span id="username-display">admin</span>
      </div>
    </div>
  </div>`;
}

function renderLayout(page, title, contentHtml) {
  document.body.innerHTML = getSidebar(page) + `
  <div class="main-content">
    ${getTopbar(title)}
    <div class="page-content">${contentHtml}</div>
  </div>`;
}
