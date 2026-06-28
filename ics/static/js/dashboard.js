/* ==============================================
   ICS — Inventory Control System
   dashboard.js · Interactive behaviours
   ============================================== */

'use strict';

// ── Helpers ───────────────────────────────────
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
const on = (el, ev, fn) => el && el.addEventListener(ev, fn);

// ── Nav & Routing ─────────────────────────────
function navigateTo(section) {
  // hide all pages
  $$('.page').forEach(p => p.classList.remove('active'));
  $$('.nav-item').forEach(n => n.classList.remove('active'));

  const page = $(`#page-${section}`);
  if (page) page.classList.add('active');

  const navItem = $(`.nav-item[data-section="${section}"]`);
  if (navItem) navItem.classList.add('active');

  const label = navItem ? navItem.querySelector('span')?.textContent || section : section;
  $('#breadcrumbLabel').textContent = label;

  document.body.dataset.section = section;

  // animate KPI counters on newly visible pages
  animateCounters(page);
}

$$('.nav-item').forEach(item => {
  on(item, 'click', e => {
    e.preventDefault();
    navigateTo(item.dataset.section);
  });
});

// card-link "view all" shortcuts
$$('[data-go]').forEach(link => {
  on(link, 'click', e => { e.preventDefault(); navigateTo(link.dataset.go); });
});

// ── Sidebar Toggle ────────────────────────────
on($('#sidebarToggle'), 'click', () => {
  document.body.classList.toggle('sidebar-collapsed');
});

// ── Role Switcher ─────────────────────────────
const roleSelect = $('#roleSelect');
const roleLabel  = $('#roleLabel');

on(roleSelect, 'change', () => {
  const role = roleSelect.value;
  document.body.dataset.role = role;
  roleLabel.textContent = role.charAt(0).toUpperCase() + role.slice(1);

  // Restrict nav for non-admin roles
  $$('.nav-item.admin-only').forEach(item => {
    item.style.display = (role === 'admin') ? '' : 'none';
  });

  // If on an admin-only page, redirect dealer/user to appropriate landing
  const current = document.body.dataset.section;
  const adminPages = ['users', 'dealers', 'settings'];
  const dealerPages = ['checkin', 'checkout', 'acknowledge'];
  const userPages = ['reports', 'products', 'inventory'];

  if (role === 'dealer' && adminPages.includes(current)) {
    navigateTo('checkin');
  } else if (role === 'user' && adminPages.includes(current)) {
    navigateTo('reports');
  }

  showToast(`Switched to ${role} view`, 'info');
});

// ── Search Bar ────────────────────────────────
const searchBar = $('#searchBar');
const searchInput = $('#globalSearch');

on($('#searchToggle'), 'click', () => {
  searchBar.classList.toggle('open');
  if (searchBar.classList.contains('open')) searchInput.focus();
});

on(searchInput, 'keydown', e => {
  if (e.key === 'Escape') searchBar.classList.remove('open');
});

// Live filter on requisition table
on(searchInput, 'input', () => {
  const q = searchInput.value.toLowerCase();
  $$('#reqTableBody tr').forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
});

// ── KPI Counter Animation ─────────────────────
function animateCounters(container = document) {
  $$('.kpi-value', container).forEach(el => {
    const target = parseInt(el.dataset.count, 10);
    if (isNaN(target) || el.dataset.animated === '1') return;
    el.dataset.animated = '1';
    let start = 0;
    const duration = 900;
    const step = performance.now();
    const tick = now => {
      const progress = Math.min((now - step) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(ease * target).toLocaleString();
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
}
// initial run on dashboard
animateCounters($('#page-dashboard'));

// ── Chart.js Stock Movement ───────────────────
function buildChart() {
  const ctx = $('#stockChart');
  if (!ctx || !window.Chart) return;

  const labels7 = ['22 Jun','23 Jun','24 Jun','25 Jun','26 Jun','27 Jun','28 Jun'];
  const labels30 = Array.from({length:30}, (_,i) => {
    const d = new Date(); d.setDate(d.getDate() - 29 + i);
    return d.toLocaleDateString('en-GB', {day:'2-digit', month:'short'});
  });

  const data7in  = [48,62,39,71,55,80,65];
  const data7out = [32,45,28,55,40,60,50];

  const rand = (n, base, spread) => Array.from({length:n}, () =>
    Math.max(0, Math.round(base + (Math.random() - .5) * spread)));

  const datasets = {
    '7d':  { labels: labels7,  inData: data7in,          outData: data7out },
    '30d': { labels: labels30, inData: rand(30,60,40),    outData: rand(30,45,30) },
    '90d': { labels: Array.from({length:90},(_,i)=>i+1), inData: rand(90,55,35), outData: rand(90,40,25) }
  };

  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: datasets['7d'].labels,
      datasets: [
        {
          label: 'Check-Ins',
          data: datasets['7d'].inData,
          borderColor: '#2563eb',
          backgroundColor: 'rgba(37,99,235,.08)',
          borderWidth: 2,
          pointRadius: 3,
          pointBackgroundColor: '#2563eb',
          tension: .4, fill: true,
        },
        {
          label: 'Check-Outs',
          data: datasets['7d'].outData,
          borderColor: '#16a34a',
          backgroundColor: 'rgba(22,163,74,.08)',
          borderWidth: 2,
          pointRadius: 3,
          pointBackgroundColor: '#16a34a',
          tension: .4, fill: true,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { position: 'top', labels: { boxWidth: 10, padding: 16, font: { size: 12, family: 'Inter' } } },
        tooltip: { mode: 'index', intersect: false }
      },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 11, family: 'Inter' }, maxRotation: 0 } },
        y: { grid: { color: '#f1f2f4' }, ticks: { font: { size: 11, family: 'Inter' } }, beginAtZero: true }
      }
    }
  });

  // Chart tab switching
  $$('.chart-tab').forEach(tab => {
    on(tab, 'click', () => {
      $$('.chart-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const range = tab.dataset.range;
      const d = datasets[range];
      chart.data.labels = d.labels;
      chart.data.datasets[0].data = d.inData;
      chart.data.datasets[1].data = d.outData;
      chart.update('active');
    });
  });
}

