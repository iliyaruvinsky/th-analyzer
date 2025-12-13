import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3011/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface DataSource {
  id: number;
  filename: string;
  file_format: string;
  data_type: string;
  status: string;
  created_at: string;
}

export interface Finding {
  id: number;
  title: string;
  description: string;
  severity: string;
  status: string;
  focus_area: {
    code: string;
    name: string;
  };
  issue_type?: {
    code: string;
    name: string;
  };
  risk_assessment?: {
    risk_score: number;
    risk_level: string;
  };
  money_loss_calculation?: {
    estimated_loss: number;
    confidence: number;
  };
  detected_at: string;
}

export interface AnalysisRun {
  id: number;
  data_source_id: number;
  status: string;
  total_findings: number;
  findings_by_focus_area: Record<string, number>;
  total_risk_score: number;
  total_money_loss: number;
  started_at: string;
  completed_at?: string;
}

export const getDataSources = async (): Promise<DataSource[]> => {
    const response = await apiClient.get('/ingestion/data-sources');
    return response.data;
};

export const uploadFile = async (file: File): Promise<DataSource> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/ingestion/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
};

export const runAnalysis = async (dataSourceId: number): Promise<AnalysisRun> => {
    const response = await apiClient.post('/analysis/run', {
      data_source_id: dataSourceId,
    });
    return response.data;
};

export const getAnalysisRuns = async (): Promise<AnalysisRun[]> => {
    const response = await apiClient.get('/analysis/runs');
    return response.data;
};

export const getAnalysisRun = async (runId: number): Promise<AnalysisRun> => {
    const response = await apiClient.get(`/analysis/runs/${runId}`);
    return response.data;
};

