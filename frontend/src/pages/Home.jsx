import { Link } from 'react-router-dom';
import { Youtube, FileText, Globe, AlignLeft, ArrowRight } from 'lucide-react';
import './Home.css';

const TOOLS = [
  {
    to: '/youtube',
    icon: Youtube,
    label: 'YouTube',
    description: 'Turn lengthy videos into clear, useful summaries.',
    color: 'tool-card--yt',
  },
  {
    to: '/documents',
    icon: FileText,
    label: 'PDF & Documents',
    description: 'Extract essential information from lengthy documents.',
    color: 'tool-card--doc',
  },
  {
    to: '/website',
    icon: Globe,
    label: 'Website',
    description: 'Understand articles and webpages without reading every line.',
    color: 'tool-card--web',
  },
  {
    to: '/text',
    icon: AlignLeft,
    label: 'Plain Text',
    description: 'Turn long passages into concise, meaningful summaries.',
    color: 'tool-card--text',
  },
];

export default function Home() {
  return (
    <main className="page-container home-page">
      <section className="home-intro" aria-label="Introduction">
        <h1 className="home-heading">Understand more.<br />In less time.</h1>
        <p className="home-sub">Summarize videos, documents, websites, and text in one place.</p>
      </section>

      <section className="tools-grid" aria-label="Available tools">
        {TOOLS.map(({ to, icon: Icon, label, description, color }) => (
          <Link key={to} to={to} className={`tool-card ${color}`} aria-label={`Open ${label} summarizer`}>
            <div className="tool-card-icon">
              <Icon size={22} aria-hidden="true" />
            </div>
            <div className="tool-card-body">
              <h2 className="tool-card-title">{label}</h2>
              <p className="tool-card-desc">{description}</p>
            </div>
            <ArrowRight size={16} className="tool-card-arrow" aria-hidden="true" />
          </Link>
        ))}
      </section>
    </main>
  );
}
