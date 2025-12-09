import React from 'react';
import { CriticalDiscoveryDrilldown, CriticalDiscovery, ConcentrationMetric, KeyFinding } from '../services/api';

interface DiscoveryDetailPanelProps {
  discovery: CriticalDiscoveryDrilldown;
  mode: 'modal' | 'inline' | 'popover';
  onClose: () => void;
  currencyFormatter: Intl.NumberFormat;
  onViewAnalysis?: (discovery: CriticalDiscoveryDrilldown) => void;
  onCreateAction?: (discovery: CriticalDiscoveryDrilldown) => void;
}

// Format number with thousands separators
const formatNumber = (value: string | number | null | undefined): string => {
  if (value === null || value === undefined) return 'N/A';
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return String(value);
  if (num < 100 && String(value).includes('.')) {
    return num.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 2 });
  }
  return num.toLocaleString('en-US', { maximumFractionDigits: 0 });
};

// Format period for display
const formatPeriod = (start?: string, end?: string): string => {
  if (!start && !end) return 'N/A';

  const formatDate = (dateStr: string) => {
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  };

  if (start && end) {
    return `${formatDate(start)} vs Prior Year`;
  }
  return start ? formatDate(start) : end ? formatDate(end) : 'N/A';
};

const DiscoveryDetailPanel: React.FC<DiscoveryDetailPanelProps> = ({
  discovery,
  mode,
  onClose,
  currencyFormatter,
  onCreateAction,
}) => {
  const hasDiscoveries = discovery.discoveries && discovery.discoveries.length > 0;
  const hasFraudIndicators = hasDiscoveries && discovery.discoveries.some(d => d.is_fraud_indicator);

  const content = (
    <div className={`discovery-detail ${mode}`}>
      {/* Header */}
      <div className="discovery-detail-header">
        <div className="discovery-detail-title">
          <h3>{discovery.alert_name}</h3>
          <span className="discovery-detail-id">{discovery.alert_id}</span>
        </div>
        <div className="discovery-header-actions">
          <button
            className="action-btn-primary"
            onClick={() => onCreateAction?.(discovery)}
            disabled={!onCreateAction}
          >
            <span>+</span> Create Action Item
          </button>
          {/* Close button hidden in popover mode - parent provides it */}
          {mode !== 'popover' && (
            <button className="discovery-close-btn" onClick={onClose}>×</button>
          )}
        </div>
      </div>

      {/* FRAUD WARNING - TOP PRIORITY (moved to top) */}
      {hasFraudIndicators && (
        <div className="fraud-alert-banner top-banner">
          <span className="fraud-icon">⚠</span>
          <span className="fraud-text">Fraud Indicator Detected - Immediate Review Required</span>
        </div>
      )}

      <div className="discovery-detail-body">

        {/* Compact Summary Strip - Horizontal badges */}
        <div className="summary-strip">
          <div className="summary-badge">
            <span className="badge-label">Module</span>
            <span className={`badge-value module-${discovery.module.toLowerCase()}`}>{discovery.module}</span>
          </div>
          <div className="summary-badge">
            <span className="badge-label">Severity</span>
            <span className={`badge-value severity-${discovery.severity.toLowerCase()}`}>{discovery.severity}</span>
          </div>
          <div className="summary-badge">
            <span className="badge-label">Records</span>
            <span className="badge-value">{formatNumber(discovery.records_affected || discovery.unique_entities || discovery.discovery_count)}</span>
          </div>
          <div className="summary-badge">
            <span className="badge-label">Period</span>
            <span className="badge-value">{formatPeriod(discovery.period_start, discovery.period_end)}</span>
          </div>
          <div className="summary-badge financial">
            <span className="badge-label">Financial Exposure</span>
            <span className="badge-value">
              {discovery.financial_impact_usd
                ? currencyFormatter.format(parseFloat(discovery.financial_impact_usd))
                : 'N/A'}
            </span>
          </div>
        </div>

        {/* Two-Pane Layout: 2/3 Left, 1/3 Right */}
        <div className="discovery-two-pane">

          {/* LEFT PANE (2/3): Key Findings */}
          <div className="discovery-left-pane">

            {/* Key Findings Table */}
            {discovery.key_findings && discovery.key_findings.length > 0 && (
              <div className="findings-block">
                <h4 className="findings-title">Key Findings</h4>
                <table className="findings-table">
                  <thead>
                    <tr>
                      <th className="col-rank">#</th>
                      <th className="col-finding">Finding</th>
                      <th className="col-category">Category</th>
                    </tr>
                  </thead>
                  <tbody>
                    {discovery.key_findings
                      .sort((a: KeyFinding, b: KeyFinding) => a.finding_rank - b.finding_rank)
                      .map((finding: KeyFinding) => (
                        <tr key={finding.id}>
                          <td className="cell-rank">{finding.finding_rank}</td>
                          <td className="cell-finding">{finding.finding_text}</td>
                          <td className="cell-category">
                            <span className="category-tag">{finding.finding_category || 'General'}</span>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Critical Discovery Text Block - Moved here to fill left pane space */}
            {hasDiscoveries && discovery.discoveries[0]?.description && (
              <div className="critical-discovery-text-block">
                <h4 className="cd-text-title">Critical Discovery</h4>
                <div className="cd-text-content">
                  <h5 className="cd-text-subtitle">{discovery.discoveries[0].title}</h5>
                  <ul className="cd-text-bullets">
                    {(() => {
                      const desc = discovery.discoveries[0].description;
                      // Split on sentence boundaries (period/semicolon followed by space and uppercase)
                      const parts = desc.split(/(?<=[.;])\s+(?=[A-Z])/).filter(p => p.trim().length > 20);
                      return parts.slice(0, 4).map((part, i) => (
                        <li key={i}>{part.trim()}</li>
                      ));
                    })()}
                  </ul>
                </div>
              </div>
            )}
          </div>

          {/* RIGHT PANE (1/3): KPI Metrics + Concentration */}
          <div className="discovery-right-pane">

            {/* Large KPI Metrics */}
            {hasDiscoveries && (
              <div className="kpi-metrics-block">
                <h4 className="kpi-title">Critical Discovery</h4>
                <div className="kpi-subtitle">{discovery.discoveries[0]?.title}</div>
                <div className="kpi-metrics-grid">
                  {(() => {
                    const text = discovery.discoveries[0]?.description || '';
                    const metrics: JSX.Element[] = [];

                    const custMatch = text.match(/(?:shows\s+)?(\d{2,6})\s+customers?\s*\(/i);
                    if (custMatch) {
                      metrics.push(
                        <div key="cust" className="kpi-metric-card">
                          <span className="kpi-metric-value">{formatNumber(custMatch[1])}</span>
                          <span className="kpi-metric-label">CUSTOMERS</span>
                        </div>
                      );
                    }

                    const percMatch = text.match(/\((\d+(?:\.\d+)?)\s*%\s*of/i);
                    if (percMatch) {
                      metrics.push(
                        <div key="perc" className="kpi-metric-card accent">
                          <span className="kpi-metric-value">{percMatch[1]}%</span>
                          <span className="kpi-metric-label">AFFECTED</span>
                        </div>
                      );
                    }

                    const growthMatch = text.match(/(?:averaging|average|avg)\s+(\d+(?:\.\d+)?)\s*%/i);
                    if (growthMatch) {
                      metrics.push(
                        <div key="growth" className="kpi-metric-card">
                          <span className="kpi-metric-value">{growthMatch[1]}%</span>
                          <span className="kpi-metric-label">AVG GROWTH</span>
                        </div>
                      );
                    }

                    // Fallback if no regex matched - use key_findings count (Issue 5 fix)
                    if (metrics.length === 0) {
                      const findingsCount = discovery.key_findings?.length || discovery.discovery_count || 0;
                      metrics.push(
                        <div key="count" className="kpi-metric-card">
                          <span className="kpi-metric-value">{formatNumber(findingsCount)}</span>
                          <span className="kpi-metric-label">FINDINGS</span>
                        </div>
                      );
                      if (discovery.risk_score) {
                        metrics.push(
                          <div key="risk" className="kpi-metric-card accent">
                            <span className="kpi-metric-value">{discovery.risk_score}</span>
                            <span className="kpi-metric-label">RISK SCORE</span>
                          </div>
                        );
                      }
                    }

                    return metrics;
                  })()}
                </div>
                {/* KPI Explanations - Issue 4 fix: Clear and specific explanations */}
                <div className="kpi-explanations">
                  <p><strong>FINDINGS:</strong> Key findings identified from alert analysis</p>
                  <p><strong>RISK SCORE:</strong> Risk score (0-100) based on severity + financial impact + fraud indicators</p>
                </div>
              </div>
            )}

            {/* Concentration Pattern Table */}
            {discovery.concentration_metrics && discovery.concentration_metrics.length > 0 && (
              <div className="concentration-block">
                <h4 className="concentration-title">Concentration Pattern</h4>
                <table className="concentration-table">
                  <thead>
                    <tr>
                      <th>Entity</th>
                      <th>Records</th>
                      <th>% Share</th>
                    </tr>
                  </thead>
                  <tbody>
                    {discovery.concentration_metrics
                      .sort((a, b) => (a.rank || 999) - (b.rank || 999))
                      .slice(0, 6)
                      .map((metric: ConcentrationMetric, index: number) => (
                        <tr key={metric.id || index}>
                          <td className="entity-cell">{metric.dimension_name || metric.dimension_code}</td>
                          <td className="number-cell">{formatNumber(metric.record_count)}</td>
                          <td className="percent-cell">
                            <span className="percent-value">{formatNumber(metric.percentage_of_total)}%</span>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
                {/* Concentration Explanation */}
                <div className="concentration-explanation">
                  <p>
                    <strong>What this shows:</strong> Distribution of flagged records across organizational units (company codes).
                    High concentration in a single entity may indicate localized control weaknesses or targeted fraud schemes.
                  </p>
                  <p className="concentration-insight">
                    {discovery.concentration_metrics[0] &&
                      `${discovery.concentration_metrics[0].dimension_name || discovery.concentration_metrics[0].dimension_code}
                       has the highest concentration with ${formatNumber(discovery.concentration_metrics[0].record_count)} records
                       (${formatNumber(discovery.concentration_metrics[0].percentage_of_total)}% of total).`
                    }
                  </p>
                </div>
              </div>
            )}

          </div>
        </div>

      </div>
    </div>
  );

  // Popover mode: just return content (parent handles container)
  if (mode === 'popover') {
    return content;
  }

  // Modal mode: overlay with centered modal
  if (mode === 'modal') {
    return (
      <div className="discovery-modal-overlay" onClick={onClose}>
        <div className="discovery-modal" onClick={(e) => e.stopPropagation()}>
          {content}
        </div>
      </div>
    );
  }

  // Inline mode: just return content
  return content;
};

export default DiscoveryDetailPanel;
