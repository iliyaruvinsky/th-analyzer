import React, { useState, useEffect } from 'react';
import {
  AlertFolder,
  ScanFoldersResponse,
  BatchStatusResponse,
  scanFolders,
  analyzeAndSave,
  analyzeBatch,
  getBatchStatus,
} from '../services/api';
import './AlertAnalysis.css';

interface AnalysisResult {
  alertName: string;
  status: 'success' | 'error' | 'pending';
  findingId?: number;
  error?: string;
}

const AlertAnalysis: React.FC = () => {
  const [basePath, setBasePath] = useState('docs/skywind-4c-alerts-output');
  const [folders, setFolders] = useState<AlertFolder[]>([]);
  const [selectedFolders, setSelectedFolders] = useState<Set<string>>(new Set());
  const [reportLevel, setReportLevel] = useState<'summary' | 'full'>('summary');
  const [isScanning, setIsScanning] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [scanError, setScanError] = useState<string | null>(null);
  const [analysisResults, setAnalysisResults] = useState<AnalysisResult[]>([]);
  const [batchJobId, setBatchJobId] = useState<string | null>(null);
  const [batchStatus, setBatchStatus] = useState<BatchStatusResponse | null>(null);
  const [stats, setStats] = useState({ total: 0, complete: 0, incomplete: 0 });
  const [moduleFilter, setModuleFilter] = useState<string>('all');

  // Get unique modules for filtering
  const modules = ['all', ...new Set(folders.map(f => f.module))];

  // Filter folders by module
  const filteredFolders = moduleFilter === 'all'
    ? folders
    : folders.filter(f => f.module === moduleFilter);

  // Get module badge class
  const getModuleBadgeClass = (module: string): string => {
    const mod = module.toLowerCase();
    if (mod === 'fi') return 'aa-badge aa-badge--fi';
    if (mod === 'mm') return 'aa-badge aa-badge--mm';
    if (mod === 'sd') return 'aa-badge aa-badge--sd';
    if (mod === 'hr') return 'aa-badge aa-badge--hr';
    return 'aa-badge';
  };

  // Scan for alert folders
  const handleScan = async () => {
    setIsScanning(true);
    setScanError(null);
    setFolders([]);
    setSelectedFolders(new Set());

    try {
      const result: ScanFoldersResponse = await scanFolders(basePath, true);
      setFolders(result.folders);
      setStats({
        total: result.total,
        complete: result.complete,
        incomplete: result.incomplete,
      });
    } catch (error: any) {
      setScanError(error.response?.data?.detail || 'Failed to scan folders');
    } finally {
      setIsScanning(false);
    }
  };

  // Toggle folder selection
  const toggleSelection = (path: string) => {
    const newSelection = new Set(selectedFolders);
    if (newSelection.has(path)) {
      newSelection.delete(path);
    } else {
      newSelection.add(path);
    }
    setSelectedFolders(newSelection);
  };

  // Select all filtered folders
  const selectAll = () => {
    const newSelection = new Set(filteredFolders.map(f => f.path));
    setSelectedFolders(newSelection);
  };

  // Clear selection
  const clearSelection = () => {
    setSelectedFolders(new Set());
  };

  // Analyze single alert
  const handleAnalyzeSingle = async (folder: AlertFolder) => {
    setIsAnalyzing(true);
    setAnalysisResults([{ alertName: folder.alert_name, status: 'pending' }]);

    try {
      const result = await analyzeAndSave(folder.path, reportLevel);
      setAnalysisResults([{
        alertName: folder.alert_name,
        status: 'success',
        findingId: result.finding_id,
      }]);
    } catch (error: any) {
      setAnalysisResults([{
        alertName: folder.alert_name,
        status: 'error',
        error: error.response?.data?.detail || 'Analysis failed',
      }]);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Analyze selected alerts in batch
  const handleBatchAnalysis = async () => {
    if (selectedFolders.size === 0) return;

    setIsAnalyzing(true);
    setAnalysisResults([]);
    setBatchStatus(null);

    try {
      const paths = Array.from(selectedFolders);
      const result = await analyzeBatch(paths, reportLevel);
      setBatchJobId(result.job_id);

      // Initialize results as pending
      const initialResults = paths.map(path => {
        const folder = folders.find(f => f.path === path);
        return {
          alertName: folder?.alert_name || path,
          status: 'pending' as const,
        };
      });
      setAnalysisResults(initialResults);
    } catch (error: any) {
      setScanError(error.response?.data?.detail || 'Batch analysis failed to start');
      setIsAnalyzing(false);
    }
  };

  // Poll batch status
  useEffect(() => {
    if (!batchJobId || !isAnalyzing) return;

    const pollInterval = setInterval(async () => {
      try {
        const status = await getBatchStatus(batchJobId);
        setBatchStatus(status);

        // Update results
        const updatedResults: AnalysisResult[] = status.results.map(r => ({
          alertName: r.alert_name,
          status: r.status === 'completed' ? 'success' : r.status === 'failed' ? 'error' : 'pending',
          findingId: r.finding_id,
          error: r.error,
        }));
        setAnalysisResults(updatedResults);

        // Stop polling when complete
        if (status.status === 'completed' || status.status === 'failed') {
          setIsAnalyzing(false);
          clearInterval(pollInterval);
        }
      } catch (error) {
        console.error('Failed to poll batch status:', error);
      }
    }, 2000);

    return () => clearInterval(pollInterval);
  }, [batchJobId, isAnalyzing]);

  return (
    <div className="aa-container">
      {/* Header */}
      <header className="aa-header">
        <h1 className="aa-title">
          <span className="aa-title-icon">⚡</span>
          Alert Analysis Pipeline
        </h1>
        <span className="aa-subtitle">Skywind 4C Alert Processing</span>
        <div className="aa-status-indicator">
          <span className="aa-status-dot"></span>
          <span className="aa-status-text">System Ready</span>
        </div>
      </header>

      {/* Panel 1: Scan */}
      <section className="aa-panel">
        <div className="aa-panel-header">
          <span className="aa-panel-step">1</span>
          <h2 className="aa-panel-title">Scan for Alerts</h2>
        </div>
        <div className="aa-panel-content">
          <div className="aa-input-row">
            <div className="aa-input-wrapper">
              <span className="aa-input-label">Base Path</span>
              <input
                type="text"
                className="aa-input"
                value={basePath}
                onChange={(e) => setBasePath(e.target.value)}
                placeholder="Enter directory path to scan..."
              />
            </div>
            <button
              className="aa-btn aa-btn-primary"
              onClick={handleScan}
              disabled={isScanning}
            >
              {isScanning ? (
                <>
                  <span className="aa-spinner"></span>
                  Scanning...
                </>
              ) : (
                <>Scan Folders</>
              )}
            </button>
          </div>

          {scanError && (
            <div className="aa-error">
              <span>⚠</span>
              {scanError}
            </div>
          )}

          {stats.total > 0 && (
            <div className="aa-stats-bar">
              <div className="aa-stat">
                <span className="aa-stat-value">{stats.total}</span>
                <span className="aa-stat-label">Total Alerts</span>
              </div>
              <div className="aa-stat aa-stat--success">
                <span className="aa-stat-value">{stats.complete}</span>
                <span className="aa-stat-label">Complete</span>
              </div>
              <div className="aa-stat aa-stat--error">
                <span className="aa-stat-value">{stats.incomplete}</span>
                <span className="aa-stat-label">Incomplete</span>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Panel 2: Select Alerts */}
      {folders.length > 0 && (
        <section className="aa-panel">
          <div className="aa-panel-header">
            <span className="aa-panel-step">2</span>
            <h2 className="aa-panel-title">Select Alerts to Analyze</h2>
          </div>
          <div className="aa-panel-content">
            {/* Toolbar */}
            <div className="aa-toolbar">
              <select
                className="aa-select"
                value={moduleFilter}
                onChange={(e) => setModuleFilter(e.target.value)}
              >
                {modules.map(m => (
                  <option key={m} value={m}>
                    {m === 'all' ? 'All Modules' : m.toUpperCase()}
                  </option>
                ))}
              </select>

              <div className="aa-toolbar-divider"></div>

              <button
                className="aa-btn aa-btn-success aa-btn-small"
                onClick={selectAll}
              >
                Select All ({filteredFolders.length})
              </button>

              <button
                className="aa-btn aa-btn-secondary aa-btn-small"
                onClick={clearSelection}
              >
                Clear
              </button>

              <div className="aa-selection-count">
                <span>{selectedFolders.size}</span>
                <span>selected</span>
              </div>
            </div>

            {/* Alert Table */}
            <div className="aa-table-container">
              <table className="aa-table">
                <thead>
                  <tr>
                    <th></th>
                    <th>Module</th>
                    <th>Alert Name</th>
                    <th>Alert ID</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredFolders.map(folder => (
                    <tr
                      key={folder.path}
                      className={selectedFolders.has(folder.path) ? 'aa-row-selected' : ''}
                    >
                      <td style={{ textAlign: 'center' }}>
                        <input
                          type="checkbox"
                          className="aa-checkbox"
                          checked={selectedFolders.has(folder.path)}
                          onChange={() => toggleSelection(folder.path)}
                        />
                      </td>
                      <td>
                        <span className={getModuleBadgeClass(folder.module)}>
                          {folder.module}
                        </span>
                      </td>
                      <td>{folder.alert_name}</td>
                      <td>
                        <span className="aa-alert-id">{folder.alert_id}</span>
                      </td>
                      <td>
                        {folder.is_complete ? (
                          <span className="aa-status aa-status--complete">
                            <span className="aa-status-icon"></span>
                            Complete
                          </span>
                        ) : (
                          <span className="aa-status aa-status--incomplete">
                            <span className="aa-status-icon"></span>
                            Incomplete
                          </span>
                        )}
                      </td>
                      <td>
                        <button
                          className="aa-btn aa-btn-secondary aa-btn-small"
                          onClick={() => handleAnalyzeSingle(folder)}
                          disabled={isAnalyzing}
                        >
                          Analyze
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      )}

      {/* Panel 3: Run Analysis */}
      {selectedFolders.size > 0 && (
        <section className="aa-panel">
          <div className="aa-panel-header">
            <span className="aa-panel-step">3</span>
            <h2 className="aa-panel-title">Run Batch Analysis</h2>
          </div>
          <div className="aa-panel-content">
            <div className="aa-options-row">
              <div className="aa-option-group">
                <span className="aa-option-label">Report Level</span>
                <select
                  className="aa-select"
                  value={reportLevel}
                  onChange={(e) => setReportLevel(e.target.value as 'summary' | 'full')}
                >
                  <option value="summary">Summary (Fast, No LLM)</option>
                  <option value="full">Full Report (LLM Generated)</option>
                </select>
              </div>

              <button
                className="aa-btn aa-btn-danger"
                onClick={handleBatchAnalysis}
                disabled={isAnalyzing || selectedFolders.size === 0}
              >
                {isAnalyzing ? (
                  <>
                    <span className="aa-spinner"></span>
                    Processing...
                  </>
                ) : (
                  <>
                    ▶ Analyze {selectedFolders.size} Alerts
                  </>
                )}
              </button>
            </div>

            {/* Progress Bar */}
            {batchStatus && (
              <div className="aa-progress">
                <div className="aa-progress-header">
                  <span className="aa-progress-label">
                    Processing alerts...
                  </span>
                  <span className="aa-progress-value">
                    {batchStatus.completed + batchStatus.failed} / {batchStatus.total}
                    {' '}({Math.round(((batchStatus.completed + batchStatus.failed) / batchStatus.total) * 100)}%)
                  </span>
                </div>
                <div className="aa-progress-track">
                  <div
                    className={`aa-progress-fill ${batchStatus.failed > 0 ? 'aa-progress--warning' : ''}`}
                    style={{
                      width: `${((batchStatus.completed + batchStatus.failed) / batchStatus.total) * 100}%`
                    }}
                  />
                </div>
              </div>
            )}
          </div>
        </section>
      )}

      {/* Panel 4: Results */}
      {analysisResults.length > 0 && (
        <section className="aa-panel">
          <div className="aa-panel-header">
            <span className="aa-panel-step">4</span>
            <h2 className="aa-panel-title">Analysis Results</h2>
          </div>
          <div className="aa-panel-content">
            <table className="aa-results-table">
              <thead>
                <tr>
                  <th>Alert</th>
                  <th>Status</th>
                  <th>Result</th>
                </tr>
              </thead>
              <tbody>
                {analysisResults.map((result, idx) => (
                  <tr key={idx}>
                    <td>{result.alertName}</td>
                    <td>
                      {result.status === 'pending' && (
                        <span className="aa-status aa-status--pending">
                          <span className="aa-spinner"></span>
                          Processing
                        </span>
                      )}
                      {result.status === 'success' && (
                        <span className="aa-status aa-status--success">
                          <span className="aa-status-icon"></span>
                          Success
                        </span>
                      )}
                      {result.status === 'error' && (
                        <span className="aa-status aa-status--error">
                          <span className="aa-status-icon"></span>
                          Failed
                        </span>
                      )}
                    </td>
                    <td>
                      {result.findingId && (
                        <a
                          href={`/findings/${result.findingId}`}
                          className="aa-finding-link"
                        >
                          Finding #{result.findingId} →
                        </a>
                      )}
                      {result.error && (
                        <span style={{ color: 'var(--aa-error)' }}>
                          {result.error}
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </div>
  );
};

export default AlertAnalysis;