export const getFindings = async (params?: {
    focus_area?: string;
    severity?: string;
    status?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<Finding[]> => {
    const response = await apiClient.get('/analysis/findings', { params });
    return response.data;
};

export const getMaintenanceDataSources = async (): Promise<any[]> => {
    const response = await apiClient.get('/maintenance/data-sources');
    return response.data;
};

export const deleteDataSource = async (id: number): Promise<any> => {
    const response = await apiClient.delete(`/maintenance/data-sources/${id}`);
    return response.data;
};

export const deleteAllDataSources = async (confirm: boolean): Promise<any> => {
    const response = await apiClient.delete('/maintenance/data-sources', {
      params: { confirm },
    });
    return response.data;
};

export const getAuditLogs = async (params?: {
    action?: string;
    entity_type?: string;
    status?: string;
  }): Promise<any[]> => {
    const response = await apiClient.get('/maintenance/logs', { params });
    return response.data;
};

export const getKpiSummary = async (): Promise<{
    total_findings: number;
    total_risk_score: number;
    total_money_loss: number;
    analysis_runs: number;
}> => {
    const { data } = await apiClient.get('/dashboard/kpis');
    return data;
};

// Content Analysis API Types
export interface AlertFolder {
  path: string;
  alert_id: string;
  alert_name: string;
  module: string;
  has_code: boolean;
  has_explanation: boolean;
  has_metadata: boolean;
  has_summary: boolean;
  is_complete: boolean;
}

export interface ScanFoldersResponse {
  folders: AlertFolder[];
  total: number;
  complete: number;
  incomplete: number;
}

export interface AnalyzeAndSaveResponse {
  finding_id: number;
  message: string;
  focus_area: string;
  severity: string;
  risk_score: number;
  money_loss_estimate: number;
  markdown_path?: string;
  report_level: string;
}

export interface BatchJobResponse {
  job_id: string;
  message: string;
  total_alerts: number;
}

export interface BatchStatusResponse {
  job_id: string;
  status: string;
  total: number;
  completed: number;
  failed: number;
  results: Array<{
    directory: string;
    alert_name: string;
    status: string;
    finding_id?: number;
    error?: string;
  }>;
}

// Content Analysis API Functions
export const scanFolders = async (basePath: string, recursive = true): Promise<ScanFoldersResponse> => {
  const response = await apiClient.post('/content-analysis/scan-folders', {
    base_path: basePath,
    recursive,
  });
  return response.data;
};

export const analyzeAndSave = async (
  directoryPath: string,
  reportLevel: 'summary' | 'full' = 'summary',
  useLlm = true
): Promise<AnalyzeAndSaveResponse> => {
  const response = await apiClient.post('/content-analysis/analyze-and-save', {
    directory_path: directoryPath,
    report_level: reportLevel,
    use_llm: useLlm,
  });
  return response.data;
};

export const analyzeBatch = async (
  directoryPaths: string[],
  reportLevel: 'summary' | 'full' = 'summary'
): Promise<BatchJobResponse> => {
  const response = await apiClient.post('/content-analysis/analyze-batch', {
    directory_paths: directoryPaths,
    report_level: reportLevel,
  });
  return response.data;
};

export const getBatchStatus = async (jobId: string): Promise<BatchStatusResponse> => {
  const response = await apiClient.get(`/content-analysis/batch-status/${jobId}`);
  return response.data;
};

export const getBatchJobs = async (): Promise<BatchJobResponse[]> => {
  const response = await apiClient.get('/content-analysis/batch-jobs');
  return response.data;
};

// =============================================================================
// Alert Dashboard API Types
// =============================================================================

export interface AlertDashboardKPIs {
  total_critical_discoveries: number;
  total_alerts_analyzed: number;
  total_financial_exposure_usd: string;
  avg_risk_score: number;
  alerts_by_severity: Record<string, number>;
  alerts_by_focus_area: Record<string, number>;
  alerts_by_module: Record<string, number>;
  open_investigations: number;
  open_action_items: number;
}

export interface CriticalDiscovery {
  id: number;
  alert_analysis_id: number;
  discovery_order: number;
  title: string;
  description: string;
  affected_entity?: string;
  affected_entity_id?: string;
  metric_value?: string;
  metric_unit?: string;
  percentage_of_total?: string;
  is_fraud_indicator: boolean;
  created_at: string;
}

export interface ConcentrationMetric {
  id: number;
  alert_analysis_id: number;
  dimension_type: string;
  dimension_code: string;
  dimension_name?: string;
  record_count?: number;
  value_local?: string;
  value_usd?: string;
  percentage_of_total?: string;
  rank?: number;
  created_at: string;
}

export interface KeyFinding {
  id: number;
  alert_analysis_id: number;
  finding_rank: number;
  finding_text: string;
  finding_category?: string;
  financial_impact_usd?: string;
  created_at: string;
}

export interface CriticalDiscoveryDrilldown {
  alert_id: string;
  alert_name: string;
  module: string;
  focus_area: string;
  severity: string;
  discovery_count: number;
  financial_impact_usd?: string;
  discoveries: CriticalDiscovery[];
  concentration_metrics?: ConcentrationMetric[];
  key_findings?: KeyFinding[];
  // Summary Data fields from AlertAnalysis
  records_affected?: number;
  unique_entities?: number;
  period_start?: string;
  period_end?: string;
  risk_score?: number;
  raw_summary_data?: Record<string, unknown>;
  // Alert configuration from AlertInstance
  business_purpose?: string;  // From Explanation_* file
  parameters?: Record<string, unknown>;  // From Metadata_* file
}

export interface ActionItem {
  id: number;
  alert_analysis_id: number;
  action_type: string;
  priority?: number;
  title: string;
  description?: string;
  status: string;
  assigned_to?: string;
  due_date?: string;
  resolution_notes?: string;
  resolved_at?: string;
  resolved_by?: string;
  created_at: string;
  finding_id?: number;
}

export interface ActionItemCreate {
  alert_analysis_id: number;
  action_type: string;
  priority?: number;
  title: string;
  description?: string;
  status?: string;
  assigned_to?: string;
  due_date?: string;
}

export interface AlertAnalysisSummary {
  id: number;
  alert_instance_id: number;
  analysis_type: string;
  execution_date: string;
  severity: string;
  risk_score?: number;
  fraud_indicator?: string;
  financial_impact_usd?: string;
  created_at: string;
}

export interface Client {
  id: number;
  code: string;
  name: string;
  description?: string;
  website?: string;
  created_at: string;
}

export interface ExceptionIndicator {
  id: number;
  ei_id: string;
  function_name?: string;
  module: string;
  category?: string;
  created_at: string;
}

// =============================================================================
// Alert Dashboard API Functions
// =============================================================================

export const getAlertDashboardKPIs = async (): Promise<AlertDashboardKPIs> => {
  const response = await apiClient.get('/alert-dashboard/kpis');
  return response.data;
};

export const getCriticalDiscoveries = async (limit = 10): Promise<CriticalDiscoveryDrilldown[]> => {
  const response = await apiClient.get('/alert-dashboard/critical-discoveries', {
    params: { limit },
  });
  return response.data;
};

export const getActionQueue = async (status = 'OPEN', limit = 50): Promise<ActionItem[]> => {
  const response = await apiClient.get('/alert-dashboard/action-queue', {
    params: { status, limit },
  });
  return response.data;
};

// Alias for Dashboard.tsx compatibility
export const getActionItems = getActionQueue;

export const getAlertAnalyses = async (params?: {
  focus_area?: string;
  severity?: string;
  analysis_type?: string;
  skip?: number;
  limit?: number;
}): Promise<AlertAnalysisSummary[]> => {
  const response = await apiClient.get('/alert-dashboard/analyses', { params });
  return response.data;
};

export const getClients = async (): Promise<Client[]> => {
  const response = await apiClient.get('/alert-dashboard/clients');
  return response.data;
};

export const getExceptionIndicators = async (module?: string): Promise<ExceptionIndicator[]> => {
  const response = await apiClient.get('/alert-dashboard/exception-indicators', {
    params: module ? { module } : {},
  });
  return response.data;
};

export const createActionItem = async (actionItem: ActionItemCreate): Promise<ActionItem> => {
  const response = await apiClient.post('/alert-dashboard/action-items', actionItem);
  return response.data;
};

export const updateActionItem = async (
  itemId: number,
  update: Partial<ActionItem>
): Promise<ActionItem> => {
  const response = await apiClient.patch(`/alert-dashboard/action-items/${itemId}`, update);
  return response.data;
};

// Delete Response Interface
export interface DeleteResponse {
  success: boolean;
  message: string;
  deleted_records?: Record<string, number>;
}

// Deletion API Functions
export const deleteAlertAnalysis = async (analysisId: number): Promise<DeleteResponse> => {
  const response = await apiClient.delete(`/alert-dashboard/analyses/${analysisId}`);
  return response.data;
};

export const deleteAlertInstance = async (alertInstanceId: number): Promise<DeleteResponse> => {
  const response = await apiClient.delete(`/alert-dashboard/alert-instances/${alertInstanceId}`);
  return response.data;
};

export const deleteAlertInstanceByAlertId = async (alertId: string): Promise<DeleteResponse> => {
  const response = await apiClient.delete(`/alert-dashboard/alert-instances/by-alert-id/${alertId}`);
  return response.data;
};

export const deleteAllAlertInstances = async (): Promise<DeleteResponse> => {
  const response = await apiClient.delete('/alert-dashboard/alert-instances', {
    params: { confirm: true },
  });
  return response.data;
};

export const deleteCriticalDiscovery = async (discoveryId: number): Promise<DeleteResponse> => {
  const response = await apiClient.delete(`/alert-dashboard/discoveries/${discoveryId}`);
  return response.data;
};

// Maintain backwards compatibility for existing imports
export const api = {
    getDataSources,
    uploadFile,
    runAnalysis,
    getAnalysisRuns,
    getAnalysisRun,
    getFindings,
    getMaintenanceDataSources,
    deleteDataSource,
    deleteAllDataSources,
    getAuditLogs,
    getKpiSummary,
    // Content Analysis
    scanFolders,
    analyzeAndSave,
    analyzeBatch,
    getBatchStatus,
    getBatchJobs,
    // Alert Dashboard
    getAlertDashboardKPIs,
    getCriticalDiscoveries,
    getActionQueue,
    getActionItems,
    getAlertAnalyses,
    getClients,
    getExceptionIndicators,
    // Action Items
    createActionItem,
    updateActionItem,
    // Deletion
    deleteAlertAnalysis,
    deleteAlertInstance,
    deleteAlertInstanceByAlertId,
    deleteAllAlertInstances,
    deleteCriticalDiscovery,
};

