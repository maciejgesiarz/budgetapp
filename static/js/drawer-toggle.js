document.addEventListener('DOMContentLoaded', () => {
  const drawer    = document.getElementById('drawer-settings');
  const toggleBtn = document.querySelector('.drawer-toggle-btn');
  const sidebarLinks = document.querySelectorAll('.sidebar .nav-link:not([href$="' + window.location.pathname + '"])');

  if (!drawer || !toggleBtn) return;

  // 1) Automatyczne otwarcie na /settings/*
  if (window.location.pathname.startsWith('/settings')) {
    drawer.classList.add('open');
    document.body.classList.add('drawer-open');
  }

  // 2) Toggle przycisku chevron
  toggleBtn.addEventListener('click', e => {
    e.preventDefault();
    const isOpen = drawer.classList.toggle('open');
    document.body.classList.toggle('drawer-open', isOpen);
  });

  // 3) Klik w inny link sidebaru → zamknięcie drawer
  document.querySelectorAll('.sidebar .nav-link[href!="' + window.location.pathname + '"]').forEach(link => {
    link.addEventListener('click', () => {
      drawer.classList.remove('open');
      document.body.classList.remove('drawer-open');
    });
  });
});
