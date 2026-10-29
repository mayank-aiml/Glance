import './SummaryOptions.css';

const OPTIONS = [
  { value: 'quick',        label: 'Quick Summary'     },
  { value: 'detailed',     label: 'Detailed Summary'  },
  { value: 'study_notes',  label: 'Study Notes'       },
  { value: 'executive',    label: 'Executive Summary' },
  { value: 'key_takeaways', label: 'Key Takeaways'   },
];

export default function SummaryOptions({ value, onChange }) {
  return (
    <div className="summary-options" role="group" aria-label="Summary format">
      <p className="summary-options-label">Summary format</p>
      <div className="summary-options-list">
        {OPTIONS.map(opt => (
          <button
            key={opt.value}
            type="button"
            className={`summary-option-btn${value === opt.value ? ' summary-option-btn--active' : ''}`}
            onClick={() => onChange(opt.value)}
            aria-pressed={value === opt.value}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  );
}
