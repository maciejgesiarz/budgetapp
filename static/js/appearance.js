// static/js/appearance.js

// Inicjalizacja - działa na każdej stronie!
document.addEventListener('DOMContentLoaded', () => {
  const savedColor = localStorage.getItem('mainColor');
  const savedTheme = localStorage.getItem('theme');

  if (savedColor) {
    document.documentElement.style.setProperty('--main-color', savedColor);
  }
  if (savedTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
  }

  // Obsługa formularza tylko jeśli jesteśmy na stronie wyglądu
  const form = document.getElementById('appearance-form');
  if (form) {
    const colorPicker = document.getElementById('main-color-picker');
    const darkToggle  = document.getElementById('dark-mode-toggle');

    // Ustaw wartości formularza zgodnie z zapisanymi ustawieniami
    if (savedColor) colorPicker.value = savedColor;
    if (savedTheme === 'dark') darkToggle.checked = true;

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const color = colorPicker.value;
      const theme = darkToggle.checked ? 'dark' : 'light';

      localStorage.setItem('mainColor', color);
      localStorage.setItem('theme', theme);

      document.documentElement.style.setProperty('--main-color', color);
      document.documentElement.setAttribute('data-theme', theme);
    });
  }
});
