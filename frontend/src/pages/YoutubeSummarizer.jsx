import { useState, useCallback } from 'react';
import { Youtube } from 'lucide-react';
import SummaryOptions from '../components/SummaryOptions';
import SummaryResult from '../components/SummaryResult';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { summarizeYoutube } from '../services/api';
import './Summarizer.css';

const YT_REGEX = /^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|shorts\/)|youtu\.be\/)[A-Za-z0-9_-]{11}/;

function validateYoutubeUrl(url) {
  if (!url.trim()) return 'Please enter a YouTube URL.';
  if (!YT_REGEX.test(url.trim())) return 'Please enter a valid YouTube video URL.';
  return '';
}

export default function YoutubeSummarizer() {
  const [url, setUrl] = useState('');
  const [summaryType, setSummaryType] = useState('detailed');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [urlError, setUrlError] = useState('');

  const submit = useCallback(async () => {
    const err = validateYoutubeUrl(url);
    if (err) { setUrlError(err); return; }
    setUrlError('');
    setError('');
    setLoading(true);
    try {
      const data = await summarizeYoutube({ url: url.trim(), summary_type: summaryType });
      setResult(data);
    } catch (e) {
      setError(e.message || 'Failed to summarize video.');
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
          <Youtube size={18} aria-hidden="true" />
          <span>YouTube Summarizer</span>
        </div>
        <h1 className="page-title">YouTube Summarizer</h1>
        <p className="page-description">Turn lengthy videos into clear, useful summaries.</p>
      </header>

      <section className="card summarizer-card" aria-label="YouTube summarizer input">
        <div className="input-group">
          <label className="input-label" htmlFor="yt-url">YouTube video URL</label>
          <div className="url-input-row">
            <input
              id="yt-url"
              type="url"
              className={`input-field${urlError ? ' input-field--error' : ''}`}
              placeholder="Paste your YouTube video URL here..."
              value={url}
              onChange={e => { setUrl(e.target.value); setUrlError(''); }}
              onKeyDown={e => e.key === 'Enter' && submit()}
              aria-invalid={!!urlError}
              aria-describedby={urlError ? 'yt-url-error' : undefined}
              disabled={loading}
            />
          </div>
          {urlError && <p id="yt-url-error" className="field-error" role="alert">{urlError}</p>}
        </div>

        <SummaryOptions value={summaryType} onChange={setSummaryType} />

        <button
          id="yt-submit"
          className="btn-primary"
          onClick={submit}
          disabled={loading}
          aria-busy={loading}
        >
          {loading ? 'Summarizing…' : 'Summarize Video'}
        </button>
      </section>

      {error && <ErrorMessage message={error} onRetry={submit} />}
      {loading && <LoadingSpinner />}

      {!loading && (
        <section aria-label="Summary result">
          <SummaryResult
            summary={result?.summary}
            metadata={result?.metadata}
            filename="youtube-summary.txt"
            onRegenerate={result ? regenerate : undefined}
            isRegenerating={loading}
          />
        </section>
      )}
    </main>
  );
}
