import React, { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import './KpiCard.css';

interface KpiDetail {
  label: string;
  value: string | number;
  description?: string;
}

interface KpiCardProps {
  icon: string;
  label: string;
  value: string | number;
  trend?: {
    icon: string;
    text: string;
  };
  helpTitle: string;
  helpContent: React.ReactNode;
  glowColor: 'cyan' | 'red' | 'amber' | 'blue';
  variant?: 'featured' | 'danger' | 'warning' | 'info';
  animationDelay?: string;
  details?: KpiDetail[];
  alertNames?: string[];
  onClick?: () => void;
}

const KpiCard: React.FC<KpiCardProps> = ({
  icon,
  label,
  value,
  trend,
  helpTitle,
  helpContent,
  glowColor,
  variant = 'info',
  animationDelay = '0s',
  details,
  alertNames,
  onClick,
}) => {
  const [showHelp, setShowHelp] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState({ top: 0, left: 0, width: 380 });
  const [popoverPosition, setPopoverPosition] = useState({ top: 0, left: 0 });
  const helpBtnRef = useRef<HTMLButtonElement>(null);
  const cardRef = useRef<HTMLDivElement>(null);

  const variantClass = variant === 'featured' ? 'kpi-featured' : `kpi-${variant}`;
  const valueClass = variant === 'featured' ? 'kpi-value-large' : 'kpi-value';

  // Update tooltip position when showing - with viewport boundary check
  useEffect(() => {
    if (showHelp && helpBtnRef.current) {
      const rect = helpBtnRef.current.getBoundingClientRect();
      const tooltipWidth = 380;
      let left = rect.left + rect.width / 2;

      // Prevent tooltip from going off-screen right
      if (left + tooltipWidth / 2 > window.innerWidth - 20) {
        left = window.innerWidth - tooltipWidth / 2 - 20;
      }
      // Prevent tooltip from going off-screen left
      if (left - tooltipWidth / 2 < 20) {
        left = tooltipWidth / 2 + 20;
      }

      setTooltipPosition({
        top: rect.bottom + 12,
        left: left,
        width: tooltipWidth,
      });
    }
  }, [showHelp]);

  // Update popover position when showing
  useEffect(() => {
    if (showDetails && cardRef.current) {
      const rect = cardRef.current.getBoundingClientRect();
      let left = rect.left;

      // Prevent popover from going off-screen right
      if (left + 380 > window.innerWidth - 20) {
        left = window.innerWidth - 380 - 20;
      }

      setPopoverPosition({
        top: rect.bottom + 12,
        left: left,
      });
    }
  }, [showDetails]);

  // Close on escape key
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setShowHelp(false);
        setShowDetails(false);
      }
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, []);

  // Close on click outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (showHelp || showDetails) {
        const target = e.target as HTMLElement;
        if (!target.closest('.intel-panel') && !target.closest('.kpi-help-btn') && !target.closest('.kpi-card')) {
          setShowHelp(false);
          setShowDetails(false);
        }
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showHelp, showDetails]);

  const handleCardClick = () => {
    if (details || alertNames) {
      setShowDetails(!showDetails);
    }
    if (onClick) {
      onClick();
    }
  };

  return (
    <div
      ref={cardRef}
      className={`kpi-card ${variantClass} ${(details || alertNames) ? 'kpi-clickable' : ''}`}
      style={{ animationDelay, position: 'relative' }}
      onClick={handleCardClick}
    >
      <div className="kpi-header">
        <span className="kpi-icon">{icon}</span>
        <span className="kpi-label">{label}</span>
        <button
          ref={helpBtnRef}
          type="button"
          className="kpi-help-btn"
          onMouseEnter={() => setShowHelp(true)}
          onMouseLeave={() => setShowHelp(false)}
          onClick={(e) => {
            e.stopPropagation();
            setShowHelp(!showHelp);
          }}
          aria-label="Help"
        >
          ?
        </button>
      </div>

      {/* Alert Names */}
      {alertNames && alertNames.length > 0 && (
        <div className="kpi-alert-names">
          {alertNames.slice(0, 2).map((name, idx) => (
            <span key={idx} className="kpi-alert-name" title={name}>
              {name.length > 30 ? name.substring(0, 30) + '...' : name}
            </span>
          ))}
          {alertNames.length > 2 && (
            <span className="kpi-alert-more">+{alertNames.length - 2} more</span>
          )}
        </div>
      )}

      <div className={valueClass}>
        {value}
      </div>

      {trend && (
        <div className="kpi-trend">
          <span className="trend-icon">{trend.icon}</span>
          <span className="trend-text">{trend.text}</span>
        </div>
      )}

      {variant === 'featured' && (
        <div className="kpi-footer">
          <div className="kpi-bar">
            <div className="kpi-bar-fill" style={{ width: '100%' }}></div>
          </div>
        </div>
      )}

      <div className={`card-glow glow-${glowColor}`}></div>

      {/* Click hint */}
      {(details || alertNames) && (
        <div className="kpi-click-hint">
          Click for details
        </div>
      )}

      {/* Help Tooltip - Intel Briefing Panel */}
      {showHelp && createPortal(
        <div
          className="intel-panel intel-tooltip"
          style={{
            position: 'fixed',
            top: tooltipPosition.top,
            left: tooltipPosition.left,
            transform: 'translateX(-50%)',
            width: tooltipPosition.width,
          }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="intel-panel-noise"></div>
          <div className="intel-panel-border"></div>
          <div className="intel-header">
            <div className="intel-header-left">
              <span className="intel-status-dot"></span>
              <span className="intel-classification">INTEL BRIEFING</span>
            </div>
            <button
              className="intel-close"
              onClick={(e) => {
                e.stopPropagation();
                setShowHelp(false);
              }}
              aria-label="Close"
            >
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M1 1L13 13M1 13L13 1" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </button>
          </div>
          <div className="intel-title-bar">
            <h3 className="intel-title">{helpTitle}</h3>
          </div>
          <div className="intel-content">
            {helpContent}
          </div>
          <div className="intel-footer">
            <span className="intel-footer-text">Press ESC to close</span>
          </div>
        </div>,
        document.body
      )}

      {/* Details Popover - Data Panel */}
      {showDetails && (details || alertNames) && createPortal(
        <div
          className="intel-panel intel-popover"
          style={{
            position: 'fixed',
            top: popoverPosition.top,
            left: popoverPosition.left,
            width: 380,
          }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="intel-panel-noise"></div>
          <div className="intel-panel-border"></div>
          <div className="intel-header">
            <div className="intel-header-left">
              <span className="intel-status-dot active"></span>
              <span className="intel-classification">DATA REPORT</span>
            </div>
            <button
              className="intel-close"
              onClick={(e) => {
                e.stopPropagation();
                setShowDetails(false);
              }}
              aria-label="Close"
            >
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M1 1L13 13M1 13L13 1" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </button>
          </div>
          <div className="intel-title-bar">
            <h3 className="intel-title">{label}</h3>
          </div>
          <div className="intel-content">
            {alertNames && alertNames.length > 0 && (
              <div className="intel-section">
                <div className="intel-section-header">
                  <span className="intel-section-label">ALERTS ANALYZED</span>
                  <span className="intel-section-count">{alertNames.length}</span>
                </div>
                <ul className="intel-list">
                  {alertNames.map((name, idx) => (
                    <li key={idx} className="intel-list-item">
                      <span className="intel-list-marker">▸</span>
                      <span className="intel-list-text">{name}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {details && details.length > 0 && (
              <div className="intel-section">
                <div className="intel-section-header">
                  <span className="intel-section-label">BREAKDOWN</span>
                </div>
                <div className="intel-table">
                  {details.map((detail, idx) => (
                    <div key={idx} className="intel-table-row">
                      <span className="intel-table-label">{detail.label}</span>
                      <span className="intel-table-value">{detail.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          <div className="intel-footer">
            <span className="intel-footer-text">Click outside to close</span>
          </div>
        </div>,
        document.body
      )}
    </div>
  );
};

export default KpiCard;
