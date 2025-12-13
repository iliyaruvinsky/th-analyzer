import React from 'react';
import { CriticalDiscoveryDrilldown } from '../../../../services/api';

interface AlertSummaryProps {
  discoveries: CriticalDiscoveryDrilldown[];
  currencyFormatter: Intl.NumberFormat;
}

const AlertSummary: React.FC<AlertSummaryProps> = ({ discoveries, currencyFormatter }) => {
  // Calculate summary stats
  const totalDiscoveries = discoveries.length;

  const totalFinancialExposure = discoveries.reduce((sum, d) => {
    const val = d.financial_impact_usd ? parseFloat(d.financial_impact_usd) : 0;
    return sum + val;
  }, 0);

  const severityCounts = discoveries.reduce((acc, d) => {
    const sev = d.severity?.toUpperCase() || 'UNKNOWN';
    acc[sev] = (acc[sev] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const moduleCounts = discoveries.reduce((acc, d) => {
    const mod = d.module || 'Unknown';
    acc[mod] = (acc[mod] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Get unique modules
  const modules = Object.keys(moduleCounts).slice(0, 4);

  return (
    <div className="alert-summary-header">
      <h2 className="alert-summary-title">Alert Summary</h2>
      <div className="alert-summary-kpis">
        <div className="summary-kpi">
          <span className="kpi-value">{totalDiscoveries}</span>
          <span className="kpi-label">Total Alerts</span>
        </div>
        <div className="summary-kpi financial">
          <span className="kpi-value">{currencyFormatter.format(totalFinancialExposure)}</span>
          <span className="kpi-label">Financial Exposure</span>
        </div>
        <div className="summary-kpi severity-breakdown">
          <div className="severity-badges">
            {severityCounts.CRITICAL && (
              <span className="severity-badge critical">{severityCounts.CRITICAL} CRIT</span>
            )}
            {severityCounts.HIGH && (
              <span className="severity-badge high">{severityCounts.HIGH} HIGH</span>
            )}
            {severityCounts.MEDIUM && (
              <span className="severity-badge medium">{severityCounts.MEDIUM} MED</span>
            )}
            {severityCounts.LOW && (
              <span className="severity-badge low">{severityCounts.LOW} LOW</span>
            )}
          </div>
          <span className="kpi-label">By Severity</span>
        </div>
        <div className="summary-kpi modules">
          <div className="module-badges">
            {modules.map(mod => (
              <span key={mod} className={`module-badge module-${mod.toLowerCase()}`}>
                {mod} ({moduleCounts[mod]})
              </span>
            ))}
          </div>
          <span className="kpi-label">SAP Modules</span>
        </div>
      </div>
    </div>
  );
};

export default AlertSummary;
