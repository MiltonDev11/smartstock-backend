// ==================================================
// SMARTSTOCK ADMIN - APP.JS (persistencia collapse + notifs + active menu)
// ==================================================

const notifBtn = document.getElementById('notifBtn');
const notifDot = document.getElementById('notifDot');
const notifDropdown = document.getElementById('notifDropdown');
const notifList = document.getElementById('notifList');
const clearNotifs = document.getElementById('clearNotifs');
const closeNotif = document.getElementById('closeNotif');
const collapseBtn = document.getElementById('collapseBtn');
const sidebar = document.querySelector('.sidebar');
const mainArea = document.querySelector('.main-area');

const STORAGE_NOTIFS = 'smartstock_notifs';
const STORAGE_DOT = 'smartstock_dot';
const STORAGE_COLLAPSED = 'smartstock_collapsed'; // <-- persistencia del sidebar

// ---------- NOTIFICACIONES ----------
function getNotifs() {
  return JSON.parse(localStorage.getItem(STORAGE_NOTIFS)) || [];
}
function saveNotifs(list) {
  localStorage.setItem(STORAGE_NOTIFS, JSON.stringify(list));
}
function updateDot() {
  const has = localStorage.getItem(STORAGE_DOT) === 'true';
  if (notifDot) notifDot.style.display = has ? 'block' : 'none';
}
function renderNotifs() {
  if (!notifList) return;
  const list = getNotifs();
  if (list.length === 0) {
    notifList.innerHTML = '<li style="color:#857768;">No hay avisos pendientes</li>';
    localStorage.setItem(STORAGE_DOT, 'false');
    updateDot();
    return;
  }
  notifList.innerHTML = '';
  list.forEach(n => {
    const li = document.createElement('li');
    li.textContent = n;
    notifList.appendChild(li);
  });
  localStorage.setItem(STORAGE_DOT, 'true');
  updateDot();
}
notifBtn?.addEventListener('click', () => {
  if (!notifDropdown) return;
  const isHidden = notifDropdown.hasAttribute('hidden');
  if (isHidden) {
    notifDropdown.removeAttribute('hidden');
    localStorage.setItem(STORAGE_DOT, 'false');
    updateDot();
  } else {
    notifDropdown.setAttribute('hidden', '');
  }
});
clearNotifs?.addEventListener('click', () => {
  localStorage.removeItem(STORAGE_NOTIFS);
  localStorage.setItem(STORAGE_DOT, 'false');
  renderNotifs();
});
closeNotif?.addEventListener('click', () => notifDropdown?.setAttribute('hidden', ''));

// ejemplo inicial (solo 1 vez)
if (!localStorage.getItem('initialized')) {
  saveNotifs([
    'En la sección de materiales, se necesita comprar tornillo 5mm.',
    'En la sección de stock, el producto "Silla tapizada" lleva 15 días en stock.'
  ]);
  localStorage.setItem('initialized', 'true');
  localStorage.setItem(STORAGE_DOT, 'true');
}

// ---------- SIDEBAR COLLAPSE (persistente) ----------
function applyCollapsedState() {
  const collapsed = localStorage.getItem(STORAGE_COLLAPSED) === 'true';
  if (collapsed) {
    sidebar?.classList.add('collapsed');
    mainArea?.classList.add('collapsed');
  } else {
    sidebar?.classList.remove('collapsed');
    mainArea?.classList.remove('collapsed');
  }
  // No necesitamos cambiar el icono con lucide: la rotación la hace CSS (.sidebar.collapsed svg)
  // Pero si lucide aún no ha renderizado (svg), la CSS aplicará cuando el svg exista.
}
function toggleCollapsed() {
  if (!sidebar) return;
  const isNow = !sidebar.classList.contains('collapsed');
  // Toggle classes:
  sidebar.classList.toggle('collapsed');
  mainArea?.classList.toggle('collapsed');
  // Guardar estado (después del toggle)
  const collapsedNow = sidebar.classList.contains('collapsed');
  localStorage.setItem(STORAGE_COLLAPSED, collapsedNow ? 'true' : 'false');
  // Re-dibujar icons (solo si necesitas forzar redraw). No obligatorio:
  try { if (window.lucide) window.lucide.createIcons(); } catch(e) {}
}

// bind
collapseBtn?.addEventListener('click', toggleCollapsed);

// apply on load
window.addEventListener('DOMContentLoaded', () => {
  renderNotifs();
  updateDot();
  applyCollapsedState();
  markActiveMenu();
});

// ---------- MARCAR MENU ACTIVO (según onclick) ----------
function markActiveMenu() {
  const current = window.location.pathname.split('/').pop().toLowerCase() || 'dashboard.html';
  document.querySelectorAll('.menu-btn').forEach(btn => {
    const onclick = btn.getAttribute('onclick') || '';
    const m = onclick.match(/'(.*?)'/);
    const target = m ? m[1].toLowerCase() : '';
    if (target && target === current) btn.classList.add('active');
    else btn.classList.remove('active');
  });
}

/* ---------- USER BADGE DROPDOWN + LOGOUT ---------- */
function setupUserMenu() {
  const badge = document.getElementById('adminBadge');
  const menu  = document.getElementById('userMenu');
  const logoutBtn = document.getElementById('logoutBtn');

  if (!badge || !menu) return;

  // Helper to open/close
  function openMenu() {
    menu.classList.add('open');
    menu.removeAttribute('hidden');
    badge.setAttribute('aria-expanded', 'true');
    try { if (window.lucide) window.lucide.createIcons(); } catch(e) {}
  }
  function closeMenu() {
    menu.classList.remove('open');
    menu.setAttribute('hidden', '');
    badge.setAttribute('aria-expanded', 'false');
  }
  function toggleMenu() {
    if (menu.classList.contains('open')) closeMenu();
    else openMenu();
  }

  // Toggle on badge click / Enter / Space
  badge.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleMenu();
  });
  badge.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleMenu();
    } else if (e.key === 'Escape') {
      closeMenu();
    }
  });

  // Close when clicking outside
  document.addEventListener('click', (ev) => {
    if (!badge.contains(ev.target) && !menu.contains(ev.target)) {
      if (menu.classList.contains('open')) closeMenu();
    }
  });

  // Close with ESC
  document.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape') closeMenu();
  });

  // Logout action: call /logout then redirect to /login
  logoutBtn?.addEventListener('click', async (ev) => {
    ev.preventDefault();
    try {
      // Usamos GET /logout (según tu ruta) y redirigimos al login.
      const resp = await fetch('/logout', { method: 'GET', credentials: 'same-origin' });
      // aunque la respuesta pueda ser un redirect, forzamos ir a login
      window.location.href = '/login';
    } catch (err) {
      // si fallo la petición, igual redirigimos para evitar quedar "pegado"
      window.location.href = '/login';
    }
  });
}

// integrarlo en el flujo de carga (si ya tienes DOMContentLoaded)
window.addEventListener('DOMContentLoaded', () => {
  try { setupUserMenu(); } catch (e) { /* no bloquear si error */ }
});
