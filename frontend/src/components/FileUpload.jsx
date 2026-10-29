import { useState, useCallback, useRef } from 'react';
import { Upload, X, File } from 'lucide-react';
import './FileUpload.css';

const MAX_SIZE_MB = 20;
const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;
const ACCEPTED_TYPES = ['application/pdf'];

export default function FileUpload({ file, onFileChange }) {
  const [dragOver, setDragOver] = useState(false);
  const [fileError, setFileError] = useState('');
  const inputRef = useRef(null);

  function validateFile(f) {
    if (!ACCEPTED_TYPES.includes(f.type)) {
      setFileError('Only PDF files are supported.');
      return false;
    }
    if (f.size > MAX_SIZE_BYTES) {
      setFileError(`File exceeds the ${MAX_SIZE_MB} MB limit.`);
      return false;
    }
    setFileError('');
    return true;
  }

  const handleSelect = useCallback((f) => {
    if (!f) return;
    if (validateFile(f)) {
      onFileChange(f);
    } else {
      onFileChange(null);
    }
  }, [onFileChange]);

  function onInputChange(e) {
    handleSelect(e.target.files?.[0] || null);
  }

  function onDrop(e) {
    e.preventDefault();
    setDragOver(false);
    handleSelect(e.dataTransfer.files?.[0] || null);
  }

  function onDragOver(e) { e.preventDefault(); setDragOver(true); }
  function onDragLeave()   { setDragOver(false); }

  function removeFile() {
    onFileChange(null);
    setFileError('');
    if (inputRef.current) inputRef.current.value = '';
  }

  function formatSize(bytes) {
    if (bytes < 1024)        return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }

  return (
    <div className="file-upload-wrap">
      {!file ? (
        <div
          className={`dropzone${dragOver ? ' dropzone--active' : ''}`}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onClick={() => inputRef.current?.click()}
          role="button"
          tabIndex={0}
          aria-label="Drop your PDF here or click to browse files"
          onKeyDown={(e) => e.key === 'Enter' && inputRef.current?.click()}
        >
          <Upload size={24} className="dropzone-icon" aria-hidden="true" />
          <p className="dropzone-primary">Drop your PDF here or <span className="dropzone-link">browse files</span></p>
          <p className="dropzone-secondary">PDF supported · Max {MAX_SIZE_MB} MB</p>
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,application/pdf"
            className="dropzone-input"
            onChange={onInputChange}
            aria-hidden="true"
            tabIndex={-1}
          />
        </div>
      ) : (
        <div className="file-preview">
          <File size={18} className="file-preview-icon" aria-hidden="true" />
          <div className="file-preview-info">
            <p className="file-preview-name">{file.name}</p>
            <p className="file-preview-size">{formatSize(file.size)}</p>
          </div>
          <button
            className="file-remove-btn"
            onClick={removeFile}
            aria-label={`Remove ${file.name}`}
          >
            <X size={16} />
          </button>
        </div>
      )}

      {fileError && (
        <p className="file-error" role="alert">{fileError}</p>
      )}
    </div>
  );
}