// Wait for Chart.js to load
if (window.Chart) buildChart();
else window.addEventListener('load', buildChart);

// ── Requisition Modal ─────────────────────────
const reqModal  = $('#reqModal');
const openReqBtn  = $('#newReqBtn');
const closeReqBtn = $('#closeReqModal');
const cancelReqBtn = $('#cancelReqModal');

on(openReqBtn, 'click', () => reqModal.classList.add('open'));
on(closeReqBtn, 'click', () => reqModal.classList.remove('open'));
on(cancelReqBtn, 'click', () => reqModal.classList.remove('open'));
on(reqModal, 'click', e => { if (e.target === reqModal) reqModal.classList.remove('open'); });

// Generic new requisition button on dashboard
const dashNewReqBtn = $('.page-actions .btn-primary', $('#page-dashboard'));
on(dashNewReqBtn, 'click', () => reqModal.classList.add('open'));

// ── Check-In Lookup Simulation ────────────────
on($('#checkinLookup'), 'click', () => {
  const code = ($('#checkinScan')?.value || '').trim();
  if (!code) return;
  const fakeDB = {
    'PCBA-001-A': 'PCBA Board — Type A',
    'SPR-003-C':  'Spare Pin Set — C3',
    'RAW-010-A':  'Raw Material — Grade A',
  };
  const match = fakeDB[code.toUpperCase()] || `Product (${code})`;
  const nameEl = $('#checkinProductName');
  if (nameEl) {
    nameEl.value = match;
    nameEl.style.border = '1px solid #16a34a';
    setTimeout(() => { nameEl.style.border = ''; }, 2000);
  }
  showToast(`Found: ${match}`, 'success');
});

// ── Check-In Submit ───────────────────────────
on($('#checkinSubmit'), 'click', () => {
  const name = $('#checkinProductName')?.value;
  const qty  = $('#checkinQty')?.value;
  if (!name || !qty) { showToast('Please fill in product and quantity', 'warn'); return; }
  showToast(`Check-in recorded: ${qty}× ${name}`, 'success');
});

// ── Acknowledge ───────────────────────────────
window.acknowledge = function(btn) {
  const row = btn.closest('tr');
  const delivId = row.cells[0].textContent.trim();
  btn.closest('td').innerHTML = `<span class="badge badge-success"><i class="fa-solid fa-check"></i> Done</span>`;
  row.cells[4].textContent = 'You';
  showToast(`${delivId} acknowledged`, 'success');
};

