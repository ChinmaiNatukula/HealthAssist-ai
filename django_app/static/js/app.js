// ── HealthAssist AI — Global JavaScript ─────────────────────

// ── CSRF Cookie Helper ─────────────────────────────────────
function getCookie(name) {
  let v = null;
  document.cookie.split(';').forEach(c => {
    const [k, val] = c.trim().split('=');
    if (k === name) v = decodeURIComponent(val);
  });
  return v;
}

// ── Toast Notifications ────────────────────────────────────
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer') || createToastContainer();
  const toast = document.createElement('div');
  const icons = { success: 'fa-circle-check', error: 'fa-circle-xmark', info: 'fa-circle-info', warning: 'fa-triangle-exclamation' };
  const cls = type === 'error' ? 'danger' : type;
  toast.className = `toast ${cls}`;
  toast.innerHTML = `<i class="fa-solid ${icons[type] || icons.info}"></i> ${message}`;
  container.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(20px)'; toast.style.transition = 'all 0.3s'; setTimeout(() => toast.remove(), 300); }, 3500);
}

function createToastContainer() {
  const c = document.createElement('div');
  c.id = 'toastContainer';
  c.className = 'toast-container';
  document.body.appendChild(c);
  return c;
}

// ── Auto-dismiss Django messages ───────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('#toastContainer .toast').forEach((toast, i) => {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(20px)';
      toast.style.transition = 'all 0.3s';
      setTimeout(() => toast.remove(), 300);
    }, 3000 + i * 500);
  });
});

// ── Navbar Scroll Effect ───────────────────────────────────
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  });
}

// ── Mobile Nav Toggle ──────────────────────────────────────
function toggleNav() {
  const links = document.getElementById('navLinks');
  const ham = document.getElementById('hamburger');
  if (!links) return;
  const open = links.classList.toggle('open');
  // Animate hamburger
  if (ham) {
    const spans = ham.querySelectorAll('span');
    if (open) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  }
}

// ── Close nav when clicking outside ───────────────────────
document.addEventListener('click', e => {
  const links = document.getElementById('navLinks');
  const ham = document.getElementById('hamburger');
  if (links && links.classList.contains('open') && !links.contains(e.target) && !ham?.contains(e.target)) {
    toggleNav();
  }
});

// ── Scroll-reveal animations ───────────────────────────────
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.style.opacity = '1'; e.target.style.transform = 'translateY(0)'; } });
}, { threshold: 0.1 });

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.fade-in').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });
});
