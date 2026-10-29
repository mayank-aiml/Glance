import './LoadingSpinner.css';

export default function LoadingSpinner({ message = 'Analyzing your content…' }) {
  return (
    <div className="loading-spinner-wrap" role="status" aria-live="polite">
      <div className="loading-ring" aria-hidden="true">
        <span /><span /><span />
      </div>
      <p className="loading-message">{message}</p>
    </div>
  );
}