// ── Category Tabs (Products) ──────────────────
$$('.cat-tab').forEach(tab => {
  on(tab, 'click', () => {
    $$('.cat-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
  });
});

// ── Invoice Generate ──────────────────────────
on($('#genInvoiceBtn'), 'click', () => {
  showToast('Invoice INV-2026-032 generated', 'success');
});

// ── Footer Last Sync Clock ────────────────────
function updateSync() {
  const el = $('#lastSync');
  if (!el) return;
  const now = new Date();
  el.textContent = now.toLocaleTimeString('en-GB', {hour:'2-digit', minute:'2-digit', second:'2-digit'});
}
updateSync();
setInterval(updateSync, 5000);

// Random DB status flicker (demo)
setInterval(() => {
  $$('.db-item').forEach(item => {
    if (item.classList.contains('warn') && Math.random() > .7) {
      item.classList.toggle('online');
      item.classList.toggle('warn');
    }
  });
}, 8000);

// ── Toast Notifications ───────────────────────
let toastContainer = null;

function showToast(msg, type = 'info') {
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.style.cssText =
      'position:fixed;bottom:60px;right:20px;z-index:999;display:flex;flex-direction:column;gap:8px;';
    document.body.appendChild(toastContainer);
  }
  const colors = {
    success: { bg:'#f0fdf4', border:'#bbf7d0', color:'#15803d' },
    warn:    { bg:'#fffbeb', border:'#fde68a', color:'#b45309' },
    info:    { bg:'#eff6ff', border:'#bfdbfe', color:'#1d4ed8' },
    error:   { bg:'#fef2f2', border:'#fecaca', color:'#dc2626' },
  };
  const c = colors[type] || colors.info;
  const toast = document.createElement('div');
  toast.style.cssText = `
    background:${c.bg};border:1px solid ${c.border};color:${c.color};
    padding:10px 16px;border-radius:8px;font-size:13px;font-family:'Inter',sans-serif;
    font-weight:500;box-shadow:0 4px 12px rgba(0,0,0,.08);
    max-width:300px;animation:slideIn .2s ease;
  `;
  toast.textContent = msg;

  const style = document.getElementById('toast-style');
  if (!style) {
    const s = document.createElement('style');
    s.id = 'toast-style';
    s.textContent = `
      @keyframes slideIn { from { opacity:0; transform:translateX(20px); } to { opacity:1; transform:none; } }
      @keyframes slideOut { to { opacity:0; transform:translateX(20px); } }
    `;
    document.head.appendChild(s);
  }

  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slideOut .2s ease forwards';
    setTimeout(() => toast.remove(), 220);
  }, 3200);
}

// ── Filter Interactions ───────────────────────
$$('.filter-input, .filter-select').forEach(input => {
  on(input, 'change', () => {
    showToast('Filter applied', 'info');
  });
});

// ── Table Sort ────────────────────────────────
$$('.data-table thead th').forEach((th, i) => {
  th.style.cursor = 'pointer';
  th.title = 'Click to sort';
  on(th, 'click', () => {
    const table = th.closest('table');
    const tbody = table.querySelector('tbody');
    if (!tbody) return;
    const rows = [...tbody.querySelectorAll('tr')];
    const asc = th.dataset.sort !== 'asc';
    th.dataset.sort = asc ? 'asc' : 'desc';

    $$('th', table).forEach(t => {
      t.textContent = t.textContent.replace(/ [▲▼]$/, '');
      delete t.dataset.sort;
    });
    th.dataset.sort = asc ? 'asc' : 'desc';
    th.textContent += asc ? ' ▲' : ' ▼';

    rows.sort((a, b) => {
      const av = a.cells[i]?.textContent.trim() || '';
      const bv = b.cells[i]?.textContent.trim() || '';
      const n = v => parseFloat(v.replace(/[^0-9.]/g, ''));
      if (!isNaN(n(av)) && !isNaN(n(bv)))
        return asc ? n(av) - n(bv) : n(bv) - n(av);
      return asc ? av.localeCompare(bv) : bv.localeCompare(av);
    });
    rows.forEach(r => tbody.appendChild(r));
  });
});

// ── Page Action Buttons ───────────────────────
$$('.btn-outline').forEach(btn => {
  on(btn, 'click', () => {
    const text = btn.textContent.trim();
    if (text.includes('Filter'))    showToast('Filter panel — coming soon', 'info');
    if (text.includes('Export'))    showToast('Exporting data…', 'info');
    if (text.includes('Refresh'))   showToast('Data refreshed', 'success');
    if (text.includes('Import'))    showToast('Import CSV — coming soon', 'info');
    if (text.includes('Scan RFID')) showToast('RFID scanner activated', 'info');
  });
});

// ── Keyboard Shortcuts ────────────────────────
on(document, 'keydown', e => {
  if (e.altKey) {
    const map = { d:'dashboard', r:'requisition', q:'quotations', p:'purchase-orders',
                  i:'invoices', c:'checkin', o:'checkout', a:'acknowledge' };
    const key = e.key.toLowerCase();
    if (map[key]) { e.preventDefault(); navigateTo(map[key]); }
  }
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
    e.preventDefault();
    searchBar.classList.add('open');
    searchInput.focus();
  }
});

// ── Init ──────────────────────────────────────
(function init() {
  navigateTo('dashboard');
  showToast('ICS loaded · Alt+D/R/Q/P/I shortcuts active', 'info');
})();