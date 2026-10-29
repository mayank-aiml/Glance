import { AlertCircle } from 'lucide-react';
import './ErrorMessage.css';

export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="error-message" role="alert" aria-live="assertive">
      <AlertCircle size={18} className="error-icon" aria-hidden="true" />
      <div className="error-body">
        <p className="error-text">{message || 'Something went wrong. Please try again.'}</p>
        {onRetry && (
          <button className="error-retry" onClick={onRetry}>
            Try again
          </button>
        )}
      </div>
    </div>
  );
}
