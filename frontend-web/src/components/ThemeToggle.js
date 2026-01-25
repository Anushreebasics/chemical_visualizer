import React, { useEffect, useState } from 'react';

function ThemeToggle({ className = '' }) {
  const [theme, setTheme] = useState(
    () => localStorage.getItem('theme') || 'light'
  );

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggle = () => setTheme((t) => (t === 'light' ? 'dark' : 'light'));

  return (
    <button
      aria-label="Toggle theme"
      title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      onClick={toggle}
      className={`btn btn-secondary theme-toggle ${className}`}
      style={{ display: 'inline-flex', alignItems: 'center', gap: 8 }}
    >
      <i className={`fas ${theme === 'light' ? 'fa-moon' : 'fa-sun'}`}></i>
      <span style={{ fontWeight: 600 }}>{theme === 'light' ? 'Dark' : 'Light'} mode</span>
    </button>
  );
}

export default ThemeToggle;
