import { useState, useCallback } from 'react';
import { Globe } from 'lucide-react';
import SummaryOptions from '../components/SummaryOptions';
import SummaryResult from '../components/SummaryResult';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { summarizeWebsite } from '../services/api';
import './Summarizer.css';

const URL_REGEX = /^https?:\/\/.+\..+/;

function validateUrl(url) {
  if (!url.trim()) return 'Please enter a website URL.';
  if (!URL_REGEX.test(url.trim())) return 'Please enter a valid HTTP or HTTPS URL.';
  return '';
}

export default function WebsiteSummarizer() {
  const [url, setUrl] = useState('');
  const [summaryType, setSummaryType] = useState('detailed');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [urlError, setUrlError] = useState('');

  const submit = useCallback(async () => {
    const err = validateUrl(url);
    if (err) { setUrlError(err); return; }
    setUrlError('');
    setError('');
    setLoading(true);
    try {
      const data = await summarizeWebsite({ url: url.trim(), summary_type: summaryType });
      setResult(data);
    } catch (e) {
      setError(e.message || 'Failed to summarize website.');
    } finally {
      setLoading(false);
    }
  }, [url, summaryType]);

  const regenerate = useCallback(() => {
    if (!loading) submit();
  }, [loading, submit]);

  return (
    <main className="page-container">
      <header className="page-header">
        <div className="icon-row">
          <Globe size={18} aria-hidden="true" />
          <span>Website Summarizer</span>
        </div>
        <h1 className="page-title">Website Summarizer</h1>
        <p className="page-description">Understand articles and webpages without reading every line.</p>
      </header>

      <section className="card summarizer-card" aria-label="Website summarizer input">
        <div className="input-group">
          <label className="input-label" htmlFor="web-url">Website URL</label>
          <input
            id="web-url"
            type="url"
            className={`input-field${urlError ? ' input-field--error' : ''}`}
            placeholder="Paste the website URL here..."
            value={url}
            onChange={e => { setUrl(e.target.value); setUrlError(''); }}
            onKeyDown={e => e.key === 'Enter' && submit()}
            aria-invalid={!!urlError}
            aria-describedby={urlError ? 'web-url-error' : undefined}
            disabled={loading}
          />
          {urlError && <p id="web-url-error" className="field-error" role="alert">{urlError}</p>}
        </div>

        <SummaryOptions value={summaryType} onChange={setSummaryType} />

        <button
          id="web-submit"
          className="btn-primary"
          onClick={submit}
          disabled={loading}
          aria-busy={loading}
        >
          {loading ? 'Summarizing…' : 'Summarize Website'}
        </button>
      </section>

      {error && <ErrorMessage message={error} onRetry={submit} />}
      {loading && <LoadingSpinner />}

      {!loading && (
        <section aria-label="Summary result">
          <SummaryResult
            summary={result?.summary}
            metadata={result?.metadata}
            filename="website-summary.txt"
            onRegenerate={result ? regenerate : undefined}
            isRegenerating={loading}
          />
        </section>
      )}
    </main>
  );
}
