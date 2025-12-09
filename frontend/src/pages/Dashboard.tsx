import React, { useState, useEffect, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getFindings, getAnalysisRuns, getKpiSummary, getCriticalDiscoveries, getActionItems, CriticalDiscoveryDrilldown, ActionItem } from '../services/api';
import FocusAreaChart from '../components/charts/FocusAreaChart';
import RiskLevelChart from '../components/charts/RiskLevelChart';
import MoneyLossChart from '../components/charts/MoneyLossChart';
import FindingsTable from '../components/tables/FindingsTable';
import DashboardFilters, { FilterState } from '../components/filters/DashboardFilters';
import KpiCard from '../components/KpiCard';
import DashboardTabs, { DashboardTabType } from '../components/DashboardTabs';
import DiscoveryDetailPanel from '../components/DiscoveryDetailPanel';
import ActionItemModal from '../components/ActionItemModal';
import { useNavigate } from 'react-router-dom';
import '../styles/dashboard.css';
import './AlertDashboard.css';

// Sort configuration type
type SortField = 'alert_name' | 'module' | 'severity' | 'discovery_count' | 'financial_impact_usd';
type SortDirection = 'asc' | 'desc';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<DashboardTabType>('overview');
  const [filters, setFilters] = useState<FilterState>({
    focusArea: '',
    severity: '',
    status: '',
    dateFrom: '',
    dateTo: '',
  });
  const [selectedDiscovery, setSelectedDiscovery] = useState<CriticalDiscoveryDrilldown | null>(null);
  const [selectedActionItem, setSelectedActionItem] = useState<ActionItem | null>(null);
  const [sortField, setSortField] = useState<SortField>('financial_impact_usd');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');

  // ESC key handler to close discovery popover
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && selectedDiscovery) {
        setSelectedDiscovery(null);
      }
    };
    document.addEventListener('keydown', handleEscKey);
    return () => document.removeEventListener('keydown', handleEscKey);
  }, [selectedDiscovery]);

  const { data: kpiData, isLoading: isLoadingKpis, error: kpiError } = useQuery({
    queryKey: ['kpiSummary'],
    queryFn: getKpiSummary,
    refetchOnWindowFocus: true,
    refetchInterval: 5000,
  });

  const { data: findings, isLoading: isLoadingFindings, error: findingsError } = useQuery({
    queryKey: ['findings', filters],
    queryFn: () =>
      getFindings({
        focus_area: filters.focusArea || undefined,
        severity: filters.severity || undefined,
        status: filters.status || undefined,
        date_from: filters.dateFrom || undefined,
        date_to: filters.dateTo || undefined,
      }),
    retry: 1,
    refetchOnWindowFocus: true,
    refetchInterval: 5000,
  });

  const { data: analysisRuns, isLoading: runsLoading, error: runsError } = useQuery({
    queryKey: ['analysisRuns'],
    queryFn: getAnalysisRuns,
    retry: 1,
    refetchOnWindowFocus: true,
    refetchInterval: 5000,
  });

  const { data: criticalDiscoveries, isLoading: discoveriesLoading } = useQuery({
    queryKey: ['criticalDiscoveries'],
    queryFn: getCriticalDiscoveries,
    retry: 1,
    refetchOnWindowFocus: true,
    refetchInterval: 10000,
    enabled: activeTab === 'alerts',
  });

  const { data: actionItems, isLoading: actionsLoading } = useQuery({
    queryKey: ['actionItems'],
    queryFn: getActionItems,
    retry: 1,
    refetchOnWindowFocus: true,
    refetchInterval: 10000,
    enabled: activeTab === 'actions',
  });

  const latestRun = analysisRuns?.[0];

  const totalFindings = kpiData?.total_findings ?? 0;
  const totalRiskScore = kpiData?.total_risk_score ?? 0;
  const totalMoneyLoss = kpiData?.total_money_loss ?? 0;
  const totalAnalysisRuns = kpiData?.analysis_runs ?? 0;

  const numberFormatter = useMemo(() => new Intl.NumberFormat('en-US'), []);
  const currencyFormatter = useMemo(
    () => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }),
    []
  );

  const focusAreaData = findings?.reduce((acc: Record<string, number>, finding: any) => {
    const code = finding.focus_area?.code || 'UNKNOWN';
    acc[code] = (acc[code] || 0) + 1;
    return acc;
  }, {}) || latestRun?.findings_by_focus_area || {};

  const riskLevelData = findings?.reduce((acc: Record<string, number>, finding: any) => {
    const level = finding.risk_assessment?.risk_level || finding.severity || 'Unknown';
    acc[level] = (acc[level] || 0) + 1;
    return acc;
  }, {}) || {};

  const moneyLossData = findings
    ?.map((f: any) => ({ date: f.detected_at, amount: f.money_loss_calculation?.estimated_loss || 0 }))
    .filter((d: { amount: number }) => d.amount > 0)
    .sort((a: { date: string }, b: { date: string }) => new Date(a.date).getTime() - new Date(b.date).getTime()) || [];

  const handleFilterChange = (newFilters: Partial<FilterState>) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
  };

  const handleFindingClick = (finding: any) => {
    navigate(`/findings/${finding.id}`);
  };

  const handleDiscoveryClick = (discovery: CriticalDiscoveryDrilldown) => {
    setSelectedDiscovery(discovery);
  };

  const handleCloseDiscovery = () => {
    setSelectedDiscovery(null);
  };

  const handleCreateAction = (discovery: CriticalDiscoveryDrilldown) => {
    console.log('Create action for:', discovery.alert_name);
  };

  // Handle column sort
  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  // Severity order for sorting
  const severityOrder: Record<string, number> = { 'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };

  // Sort discoveries
  const sortedDiscoveries = useMemo(() => {
    if (!criticalDiscoveries) return [];

    return [...criticalDiscoveries].sort((a, b) => {
      let comparison = 0;

      switch (sortField) {
        case 'alert_name':
          comparison = a.alert_name.localeCompare(b.alert_name);
          break;
        case 'module':
          comparison = a.module.localeCompare(b.module);
          break;
        case 'severity':
          comparison = (severityOrder[a.severity] || 0) - (severityOrder[b.severity] || 0);
          break;
        case 'discovery_count':
          comparison = a.discovery_count - b.discovery_count;
          break;
        case 'financial_impact_usd':
          const aVal = a.financial_impact_usd ? parseFloat(a.financial_impact_usd) : 0;
          const bVal = b.financial_impact_usd ? parseFloat(b.financial_impact_usd) : 0;
          comparison = aVal - bVal;
          break;
      }

      return sortDirection === 'asc' ? comparison : -comparison;
    });
  }, [criticalDiscoveries, sortField, sortDirection]);

  if (isLoadingKpis || isLoadingFindings || runsLoading) {
    return (
      <div className="excavation-loader">
        <div className="scanner-line"></div>
        <div className="loading-text">
          <span className="glow">Loading Dashboard</span>
          <div className="loading-dots">
            <span style={{ animationDelay: '0s' }}>.</span>
            <span style={{ animationDelay: '0.2s' }}>.</span>
            <span style={{ animationDelay: '0.4s' }}>.</span>
          </div>
        </div>
      </div>
    );
  }

  if (kpiError || findingsError || runsError) {
    return (
      <div className="command-center">
        <div className="system-alert">
          <div className="alert-icon">⚠</div>
          <h2>Connection Error</h2>
          <p className="alert-detail">Unable to connect to the backend API</p>
          <button className="alert-retry" onClick={() => window.location.reload()}>Retry Connection</button>
        </div>
      </div>
    );
  }

  const renderOverviewTab = () => (
    <>
      <div className="kpi-grid">
        <KpiCard
          icon="⬢"
          label="TOTAL FINDINGS"
          value={numberFormatter.format(totalFindings)}
          variant="featured"
          glowColor="cyan"
          animationDelay="0.1s"
          alertNames={findings?.map((f: any) => f.title) || []}
          helpTitle="Total Findings"
          helpContent={<div><p>Total number of unique findings detected across all uploaded data sources.</p></div>}
          details={findings?.map((f: any) => ({ label: f.title, value: f.severity || 'N/A' })).slice(0, 10)}
        />
        <KpiCard
          icon="▲"
          label="RISK SCORE"
          value={numberFormatter.format(totalRiskScore)}
          trend={{ icon: '↑', text: 'ELEVATED' }}
          variant="danger"
          glowColor="red"
          animationDelay="0.2s"
          alertNames={findings?.map((f: any) => f.title) || []}
          helpTitle="Risk Score"
          helpContent={<div><p>Combined risk score from all findings.</p></div>}
          details={findings?.map((f: any) => ({ label: f.title, value: f.risk_assessment?.risk_score || 0 })).slice(0, 10)}
        />
        <KpiCard
          icon="$"
          label="FINANCIAL EXPOSURE"
          value={currencyFormatter.format(totalMoneyLoss)}
          trend={{ icon: '⬤', text: 'MONITORED' }}
          variant="warning"
          glowColor="amber"
          animationDelay="0.3s"
          alertNames={findings?.map((f: any) => f.title) || []}
          helpTitle="Financial Exposure"
          helpContent={<div><p>Total estimated financial exposure from all findings.</p></div>}
          details={findings?.filter((f: any) => f.money_loss_calculation?.estimated_loss > 0).map((f: any) => ({ label: f.title, value: currencyFormatter.format(f.money_loss_calculation?.estimated_loss || 0) })).slice(0, 10)}
        />
        <KpiCard
          icon="◉"
          label="ANALYSIS RUNS"
          value={numberFormatter.format(totalAnalysisRuns)}
          trend={{ icon: '→', text: 'ACTIVE' }}
          variant="info"
          glowColor="blue"
          animationDelay="0.4s"
          helpTitle="Analysis Runs"
          helpContent={<div><p>Total number of analysis processes executed.</p></div>}
        />
      </div>

      <div className="filter-panel" style={{ animationDelay: '0.5s' }}>
        <DashboardFilters filters={filters} onFilterChange={handleFilterChange} />
      </div>

      <div className="charts-grid" style={{ animationDelay: '0.6s' }}>
        <div className="chart-panel">
          <div className="panel-header">
            <span className="panel-icon">◐</span>
            <h3 className="panel-title">Focus Area Distribution</h3>
          </div>
          <div className="panel-body"><FocusAreaChart data={focusAreaData} /></div>
        </div>
        <div className="chart-panel">
          <div className="panel-header">
            <span className="panel-icon">◪</span>
            <h3 className="panel-title">Risk Level Analysis</h3>
          </div>
          <div className="panel-body"><RiskLevelChart data={riskLevelData} /></div>
        </div>
      </div>

      {moneyLossData.length > 0 && (
        <div className="timeline-panel" style={{ animationDelay: '0.7s' }}>
          <div className="panel-header">
            <span className="panel-icon">▬</span>
            <h3 className="panel-title">Financial Exposure Timeline</h3>
          </div>
          <div className="panel-body"><MoneyLossChart data={moneyLossData} /></div>
        </div>
      )}

      <div className="findings-panel" style={{ animationDelay: '0.8s' }}>
        <div className="panel-header">
          <div className="panel-header-left">
            <span className="panel-icon">▦</span>
            <h3 className="panel-title">Security Findings</h3>
          </div>
          <button className="action-button primary" onClick={() => navigate('/reports')}>
            <span className="button-icon">◈</span>Generate Report
          </button>
        </div>
        <div className="panel-body"><FindingsTable data={findings || []} onRowClick={handleFindingClick} /></div>
      </div>
    </>
  );

  const renderAlertsTab = () => {
    // Compute KPI summaries from criticalDiscoveries
    const totalDiscoveries = criticalDiscoveries?.length || 0;
    const totalFinancialImpact = criticalDiscoveries?.reduce((sum, d) =>
      sum + (d.financial_impact_usd ? parseFloat(d.financial_impact_usd) : 0), 0) || 0;

    // Severity breakdown
    const severityCounts = criticalDiscoveries?.reduce((acc, d) => {
      acc[d.severity] = (acc[d.severity] || 0) + 1;
      return acc;
    }, {} as Record<string, number>) || {};

    // Module breakdown
    const moduleCounts = criticalDiscoveries?.reduce((acc, d) => {
      const mod = d.module.split(' ')[0]; // Get first word (FI, MM, SD, etc.)
      acc[mod] = (acc[mod] || 0) + 1;
      return acc;
    }, {} as Record<string, number>) || {};

    // Focus area breakdown
    const areaCounts = criticalDiscoveries?.reduce((acc, d) => {
      const area = d.focus_area || 'Unknown';
      acc[area] = (acc[area] || 0) + 1;
      return acc;
    }, {} as Record<string, number>) || {};

    return (
    <div className="ad-container">
      <div className="ad-section">
        <div className="ad-section-header">
          <div className="ad-header-content">
            <h2 className="ad-section-title">
              <span className="ad-section-icon">⚡</span>
              Critical Discoveries
            </h2>
            <p className="ad-section-description">
              Automated analysis of SAP alerts identifying high-risk patterns, anomalies, and potential compliance issues requiring immediate attention.
            </p>
          </div>
          <span className="ad-hint">{selectedDiscovery ? 'Press ESC or click × to close detail panel' : 'Click a row to view details'}</span>
        </div>

        {/* KPI Summary Cards */}
        {!selectedDiscovery && criticalDiscoveries && criticalDiscoveries.length > 0 && (
          <div className="ad-kpi-grid">
            <div className="ad-kpi-card">
              <div className="ad-kpi-value">{totalDiscoveries}</div>
              <div className="ad-kpi-label">Total Discoveries</div>
            </div>
            <div className="ad-kpi-card financial">
              <div className="ad-kpi-value">{currencyFormatter.format(totalFinancialImpact)}</div>
              <div className="ad-kpi-label">Total Financial Exposure</div>
            </div>
            <div className="ad-kpi-card">
              <div className="ad-kpi-value">
                {Object.entries(severityCounts).map(([sev, count]) => (
                  <span key={sev} className={`ad-kpi-tag severity-${sev.toLowerCase()}`}>{count} {sev}</span>
                ))}
              </div>
              <div className="ad-kpi-label">By Severity</div>
            </div>
            <div className="ad-kpi-card">
              <div className="ad-kpi-value">
                {Object.entries(moduleCounts).slice(0, 4).map(([mod, count]) => (
                  <span key={mod} className="ad-kpi-tag module">{count} {mod}</span>
                ))}
              </div>
              <div className="ad-kpi-label">SAP Modules</div>
            </div>
            <div className="ad-kpi-card">
              <div className="ad-kpi-value">
                {Object.entries(areaCounts).slice(0, 3).map(([area, count]) => (
                  <span key={area} className="ad-kpi-tag area">{count} {area.replace('_', ' ')}</span>
                ))}
              </div>
              <div className="ad-kpi-label">Focus Areas</div>
            </div>
          </div>
        )}

        {discoveriesLoading ? (
          <div className="ad-loading">Loading critical discoveries...</div>
        ) : criticalDiscoveries && criticalDiscoveries.length > 0 ? (
          <div className="critical-discoveries-container">
            {/* Alert List - Compact when popover open */}
            <div className={`critical-discoveries-list ${selectedDiscovery ? 'with-popover' : ''}`}>
              <table className="ad-table">
                <thead>
                  <tr>
                    <th className={`sortable ${sortField === 'alert_name' ? 'sorted' : ''}`} onClick={() => handleSort('alert_name')}>
                      Alert {sortField === 'alert_name' && <span className="sort-indicator">{sortDirection === 'asc' ? '▲' : '▼'}</span>}
                    </th>
                    <th className={`sortable ${sortField === 'module' ? 'sorted' : ''}`} onClick={() => handleSort('module')}>
                      Module {sortField === 'module' && <span className="sort-indicator">{sortDirection === 'asc' ? '▲' : '▼'}</span>}
                    </th>
                    <th className={`sortable ${sortField === 'severity' ? 'sorted' : ''}`} onClick={() => handleSort('severity')}>
                      Severity {sortField === 'severity' && <span className="sort-indicator">{sortDirection === 'asc' ? '▲' : '▼'}</span>}
                    </th>
                    <th className={`sortable ${sortField === 'discovery_count' ? 'sorted' : ''}`} onClick={() => handleSort('discovery_count')}>
                      Discoveries {sortField === 'discovery_count' && <span className="sort-indicator">{sortDirection === 'asc' ? '▲' : '▼'}</span>}
                    </th>
                    <th className={`sortable ${sortField === 'financial_impact_usd' ? 'sorted' : ''}`} onClick={() => handleSort('financial_impact_usd')}>
                      Financial Impact {sortField === 'financial_impact_usd' && <span className="sort-indicator">{sortDirection === 'asc' ? '▲' : '▼'}</span>}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {sortedDiscoveries.map((discovery: CriticalDiscoveryDrilldown) => (
                    <tr
                      key={discovery.id}
                      className={`ad-row ${selectedDiscovery?.id === discovery.id ? 'selected' : ''}`}
                      onClick={() => handleDiscoveryClick(discovery)}
                    >
                      <td>
                        <div className="ad-alert-name">{discovery.alert_name}</div>
                        <div className="ad-alert-id">{discovery.alert_id}</div>
                      </td>
                      <td><span className={`ad-badge module-${discovery.module.toLowerCase()}`}>{discovery.module}</span></td>
                      <td><span className={`ad-badge severity-${discovery.severity.toLowerCase()}`}>{discovery.severity}</span></td>
                      <td><span className="ad-count">{discovery.discovery_count}</span></td>
                      <td><span className="ad-amount">{discovery.financial_impact_usd ? currencyFormatter.format(parseFloat(discovery.financial_impact_usd)) : 'N/A'}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Horizontal Popover - Detail Panel Below */}
            {selectedDiscovery && (
              <div className="discovery-popover">
                <button className="popover-close-btn" onClick={handleCloseDiscovery} title="Close (ESC)">×</button>
                <DiscoveryDetailPanel
                  discovery={selectedDiscovery}
                  mode="popover"
                  onClose={handleCloseDiscovery}
                  currencyFormatter={currencyFormatter}
                  onCreateAction={handleCreateAction}
                />
              </div>
            )}
          </div>
        ) : (
          <div className="ad-empty">No critical discoveries found</div>
        )}
      </div>
    </div>
    );
  };

  const renderActionsTab = () => (
    <div className="ad-container">
      <div className="ad-section">
        <div className="ad-section-header">
          <h2 className="ad-section-title">
            <span className="ad-section-icon">✓</span>
            Action Queue
          </h2>
        </div>

        {actionsLoading ? (
          <div className="ad-loading">Loading action items...</div>
        ) : actionItems && actionItems.length > 0 ? (
          <div className="ad-actions-grid">
            {actionItems.map((item: ActionItem) => (
              <div key={item.id} className={`ad-action-card priority-${item.priority.toLowerCase()}`} onClick={() => setSelectedActionItem(item)}>
                <div className="ad-action-header">
                  <span className={`ad-action-priority priority-${item.priority.toLowerCase()}`}>{item.priority}</span>
                  <span className={`ad-action-status status-${item.status.toLowerCase().replace(' ', '-')}`}>{item.status}</span>
                </div>
                <h3 className="ad-action-title">{item.title}</h3>
                <p className="ad-action-description">{item.description}</p>
                <div className="ad-action-meta">
                  <span className="ad-action-due">{item.due_date ? `Due: ${new Date(item.due_date).toLocaleDateString()}` : 'No due date'}</span>
                  {item.assigned_to && <span className="ad-action-assignee">{item.assigned_to}</span>}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="ad-empty">No action items in queue</div>
        )}
      </div>

      {selectedActionItem && <ActionItemModal actionItem={selectedActionItem} onClose={() => setSelectedActionItem(null)} />}
    </div>
  );

  return (
    <div className="command-center">
      <div className="scan-line"></div>

      <header className="cc-header">
        <div className="header-left">
          <h1 className="cc-title">
            <span className="title-icon">◆</span>
            Treasure Hunt Analyzer
            <span className="title-sub">SAP Security & Compliance Insights</span>
          </h1>
        </div>
        <div className="header-right">
          <div className="status-indicator active">
            <span className="status-dot pulse"></span>
            System Active
          </div>
        </div>
      </header>

      <DashboardTabs activeTab={activeTab} onTabChange={setActiveTab} />

      {activeTab === 'overview' && renderOverviewTab()}
      {activeTab === 'alerts' && renderAlertsTab()}
      {activeTab === 'actions' && renderActionsTab()}
    </div>
  );
};

export default Dashboard;
