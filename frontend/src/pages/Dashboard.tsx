import React, { useState, useEffect, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getFindings, getAnalysisRuns, getKpiSummary } from '../services/api';
import FocusAreaChart from '../components/charts/FocusAreaChart';
import RiskLevelChart from '../components/charts/RiskLevelChart';
import MoneyLossChart from '../components/charts/MoneyLossChart';
import FindingsTable from '../components/tables/FindingsTable';
import DashboardFilters, { FilterState } from '../components/filters/DashboardFilters';
import KpiCard from '../components/KpiCard';
import { useNavigate } from 'react-router-dom';
import '../styles/dashboard.css';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<FilterState>({
    focusArea: '',
    severity: '',
    status: '',
    dateFrom: '',
    dateTo: '',
  });

  const { data: kpiData, isLoading: isLoadingKpis, error: kpiError } = useQuery({
    queryKey: ['kpiSummary'],
    queryFn: getKpiSummary,
    refetchOnWindowFocus: true,
    refetchInterval: 5000,
  });

  const { data: findings, isLoading: isLoadingFindings, error: findingsError, refetch: refetchFindings } = useQuery({
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
    onError: (error) => {
      console.error('Failed to load findings:', error);
    },
  });

  const { data: analysisRuns, isLoading: runsLoading, error: runsError, refetch: refetchRuns } = useQuery({
    queryKey: ['analysisRuns'],
    queryFn: getAnalysisRuns,
    retry: 1,
    refetchOnWindowFocus: true,
    refetchInterval: 5000,
    onError: (error) => {
      console.error('Failed to load analysis runs:', error);
    },
  });

  const latestRun = analysisRuns?.[0];

  // Debug logging
  useEffect(() => {
    if (findings) {
      console.log('Findings loaded:', findings.length);
      const withRisk = findings.filter(f => f.risk_assessment).length;
      const withMoney = findings.filter(f => f.money_loss_calculation).length;
      console.log('Findings with risk_assessment:', withRisk);
      console.log('Findings with money_loss_calculation:', withMoney);

      const totalRisk = findings.reduce((sum, f) => {
        const score = f.risk_assessment?.risk_score || 0;
        return sum + (typeof score === 'number' ? score : 0);
      }, 0);
      const totalMoney = findings.reduce((sum, f) => {
        const loss = f.money_loss_calculation?.estimated_loss || 0;
        return sum + (typeof loss === 'number' ? loss : 0);
      }, 0);
      console.log('Calculated Total Risk Score:', totalRisk);
      console.log('Calculated Total Money Loss:', totalMoney);
    }
  }, [findings]);

  // Totals from the new KPI endpoint
  const totalFindings = kpiData?.total_findings ?? 0;
  const totalRiskScore = kpiData?.total_risk_score ?? 0;
  const totalMoneyLoss = kpiData?.total_money_loss ?? 0;
  const totalAnalysisRuns = kpiData?.analysis_runs ?? 0;

  const numberFormatter = useMemo(
    () => new Intl.NumberFormat('en-US'),
    []
  );
  const currencyFormatter = useMemo(
    () =>
      new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0,
      }),
    []
  );

  // Aggregate data for charts - use findings data instead of just latest run
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
    ?.map((f: any) => ({
      date: f.detected_at,
      amount: f.money_loss_calculation?.estimated_loss || 0,
    }))
    .filter((d: { amount: number }) => d.amount > 0)
    .sort((a: { date: string }, b: { date: string }) =>
      new Date(a.date).getTime() - new Date(b.date).getTime()
    ) || [];

  const handleFilterChange = (newFilters: Partial<FilterState>) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
  };

  const handleFindingClick = (finding: any) => {
    navigate(`/findings/${finding.id}`);
  };

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
          <p className="alert-endpoint">Expected: http://localhost:8080</p>
          <p className="alert-error">{kpiError?.message || findingsError?.message || runsError?.message || 'Unknown error'}</p>
          <button className="alert-retry" onClick={() => window.location.reload()}>
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="command-center">
      {/* Scan line effect */}
      <div className="scan-line"></div>

      {/* Header */}
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

      {/* KPI Grid - Asymmetric layout */}
      <div className="kpi-grid">
        {/* Total Findings KPI */}
        <KpiCard
          icon="⬢"
          label="TOTAL FINDINGS"
          value={numberFormatter.format(totalFindings)}
          variant="featured"
          glowColor="cyan"
          animationDelay="0.1s"
          alertNames={findings?.map((f: any) => f.title) || []}
          helpTitle="Total Findings"
          helpContent={
            <div>
              <p>Total number of unique findings detected across all uploaded data sources.</p>
              <h4>What are Findings?</h4>
              <p>Each finding represents an alert from the 4C system that has been analyzed for risk and financial impact.</p>
            </div>
          }
          details={findings?.map((f: any) => ({
            label: f.title,
            value: f.severity || 'N/A',
          })).slice(0, 10)}
        />

        {/* Risk Score KPI */}
        <KpiCard
          icon="▲"
          label="RISK SCORE"
          value={numberFormatter.format(totalRiskScore)}
          trend={{ icon: '↑', text: 'ELEVATED' }}
          variant="danger"
          glowColor="red"
          animationDelay="0.2s"
          alertNames={findings?.map((f: any) => f.title) || []}
          helpTitle="Risk Score Calculation"
          helpContent={
            <div>
              <p>Combined risk score from all findings, calculated using a 5-factor model:</p>
              <h4>Scoring Formula</h4>
              <p><code>Score = (F1 + F2 + F3 + F5) × F4</code></p>
              <h4>Factors</h4>
              <ul>
                <li><strong>F1 - Severity Base:</strong> Critical=90, High=75, Medium=60, Low=50</li>
                <li><strong>F2 - Count:</strong> Daily rate normalized by BACKDAYS (+0 to +15)</li>
                <li><strong>F3 - Money:</strong> $1M+=20, $100K+=15, $10K+=10, $1K+=5</li>
                <li><strong>F4 - Focus Area:</strong> BUSINESS_PROTECTION ×1.2</li>
                <li><strong>F5 - Patterns:</strong> Concentration & threshold violations (+0 to +15)</li>
              </ul>
              <h4>Risk Levels</h4>
              <ul>
                <li><strong>Critical:</strong> 76-100</li>
                <li><strong>High:</strong> 51-75</li>
                <li><strong>Medium:</strong> 26-50</li>
                <li><strong>Low:</strong> 0-25</li>
              </ul>
            </div>
          }
          details={findings?.map((f: any) => ({
            label: f.title,
            value: f.risk_assessment?.risk_score || 0,
            description: f.risk_assessment?.risk_level,
          })).slice(0, 10)}
        />

        {/* Financial Exposure KPI */}
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
          helpContent={
            <div>
              <p>Total estimated financial exposure from all findings.</p>
              <h4>Data Source</h4>
              <p>Monetary amounts are extracted <strong>only from Summary_* files</strong> (actual alert output data).</p>
              <h4>Important Notes</h4>
              <ul>
                <li>Values represent potential exposure, not confirmed losses</li>
                <li>Amounts may be balances at risk, not actual fraud</li>
                <li>Review individual findings for context</li>
              </ul>
            </div>
          }
          details={findings?.filter((f: any) => f.money_loss_calculation?.estimated_loss > 0).map((f: any) => ({
            label: f.title,
            value: currencyFormatter.format(f.money_loss_calculation?.estimated_loss || 0),
          })).slice(0, 10)}
        />

        {/* Analysis Runs KPI */}
        <KpiCard
          icon="◉"
          label="ANALYSIS RUNS"
          value={numberFormatter.format(totalAnalysisRuns)}
          trend={{ icon: '→', text: 'ACTIVE' }}
          variant="info"
          glowColor="blue"
          animationDelay="0.4s"
          helpTitle="Analysis Runs"
          helpContent={
            <div>
              <p>Total number of analysis processes that have been executed.</p>
              <h4>Analysis Process</h4>
              <ul>
                <li>Upload 4 artifact files (Code, Explanation, Metadata, Summary)</li>
                <li>System classifies into Focus Area</li>
                <li>Extracts quantitative data from Summary</li>
                <li>Calculates risk score and severity</li>
                <li>Saves finding to database</li>
              </ul>
            </div>
          }
        />
      </div>

      {/* Filters */}
      <div className="filter-panel" style={{ animationDelay: '0.5s' }}>
        <DashboardFilters filters={filters} onFilterChange={handleFilterChange} />
      </div>

      {/* Charts Section */}
      <div className="charts-grid" style={{ animationDelay: '0.6s' }}>
        <div className="chart-panel">
          <div className="panel-header">
            <span className="panel-icon">◐</span>
            <h3 className="panel-title">Focus Area Distribution</h3>
          </div>
          <div className="panel-body">
            <FocusAreaChart data={focusAreaData} />
          </div>
          <div className="panel-grid"></div>
        </div>

        <div className="chart-panel">
          <div className="panel-header">
            <span className="panel-icon">◪</span>
            <h3 className="panel-title">Risk Level Analysis</h3>
          </div>
          <div className="panel-body">
            <RiskLevelChart data={riskLevelData} />
          </div>
          <div className="panel-grid"></div>
        </div>
      </div>

      {/* Money Loss Timeline */}
      {moneyLossData.length > 0 && (
        <div className="timeline-panel" style={{ animationDelay: '0.7s' }}>
          <div className="panel-header">
            <span className="panel-icon">▬</span>
            <h3 className="panel-title">Financial Exposure Timeline</h3>
          </div>
          <div className="panel-body">
            <MoneyLossChart data={moneyLossData} />
          </div>
          <div className="panel-grid"></div>
        </div>
      )}

      {/* Findings Table */}
      <div className="findings-panel" style={{ animationDelay: '0.8s' }}>
        <div className="panel-header">
          <div className="panel-header-left">
            <span className="panel-icon">▦</span>
            <h3 className="panel-title">Security Findings</h3>
          </div>
          <button
            className="action-button primary"
            onClick={() => navigate('/reports')}
          >
            <span className="button-icon">◈</span>
            Generate Report
          </button>
        </div>
        <div className="panel-body">
          <FindingsTable
            data={findings || []}
            onRowClick={handleFindingClick}
          />
        </div>
        <div className="panel-grid"></div>
      </div>
    </div>
  );
};

export default Dashboard;
