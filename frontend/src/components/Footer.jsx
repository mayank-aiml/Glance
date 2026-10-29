import { Link } from 'react-router-dom';
import { Linkedin, Github } from 'lucide-react';
import { SOCIAL_LINKS } from '../config/socialLinks';
import './Footer.css';

const FOOTER_LINKS = [
  { to: '/',          label: 'Home'                  },
  { to: '/youtube',   label: 'YouTube Summarizer'    },
  { to: '/documents', label: 'PDF & Documents'       },
  { to: '/website',   label: 'Website Summarizer'    },
  { to: '/text',      label: 'Text Summarizer'       },
];

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="footer" role="contentinfo">
      <div className="footer-inner">
        {/* Brand */}
        <div className="footer-brand">
          <div className="footer-logo">
            <span className="logo-gla">Gla</span><span className="logo-nce">nce</span>
          </div>
          <p className="footer-tagline">Everything important, at a glance.</p>
        </div>

        {/* Navigation */}
        <nav className="footer-nav" aria-label="Footer navigation">
          <p className="footer-nav-heading">Navigation</p>
          {FOOTER_LINKS.map(({ to, label }) => (
            <Link key={to} to={to} className="footer-link">{label}</Link>
          ))}
        </nav>

        {/* Connect */}
        <div className="footer-connect">
          <p className="footer-nav-heading">Connect with me</p>
          <div className="footer-socials">
            <a
              href={SOCIAL_LINKS.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="footer-social-link"
              aria-label="LinkedIn profile"
            >
              <Linkedin size={16} aria-hidden="true" />
              LinkedIn
            </a>
            <a
              href={SOCIAL_LINKS.github}
              target="_blank"
              rel="noopener noreferrer"
              className="footer-social-link"
              aria-label="GitHub profile"
            >
              <Github size={16} aria-hidden="true" />
              GitHub
            </a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; {year} Glance. All rights reserved.</p>
      </div>
    </footer>
  );
}
