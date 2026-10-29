import { useState, useCallback } from 'react';
import { AlignLeft, X } from 'lucide-react';
import SummaryOptions from '../components/SummaryOptions';
import SummaryResult from '../components/SummaryResult';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { summarizeText } from '../services/api';
import './Summarizer.css';

const MAX_CHARS = 50000;

export default function TextSummarizer() {
  const [text, setText] = useState('');
  const [summaryType, setSummaryType] = useState('detailed');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const charCount = text.length;
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const isEmpty = !text.trim();
  const overLimit = charCount > MAX_CHARS;

  const submit = useCallback(async () => {
    if (isEmpty || overLimit) return;
    setError('');
    setLoading(true);
    try {
      const data = await summarizeText({ text: text.trim(), summary_type: summaryType });
      setResult(data);
    } catch (e) {
      setError(e.message || 'Failed to summarize text.');
    } finally {
      setLoading(false);
    }
  }, [text, summaryType, isEmpty, overLimit]);

  const regenerate = useCallback(() => {
    if (!loading) submit();
  }, [loading, submit]);

  const clearText = () => setText('');

  return (
    <main className="page-container">
      <header className="page-header">
        <div className="icon-row">
          <AlignLeft size={18} aria-hidden="true" />
          <span>Text Summarizer</span>
        </div>
        <h1 className="page-title">Text Summarizer</h1>
        <p className="page-description">Turn long passages into concise, meaningful summaries.</p>
      </header>

      <section className="card summarizer-card" aria-label="Text summarizer input">
        <div className="input-group textarea-group">
          <div className="textarea-header">
            <label className="input-label" htmlFor="text-input">Your text</label>
            <div className="textarea-meta">
              <span className={`char-count${overLimit ? ' char-count--over' : ''}`}>
                {charCount.toLocaleString()} / {MAX_CHARS.toLocaleString()} characters
              </span>
              <span className="word-count">{wordCount.toLocaleString()} words</span>
            </div>
          </div>
          <textarea
            id="text-input"
            className={`input-field text-area${overLimit ? ' input-field--error' : ''}`}
            placeholder="Paste your text here to generate a summary..."
            value={text}
            onChange={e => { setText(e.target.value); setError(''); }}
            disabled={loading}
            aria-describedby={overLimit ? 'text-limit-error' : undefined}
            aria-invalid={overLimit}
          />
          {overLimit && (
            <p id="text-limit-error" className="field-error" role="alert">
              Text exceeds the {MAX_CHARS.toLocaleString()} character limit. Please shorten your input.
            </p>
          )}
        </div>

        <SummaryOptions value={summaryType} onChange={setSummaryType} />

        <div className="text-action-row">
          <button
            className="btn-secondary"
            onClick={clearText}
            disabled={isEmpty || loading}
            aria-label="Clear text"
          >
            <X size={14} aria-hidden="true" />
            Clear Text
          </button>
          <button
            id="text-submit"
            className="btn-primary"
            onClick={submit}
            disabled={loading || isEmpty || overLimit}
            aria-busy={loading}
          >
            {loading ? 'Summarizing…' : 'Summarize Text'}
          </button>
        </div>
      </section>

      {error && <ErrorMessage message={error} onRetry={!isEmpty ? submit : undefined} />}
      {loading && <LoadingSpinner />}

      {!loading && (
        <section aria-label="Summary result">
          <SummaryResult
            summary={result?.summary}
            metadata={result?.metadata}
            filename="text-summary.txt"
            onRegenerate={result ? regenerate : undefined}
            isRegenerating={loading}
          />
        </section>
      )}
    </main>
  );
}
