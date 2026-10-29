import { useState, useRef, useEffect } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { Youtube, FileText, Globe, AlignLeft, Sun, Moon, Monitor, ChevronDown, Menu, X } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';
import './Navbar.css';

const NAV_ITEMS = [
  { to: '/youtube',   label: 'YouTube',       icon: Youtube   },
  { to: '/documents', label: 'PDF & Docs',    icon: FileText  },
  { to: '/website',   label: 'Website',       icon: Globe     },
  { to: '/text',      label: 'Text',          icon: AlignLeft },
];

const THEME_OPTIONS = [
  { value: 'system', label: 'System', icon: Monitor },
  { value: 'light',  label: 'Light',  icon: Sun     },
  { value: 'dark',   label: 'Dark',   icon: Moon    },
];

export default function Navbar() {
  const { mode, setThemeMode } = useTheme();
  const [themeOpen, setThemeOpen] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const themeRef = useRef(null);
  const navigate = useNavigate();

  // Close theme dropdown on outside click
  useEffect(() => {
    function handler(e) {
      if (themeRef.current && !themeRef.current.contains(e.target)) {
        setThemeOpen(false);
      }
    }
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setMobileOpen(false);
  }, [navigate]);

  const currentTheme = THEME_OPTIONS.find(t => t.value === mode);
  const ThemeIcon = currentTheme?.icon || Monitor;

  return (
    <header className="navbar" role="banner">
      <div className="navbar-inner">
        {/* Logo */}
        <Link to="/" className="navbar-logo" aria-label="Glance home">
          <span className="logo-gla">Gla</span><span className="logo-nce">nce</span>
        </Link>

        {/* Desktop nav */}
        <nav className="navbar-nav" aria-label="Main navigation">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `nav-item${isActive ? ' nav-item--active' : ''}`
              }
            >
              <Icon size={15} aria-hidden="true" />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Right: theme switcher + mobile toggle */}
        <div className="navbar-right">
          {/* Theme dropdown */}
          <div className="theme-switcher" ref={themeRef}>
            <button
              className="theme-trigger"
              onClick={() => setThemeOpen(o => !o)}
              aria-label={`Theme: ${currentTheme?.label}. Click to change.`}
              aria-expanded={themeOpen}
              aria-haspopup="listbox"
            >
              <ThemeIcon size={15} aria-hidden="true" />
              <span className="theme-label">{currentTheme?.label}</span>
              <ChevronDown size={13} className={`chevron ${themeOpen ? 'open' : ''}`} aria-hidden="true" />
            </button>

            {themeOpen && (
              <ul className="theme-dropdown" role="listbox" aria-label="Select theme">
                {THEME_OPTIONS.map(({ value, label, icon: Icon }) => (
                  <li key={value}>
                    <button
                      role="option"
                      aria-selected={mode === value}
                      className={`theme-option${mode === value ? ' theme-option--active' : ''}`}
                      onClick={() => { setThemeMode(value); setThemeOpen(false); }}
                    >
                      <Icon size={14} aria-hidden="true" />
                      {label}
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Mobile hamburger */}
          <button
            className="mobile-toggle"
            onClick={() => setMobileOpen(o => !o)}
            aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={mobileOpen}
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <nav className="mobile-nav" aria-label="Mobile navigation">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `mobile-nav-item${isActive ? ' mobile-nav-item--active' : ''}`
              }
              onClick={() => setMobileOpen(false)}
            >
              <Icon size={16} aria-hidden="true" />
              {label}
            </NavLink>
          ))}
          <div className="mobile-theme-row">
            {THEME_OPTIONS.map(({ value, label, icon: Icon }) => (
              <button
                key={value}
                className={`mobile-theme-btn${mode === value ? ' mobile-theme-btn--active' : ''}`}
                onClick={() => { setThemeMode(value); setMobileOpen(false); }}
              >
                <Icon size={14} aria-hidden="true" />
                {label}
              </button>
            ))}
          </div>
        </nav>
      )}
    </header>
  );
}
