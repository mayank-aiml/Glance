import { useState, useCallback } from 'react';
import { Copy, Download, RefreshCw, CheckCheck } from 'lucide-react';
import './SummaryResult.css';

function renderMarkdown(text) {
  if (!text) return [];
  const lines = text.split('\n');
  const elements = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    if (!line.trim()) { i++; continue; }

    // Heading
    const h3 = line.match(/^###\s+(.*)/);
    const h2 = line.match(/^##\s+(.*)/);
    const h1 = line.match(/^#\s+(.*)/);
    if (h1) { elements.push(<h1 key={i} className="md-h1">{h1[1]}</h1>); i++; continue; }
    if (h2) { elements.push(<h2 key={i} className="md-h2">{h2[1]}</h2>); i++; continue; }
    if (h3) { elements.push(<h3 key={i} className="md-h3">{h3[1]}</h3>); i++; continue; }

    // Bullet list
    if (line.match(/^[\-\*]\s+/)) {
      const items = [];
      while (i < lines.length && lines[i].match(/^[\-\*]\s+/)) {
        items.push(<li key={i}>{inlineFormat(lines[i].replace(/^[\-\*]\s+/, ''))}</li>);
        i++;
      }
      elements.push(<ul key={`ul-${i}`} className="md-ul">{items}</ul>);
      continue;
    }

    // Numbered list
    if (line.match(/^\d+\.\s+/)) {
      const items = [];
      while (i < lines.length && lines[i].match(/^\d+\.\s+/)) {
        items.push(<li key={i}>{inlineFormat(lines[i].replace(/^\d+\.\s+/, ''))}</li>);
        i++;
      }
      elements.push(<ol key={`ol-${i}`} className="md-ol">{items}</ol>);
      continue;
    }

    // Paragraph
    elements.push(<p key={i} className="md-p">{inlineFormat(line)}</p>);
    i++;
  }

  return elements;
}

function inlineFormat(text) {
  // Bold **text**
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, idx) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={idx}>{part.slice(2, -2)}</strong>;
    }
    return part;
  });
}

export default function SummaryResult({ summary, metadata, filename, onRegenerate, isRegenerating }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    if (!summary) return;
    try {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback for older browsers
      const ta = document.createElement('textarea');
      ta.value = summary;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus(); ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [summary]);

  const handleDownload = useCallback(() => {
    if (!summary) return;
    const blob = new Blob([summary], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'glance-summary.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, [summary, filename]);

  if (!summary) {
    return (
      <div className="summary-result summary-result--empty">
        <div className="summary-empty-icon" aria-hidden="true">✦</div>
        <p className="summary-empty-text">Your summary will appear here.</p>
        <p className="summary-empty-sub">Choose a format above and submit your content to get started.</p>
      </div>
    );
  }

  return (
    <div className="summary-result" aria-live="polite" aria-label="Generated summary">
      <div className="summary-result-header">
        <div className="summary-result-meta">
          <h2 className="summary-result-title">Summary</h2>
          {metadata?.title && (
            <p className="summary-result-source">{metadata.title}</p>
          )}
          {metadata?.duration && (
            <p className="summary-result-source">
              Duration: {Math.floor(metadata.duration / 60)}m {metadata.duration % 60}s
            </p>
          )}
        </div>
        <div className="summary-result-actions">
          <button
            className="btn-secondary result-action-btn"
            onClick={handleCopy}
            aria-label="Copy summary to clipboard"
          >
            {copied ? <CheckCheck size={14} /> : <Copy size={14} />}
            {copied ? 'Copied!' : 'Copy'}
          </button>
          <button
            className="btn-secondary result-action-btn"
            onClick={handleDownload}
            aria-label="Download summary as text file"
          >
            <Download size={14} />
            Download
          </button>
          {onRegenerate && (
            <button
              className="btn-secondary result-action-btn"
              onClick={onRegenerate}
              disabled={isRegenerating}
              aria-label="Regenerate summary"
            >
              <RefreshCw size={14} className={isRegenerating ? 'spinning' : ''} />
              {isRegenerating ? 'Regenerating…' : 'Regenerate'}
            </button>
          )}
        </div>
      </div>

      <hr className="summary-divider" />

      <div className="summary-content" tabIndex={0}>
        {renderMarkdown(summary)}
      </div>
    </div>
  );
}
