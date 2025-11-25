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
};

