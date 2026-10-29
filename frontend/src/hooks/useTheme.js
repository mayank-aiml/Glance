import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'glance-theme';

function getSystemTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTheme(effective) {
  document.documentElement.setAttribute('data-theme', effective);
}

export function useTheme() {
  const [mode, setMode] = useState(() => {
    try {
      return localStorage.getItem(STORAGE_KEY) || 'system';
    } catch {
      return 'system';
    }
  });

  const [systemTheme, setSystemTheme] = useState(getSystemTheme);

  // Listen to OS theme changes
  useEffect(() => {
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = (e) => setSystemTheme(e.matches ? 'dark' : 'light');
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);

  // Resolve effective theme
  const effectiveTheme = mode === 'system' ? systemTheme : mode;

  // Apply whenever effective theme changes
  useEffect(() => {
    applyTheme(effectiveTheme);
  }, [effectiveTheme]);

  const setThemeMode = useCallback((newMode) => {
    setMode(newMode);
    try {
      localStorage.setItem(STORAGE_KEY, newMode);
    } catch {}
  }, []);

  return { mode, effectiveTheme, setThemeMode };
}
