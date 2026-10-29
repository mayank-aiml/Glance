import { useState, useCallback } from 'react';
import { FileText } from 'lucide-react';
import FileUpload from '../components/FileUpload';
import SummaryOptions from '../components/SummaryOptions';
import SummaryResult from '../components/SummaryResult';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { summarizeDocument } from '../services/api';
import './Summarizer.css';

export default function DocumentSummarizer() {
  const [file, setFile] = useState(null);
  const [summaryType, setSummaryType] = useState('detailed');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const submit = useCallback(async () => {
    if (!file) return;
    setError('');
    setLoading(true);
    try {
      const data = await summarizeDocument({ file, summary_type: summaryType });
      setResult(data);
    } catch (e) {
      setError(e.message || 'Failed to summarize document.');
    } finally {
      setLoading(false);
    }
  }, [file, summaryType]);

  const regenerate = useCallback(() => {
    if (!loading) submit();
  }, [loading, submit]);

  return (
    <main className="page-container">
      <header className="page-header">
        <div className="icon-row">
          <FileText size={18} aria-hidden="true" />
          <span>PDF & Documents Summarizer</span>
        </div>
        <h1 className="page-title">PDF &amp; Documents Summarizer</h1>
        <p className="page-description">Extract the essential information from lengthy documents.</p>
      </header>

      <section className="card summarizer-card" aria-label="Document summarizer input">
        <FileUpload file={file} onFileChange={(f) => { setFile(f); setError(''); }} />
        <SummaryOptions value={summaryType} onChange={setSummaryType} />
        <button
          id="doc-submit"
          className="btn-primary"
          onClick={submit}
          disabled={loading || !file}
          aria-busy={loading}
        >
          {loading ? 'Summarizing…' : 'Summarize Document'}
        </button>
      </section>

      {error && <ErrorMessage message={error} onRetry={file ? submit : undefined} />}
      {loading && <LoadingSpinner />}

      {!loading && (
        <section aria-label="Summary result">
          <SummaryResult
            summary={result?.summary}
            metadata={result?.metadata}
            filename="document-summary.txt"
            onRegenerate={result ? regenerate : undefined}
            isRegenerating={loading}
          />
        </section>
      )}
    </main>
  );
}
