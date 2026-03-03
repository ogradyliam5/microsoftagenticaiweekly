(function () {
  const KEY = 'maiw-theme';
  const root = document.documentElement;

  function preferredTheme() {
    const stored = localStorage.getItem(KEY);
    if (stored === 'light' || stored === 'dark') return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    document.querySelectorAll('[data-theme-toggle]').forEach((btn) => {
      const next = theme === 'dark' ? 'light' : 'dark';
      btn.setAttribute('aria-label', `Switch to ${next} mode`);
      btn.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
    });
  }

  function init() {
    applyTheme(preferredTheme());
    document.addEventListener('click', (event) => {
      const target = event.target.closest('[data-theme-toggle]');
      if (!target) return;
      const current = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      localStorage.setItem(KEY, next);
      applyTheme(next);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
