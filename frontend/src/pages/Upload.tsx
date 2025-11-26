import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3011/api/v1';

const Upload: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // Single file upload state
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  // Multi-file artifact upload state
  const [artifactFiles, setArtifactFiles] = useState<File[]>([]);
  const [artifactUploadProgress, setArtifactUploadProgress] = useState(0);
  const [artifactError, setArtifactError] = useState<string | null>(null);
  const [artifactSuccess, setArtifactSuccess] = useState<string | null>(null);

  // Single file upload mutation (existing)
  const uploadMutation = useMutation({
    mutationFn: api.uploadFile,
    onSuccess: async (response) => {
      const dataSourceId = response.data_source_id || response.id;
      console.log('Upload successful, starting analysis for data source:', dataSourceId);

      try {
        const analysisRun = await api.runAnalysis(dataSourceId);
        console.log('Analysis completed:', analysisRun);
        await queryClient.invalidateQueries({ queryKey: ['analysisRuns'] });
        await queryClient.invalidateQueries({ queryKey: ['findings'] });
        await queryClient.refetchQueries({ queryKey: ['analysisRuns'] });
        await queryClient.refetchQueries({ queryKey: ['findings'] });
        setTimeout(() => {
          navigate('/');
        }, 1500);
      } catch (error: any) {
        console.error('Analysis failed:', error);
        alert(`Upload successful but analysis failed: ${error?.message || 'Unknown error'}`);
        queryClient.invalidateQueries({ queryKey: ['analysisRuns'] });
        queryClient.invalidateQueries({ queryKey: ['findings'] });
        navigate('/');
      }
    },
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      setUploadProgress(50);
      await uploadMutation.mutateAsync(selectedFile);
      setUploadProgress(100);
      setTimeout(() => {
        setUploadProgress(0);
        setSelectedFile(null);
      }, 2000);
    } catch (error) {
      console.error('Upload failed:', error);
      setUploadProgress(0);
    }
  };

  // Multi-file artifact handlers - add files one by one
  const handleAddArtifactFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const newFile = e.target.files[0];
      // Check if file with same name already exists
      const exists = artifactFiles.some(f => f.name === newFile.name);
      if (!exists) {
        setArtifactFiles(prev => [...prev, newFile]);
      }
      setArtifactError(null);
      setArtifactSuccess(null);
      // Reset the input so same file can be re-selected if removed
      e.target.value = '';
    }
  };

  const handleRemoveArtifactFile = (fileName: string) => {
    setArtifactFiles(prev => prev.filter(f => f.name !== fileName));
  };

  const handleClearArtifactFiles = () => {
    setArtifactFiles([]);
    setArtifactError(null);
    setArtifactSuccess(null);
  };

  const handleArtifactUpload = async () => {
    if (artifactFiles.length === 0) return;

    setArtifactError(null);
    setArtifactSuccess(null);
    setArtifactUploadProgress(25);

    try {
      // Step 1: Upload artifacts
      const formData = new FormData();
      artifactFiles.forEach(file => {
        formData.append('files', file);
      });

      const uploadResponse = await fetch(`${API_BASE_URL}/ingestion/upload-artifacts`, {
        method: 'POST',
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error(`Upload failed: ${uploadResponse.statusText}`);
      }

      const uploadResult = await uploadResponse.json();
      console.log('Artifacts uploaded:', uploadResult);
      setArtifactUploadProgress(50);

      // Step 2: Analyze and save
      const analyzeResponse = await fetch(`${API_BASE_URL}/content-analysis/analyze-and-save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          directory_path: uploadResult.artifacts_path,
          use_llm: false
        }),
      });

      if (!analyzeResponse.ok) {
        const errorData = await analyzeResponse.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const analyzeResult = await analyzeResponse.json();
      console.log('Analysis result:', analyzeResult);
      setArtifactUploadProgress(100);

      // Refresh data
      await queryClient.invalidateQueries({ queryKey: ['findings'] });
      await queryClient.invalidateQueries({ queryKey: ['kpis'] });
      await queryClient.refetchQueries({ queryKey: ['findings'] });

      setArtifactSuccess(
        `Success! Finding "${analyzeResult.focus_area}" created with ` +
        `$${(analyzeResult.money_loss_estimate || 0).toLocaleString()} exposure`
      );

      setTimeout(() => {
        setArtifactUploadProgress(0);
        setArtifactFiles([]);
        navigate('/');
      }, 2000);

    } catch (error: any) {
      console.error('Artifact upload/analysis failed:', error);
      setArtifactError(error.message || 'Unknown error');
      setArtifactUploadProgress(0);
    }
  };

  // Categorize selected artifact files
  const categorizeFiles = () => {
    const categories = {
      code: null as File | null,
      explanation: null as File | null,
      metadata: null as File | null,
      summary: null as File | null,
      other: [] as File[],
    };

    artifactFiles.forEach(file => {
      const name = file.name.toLowerCase();
      if (name.startsWith('code_') || name.includes('_code')) {
        categories.code = file;
      } else if (name.startsWith('explanation_') || name.includes('_explanation')) {
        categories.explanation = file;
      } else if (name.startsWith('metadata_') || name.includes('_metadata')) {
        categories.metadata = file;
      } else if (name.startsWith('summary_') || name.includes('_summary')) {
        categories.summary = file;
      } else {
        categories.other.push(file);
      }
    });

    return categories;
  };

  const fileCategories = categorizeFiles();

  return (
    <div className="container p-4">
      <h1 className="mb-4">Upload Files</h1>

      {/* Alert Artifacts Upload - NEW */}
      <div className="card mb-4">
        <div className="card-header bg-primary text-white">
          <h5 className="mb-0">Upload Alert Artifacts (4 Files)</h5>
        </div>
        <div className="card-body">
          <p className="text-muted mb-3">
            Upload the 4 artifact files for a single alert: Code, Explanation, Metadata, and Summary.
            Files should be named with prefixes like <code>Code_</code>, <code>Explanation_</code>, etc.
          </p>

          <div className="mb-3">
            <label className="form-label">Add Artifact Files (one by one)</label>
            <input
              type="file"
              className="form-control"
              accept=".txt,.csv,.xlsx,.docx,.pdf"
              onChange={handleAddArtifactFile}
            />
            <small className="form-text text-muted">
              Add each file one at a time. Files: Code_*, Explanation_*, Metadata_*, Summary_*
            </small>
          </div>

          {artifactFiles.length > 0 && (
            <div className="mb-3">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <h6 className="mb-0">Added Files ({artifactFiles.length}/4):</h6>
                <button
                  className="btn btn-sm btn-outline-danger"
                  onClick={handleClearArtifactFiles}
                >
                  Clear All
                </button>
              </div>
              <ul className="list-group list-group-flush">
                <li className={`list-group-item d-flex justify-content-between align-items-center ${fileCategories.code ? 'list-group-item-success' : 'list-group-item-warning'}`}>
                  <span><strong>Code:</strong> {fileCategories.code?.name || '(not added yet)'}</span>
                  {fileCategories.code && (
                    <button className="btn btn-sm btn-outline-danger" onClick={() => handleRemoveArtifactFile(fileCategories.code!.name)}>×</button>
                  )}
                </li>
                <li className={`list-group-item d-flex justify-content-between align-items-center ${fileCategories.explanation ? 'list-group-item-success' : 'list-group-item-warning'}`}>
                  <span><strong>Explanation:</strong> {fileCategories.explanation?.name || '(not added yet)'}</span>
                  {fileCategories.explanation && (
                    <button className="btn btn-sm btn-outline-danger" onClick={() => handleRemoveArtifactFile(fileCategories.explanation!.name)}>×</button>
                  )}
                </li>
                <li className={`list-group-item d-flex justify-content-between align-items-center ${fileCategories.metadata ? 'list-group-item-success' : 'list-group-item-warning'}`}>
                  <span><strong>Metadata:</strong> {fileCategories.metadata?.name || '(not added yet)'}</span>
                  {fileCategories.metadata && (
                    <button className="btn btn-sm btn-outline-danger" onClick={() => handleRemoveArtifactFile(fileCategories.metadata!.name)}>×</button>
                  )}
                </li>
                <li className={`list-group-item d-flex justify-content-between align-items-center ${fileCategories.summary ? 'list-group-item-success' : 'list-group-item-warning'}`}>
                  <span><strong>Summary:</strong> {fileCategories.summary?.name || '(not added yet)'}</span>
                  {fileCategories.summary && (
                    <button className="btn btn-sm btn-outline-danger" onClick={() => handleRemoveArtifactFile(fileCategories.summary!.name)}>×</button>
                  )}
                </li>
                {fileCategories.other.length > 0 && fileCategories.other.map(f => (
                  <li key={f.name} className="list-group-item list-group-item-info d-flex justify-content-between align-items-center">
                    <span><strong>Other:</strong> {f.name}</span>
                    <button className="btn btn-sm btn-outline-danger" onClick={() => handleRemoveArtifactFile(f.name)}>×</button>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {artifactUploadProgress > 0 && (
            <div className="mb-3">
              <div className="progress">
                <div
                  className="progress-bar bg-primary"
                  role="progressbar"
                  style={{ width: `${artifactUploadProgress}%` }}
                >
                  {artifactUploadProgress < 50 ? 'Uploading...' : artifactUploadProgress < 100 ? 'Analyzing...' : 'Done!'}
                </div>
              </div>
            </div>
          )}

          <button
            className="btn btn-primary"
            onClick={handleArtifactUpload}
            disabled={artifactFiles.length === 0 || artifactUploadProgress > 0}
          >
            {artifactUploadProgress > 0 ? 'Processing...' : 'Upload & Analyze Artifacts'}
          </button>

          {artifactError && (
            <div className="alert alert-danger mt-3">
              {artifactError}
            </div>
          )}

          {artifactSuccess && (
            <div className="alert alert-success mt-3">
              {artifactSuccess}
            </div>
          )}
        </div>
      </div>

      {/* Single File Upload - Existing */}
      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">Upload Single Report File</h5>
        </div>
        <div className="card-body">
          <p className="text-muted mb-3">
            Upload a single PDF, CSV, DOCX, or XLSX file containing a Skywind 4C alert or SoDA report.
          </p>

          <div className="mb-3">
            <label className="form-label">Select File</label>
            <input
              type="file"
              className="form-control"
              accept=".pdf,.csv,.docx,.xlsx"
              onChange={handleFileChange}
            />
            <small className="form-text text-muted">
              Supported formats: PDF, CSV, DOCX, XLSX
            </small>
          </div>

          {selectedFile && (
            <div className="mb-3">
              <p><strong>Selected:</strong> {selectedFile.name}</p>
              <p><strong>Size:</strong> {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          )}

          {uploadProgress > 0 && (
            <div className="mb-3">
              <div className="progress">
                <div
                  className="progress-bar"
                  role="progressbar"
                  style={{ width: `${uploadProgress}%` }}
                >
                  {uploadProgress}%
                </div>
              </div>
            </div>
          )}

          <button
            className="btn btn-secondary"
            onClick={handleUpload}
            disabled={!selectedFile || uploadMutation.isPending}
          >
            {uploadMutation.isPending ? 'Uploading...' : 'Upload & Analyze'}
          </button>

          {uploadMutation.isError && (
            <div className="alert alert-danger mt-3">
              Upload failed: {uploadMutation.error instanceof Error ? uploadMutation.error.message : 'Unknown error'}
            </div>
          )}

          {uploadMutation.isSuccess && (
            <div className="alert alert-success mt-3">
              File uploaded and analysis started successfully!
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Upload;
