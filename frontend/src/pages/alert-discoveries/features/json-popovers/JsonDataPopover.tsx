import React, { useState, useRef, useEffect } from 'react';

interface JsonDataPopoverProps {
  data: Record<string, unknown> | null | undefined;
  title: string;
  buttonLabel: string;
  buttonIcon?: string;
  variant?: 'default' | 'secondary';
}

// Format value for display
const formatValue = (value: unknown): string => {
  if (value === null || value === undefined) return 'N/A';
  if (typeof value === 'boolean') return value ? 'Yes' : 'No';
  if (typeof value === 'number') {
    // Format large numbers with commas
    if (Math.abs(value) >= 1000) {
      return value.toLocaleString('en-US', { maximumFractionDigits: 2 });
    }
    return String(value);
  }
  if (typeof value === 'string') {
    // Try to parse as number for formatting
    const num = parseFloat(value);
    if (!isNaN(num) && Math.abs(num) >= 1000) {
      return num.toLocaleString('en-US', { maximumFractionDigits: 2 });
    }
    return value;
  }
  if (Array.isArray(value)) {
    return value.length > 0 ? value.join(', ') : 'Empty';
  }
  if (typeof value === 'object') {
    return JSON.stringify(value);
  }
  return String(value);
};

// Convert key to readable label
const formatKey = (key: string): string => {
  return key
    .replace(/_/g, ' ')
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
    .trim();
};

// Flatten nested objects for display
const flattenObject = (obj: Record<string, unknown>, prefix = ''): Array<{ key: string; value: unknown }> => {
  const result: Array<{ key: string; value: unknown }> = [];

  for (const [key, value] of Object.entries(obj)) {
    const newKey = prefix ? `${prefix} > ${key}` : key;

    if (value && typeof value === 'object' && !Array.isArray(value)) {
      result.push(...flattenObject(value as Record<string, unknown>, newKey));
    } else {
      result.push({ key: newKey, value });
    }
  }

  return result;
};

const JsonDataPopover: React.FC<JsonDataPopoverProps> = ({
  data,
  title,
  buttonLabel,
  buttonIcon = '',
  variant = 'default',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const popoverRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // Close on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        popoverRef.current &&
        !popoverRef.current.contains(event.target as Node) &&
        buttonRef.current &&
        !buttonRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  // Close on Escape key
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen]);

  const hasData = data && Object.keys(data).length > 0;
  const entries = hasData ? flattenObject(data) : [];

  return (
    <div className="json-popover-container">
      <button
        ref={buttonRef}
        className={`json-popover-btn ${variant} ${!hasData ? 'disabled' : ''}`}
        onClick={() => hasData && setIsOpen(!isOpen)}
        disabled={!hasData}
        title={hasData ? `View ${title}` : 'No data available'}
      >
        {buttonIcon && <span className="btn-icon">{buttonIcon}</span>}
        <span className="btn-label">{buttonLabel}</span>
      </button>

      {isOpen && hasData && (
        <div ref={popoverRef} className="json-popover">
          <div className="json-popover-header">
            <h4>{title}</h4>
            <button className="json-popover-close" onClick={() => setIsOpen(false)}>
              &times;
            </button>
          </div>
          <div className="json-popover-body">
            <table className="json-data-table">
              <tbody>
                {entries.map(({ key, value }, index) => (
                  <tr key={index}>
                    <td className="json-key">{formatKey(key)}</td>
                    <td className="json-value">{formatValue(value)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default JsonDataPopover;
