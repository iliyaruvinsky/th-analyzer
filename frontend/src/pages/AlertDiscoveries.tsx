import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useQueryClient, useMutation } from '@tanstack/react-query';
import { 
  getCriticalDiscoveries, 
  CriticalDiscoveryDrilldown,
  deleteAlertInstanceByAlertId,
  deleteAllAlertInstances,
  DeleteResponse
} from '../services/api';
import AlertSummary from './alert-discoveries/features/alert-summary';
import DiscoveryDetailPanel from './alert-discoveries/features/detail-panel';
import CreateActionItemModal from './alert-discoveries/features/create-action-item';
import { useAutoNavigation } from './alert-discoveries/features/auto-navigation';
import '../pages/AlertDashboard.css';

const AlertDiscoveries: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [actionModalOpen, setActionModalOpen] = useState(false);
  const [selectedForAction, setSelectedForAction] = useState<CriticalDiscoveryDrilldown | null>(null);
  const [selectedForDeletion, setSelectedForDeletion] = useState<Set<string>>(new Set());
  const [showDeleteAllModal, setShowDeleteAllModal] = useState(false);
  const [deleteAllConfirm, setDeleteAllConfirm] = useState('');
  const [showDeleteSingleModal, setShowDeleteSingleModal] = useState(false);
  const [showDeleteSelectedModal, setShowDeleteSelectedModal] = useState(false);
  const [discoveryToDelete, setDiscoveryToDelete] = useState<CriticalDiscoveryDrilldown | null>(null);
  const [toastMessage, setToastMessage] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const [deleteProgress, setDeleteProgress] = useState<{ isActive: boolean; current: number; total: number } | null>(null);

  // Currency formatter
  const currencyFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  });

  // Fetch all discoveries
  const { data: discoveries = [], isLoading, error } = useQuery<CriticalDiscoveryDrilldown[]>({
    queryKey: ['critical-discoveries'],
    queryFn: () => getCriticalDiscoveries(50),
    staleTime: 0, // Always refetch when invalidated
    refetchOnMount: true, // Refetch when component mounts
  });

  // Find selected discovery by alert_id
  const selectedDiscovery = id
    ? discoveries.find(d => d.alert_id === id)
    : discoveries[0];

  // Auto-select first discovery if none selected
  // Using default replace: false to preserve browser history
  useAutoNavigation({ id, discoveries });

  const handleCreateAction = (discovery: CriticalDiscoveryDrilldown) => {
    setSelectedForAction(discovery);
    setActionModalOpen(true);
  };

  // Delete single alert instance by alert_id
  const deleteInstanceMutation = useMutation({
    mutationFn: (alertId: string) => deleteAlertInstanceByAlertId(alertId),
    onSuccess: (data: DeleteResponse, alertId: string) => {
      const deletedDiscovery = discoveries.find(d => d.alert_id === alertId);
      
      // Show success toast
      setToastMessage({
        type: 'success',
        message: `Discovery "${deletedDiscovery?.alert_name || alertId}" successfully deleted`
      });
      
      // Invalidate and refetch queries to update KPIs and sidebar
      queryClient.invalidateQueries({ queryKey: ['critical-discoveries'] });
      queryClient.invalidateQueries({ queryKey: ['criticalDiscoveries'] });
      queryClient.invalidateQueries({ queryKey: ['critical-discoveries-sidebar'] });
      queryClient.invalidateQueries({ queryKey: ['alert-dashboard-kpis'] });
      
      // Remove from selection
      const newSelection = new Set(selectedForDeletion);
      newSelection.delete(alertId);
      setSelectedForDeletion(newSelection);
      
      // Force immediate refetch to update UI (bypass staleTime by removing and refetching)
      setTimeout(() => {
        // Clear cached queries to force fresh fetch
        queryClient.removeQueries({ queryKey: ['critical-discoveries-sidebar'] });
        queryClient.removeQueries({ queryKey: ['critical-discoveries'] });
        
        // Refetch fresh data
        queryClient.refetchQueries({ queryKey: ['critical-discoveries'] });
        queryClient.refetchQueries({ queryKey: ['critical-discoveries-sidebar'] });
        queryClient.refetchQueries({ queryKey: ['alert-dashboard-kpis'] });
      }, 300);
      
      // Navigate away if deleted discovery was selected
      if (selectedDiscovery && selectedDiscovery.alert_id === alertId) {
        setTimeout(() => {
          const remaining = discoveries.filter(d => d.alert_id !== alertId);
          if (remaining.length > 0) {
            navigate(`/alert-discoveries/${remaining[0].alert_id}`);
          } else {
            navigate('/alert-discoveries');
          }
        }, 400);
      }
    },
    onError: (error: Error) => {
      setToastMessage({
        type: 'error',
        message: `Failed to delete discovery: ${error.message}`
      });
    },
  });

  // Delete all alert instances
  const deleteAllMutation = useMutation({
    mutationFn: () => {
      setDeleteProgress({ isActive: true, current: 0, total: discoveries.length });
      return deleteAllAlertInstances();
    },
    onSuccess: () => {
      setDeleteProgress({ isActive: true, current: discoveries.length, total: discoveries.length });
      
      // Show success toast
      setToastMessage({
        type: 'success',
        message: `All ${discoveries.length} discoveries successfully deleted`
      });
      
      // Invalidate and refetch queries to update KPIs and sidebar
      queryClient.invalidateQueries({ queryKey: ['critical-discoveries'] });
      queryClient.invalidateQueries({ queryKey: ['criticalDiscoveries'] });
      queryClient.invalidateQueries({ queryKey: ['critical-discoveries-sidebar'] });
      queryClient.invalidateQueries({ queryKey: ['alert-dashboard-kpis'] });
      
      // Force immediate refetch to update UI (bypass staleTime)
      setTimeout(() => {
        // Remove staleTime by resetting the queries
        queryClient.removeQueries({ queryKey: ['critical-discoveries-sidebar'] });
        queryClient.removeQueries({ queryKey: ['critical-discoveries'] });
        
        // Then refetch fresh data
        queryClient.refetchQueries({ queryKey: ['critical-discoveries'] });
        queryClient.refetchQueries({ queryKey: ['critical-discoveries-sidebar'] });
        queryClient.refetchQueries({ queryKey: ['alert-dashboard-kpis'] });
      }, 300);
      
      // Close modal and navigate
      setShowDeleteAllModal(false);
      setDeleteAllConfirm('');
      setSelectedForDeletion(new Set());
      setDeleteProgress(null);
      
      setTimeout(() => {
        navigate('/alert-discoveries');
      }, 500);
    },
    onError: (error: Error) => {
      setDeleteProgress(null);
      setToastMessage({
        type: 'error',
        message: `Failed to delete all discoveries: ${error.message}`
      });
    },
  });

  const handleDeleteDiscovery = (discovery: CriticalDiscoveryDrilldown, e?: React.MouseEvent) => {
    e?.stopPropagation();
    setDiscoveryToDelete(discovery);
    setShowDeleteSingleModal(true);
  };

  const confirmDeleteSingle = () => {
    if (discoveryToDelete) {
      const alertId = discoveryToDelete.alert_id;
      deleteInstanceMutation.mutate(alertId, {
        onSuccess: () => {
          setShowDeleteSingleModal(false);
          setDiscoveryToDelete(null);
        },
        onError: () => {
          // Keep modal open on error so user can retry
        }
      });
    }
  };

  const handleToggleSelection = (alertId: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    const newSelection = new Set(selectedForDeletion);
    if (newSelection.has(alertId)) {
      newSelection.delete(alertId);
    } else {
      newSelection.add(alertId);
    }
    setSelectedForDeletion(newSelection);
  };

  const handleSelectAll = () => {
    if (selectedForDeletion.size === discoveries.length) {
      setSelectedForDeletion(new Set());
    } else {
      setSelectedForDeletion(new Set(discoveries.map(d => d.alert_id)));
    }
  };

  const handleDeleteSelected = () => {
    if (selectedForDeletion.size === 0) return;
    
    const count = selectedForDeletion.size;
    const selectedDiscoveries = discoveries.filter(d => selectedForDeletion.has(d.alert_id));
    setDiscoveryToDelete(selectedDiscoveries[0]); // For modal display
    setShowDeleteSelectedModal(true);
  };

  const confirmDeleteSelected = async () => {
    if (selectedForDeletion.size === 0) return;
    
    const alertIds = Array.from(selectedForDeletion);
    const total = alertIds.length;
    setDeleteProgress({ isActive: true, current: 0, total });
    setShowDeleteSelectedModal(false);
    setDiscoveryToDelete(null);
    
    // Delete each selected discovery sequentially with progress updates
    let completed = 0;
    const errors: string[] = [];
    
    for (const alertId of alertIds) {
      try {
        await deleteAlertInstanceByAlertId(alertId);
        completed++;
        setDeleteProgress({ isActive: true, current: completed, total });
        
        // Invalidate queries after each deletion to update KPIs
        queryClient.invalidateQueries({ queryKey: ['critical-discoveries'] });
        queryClient.invalidateQueries({ queryKey: ['critical-discoveries-sidebar'] });
        queryClient.invalidateQueries({ queryKey: ['alert-dashboard-kpis'] });
      } catch (error) {
        errors.push(alertId);
        completed++;
        setDeleteProgress({ isActive: true, current: completed, total });
      }
    }
    
    // Final refetch and cleanup
    setTimeout(() => {
      queryClient.refetchQueries({ queryKey: ['critical-discoveries'], type: 'active' });
      queryClient.refetchQueries({ queryKey: ['critical-discoveries-sidebar'], type: 'active' });
      queryClient.refetchQueries({ queryKey: ['alert-dashboard-kpis'], type: 'active' });
    }, 100);
    
    if (errors.length === 0) {
      setToastMessage({
        type: 'success',
        message: `${total} discoveries successfully deleted`
      });
    } else {
      setToastMessage({
        type: 'error',
        message: `${total - errors.length} deleted, ${errors.length} failed`
      });
    }
    
    setTimeout(() => {
      setDeleteProgress(null);
      setSelectedForDeletion(new Set());
      
      // Navigate away if current discovery was deleted
      if (selectedDiscovery && selectedForDeletion.has(selectedDiscovery.alert_id)) {
        const remaining = discoveries.filter(d => !selectedForDeletion.has(d.alert_id));
        if (remaining.length > 0) {
          navigate(`/alert-discoveries/${remaining[0].alert_id}`);
        } else {
          navigate('/alert-discoveries');
        }
      }
    }, 500);
  };

  const handleDeleteAll = () => {
    if (deleteAllConfirm !== 'DELETE ALL') {
      alert('Please type "DELETE ALL" to confirm');
      return;
    }
    setDeleteProgress({ isActive: true, current: 0, total: discoveries.length });
    deleteAllMutation.mutate();
  };

  // Auto-hide toast after 5 seconds
  useEffect(() => {
    if (toastMessage) {
      const timer = setTimeout(() => {
        setToastMessage(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [toastMessage]);

  if (isLoading) {
    return (
      <div className="alert-discoveries-page">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading discoveries...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert-discoveries-page">
        <div className="error-state">
          <h3>Error loading discoveries</h3>
          <p>{(error as Error).message}</p>
        </div>
      </div>
    );
  }

  if (discoveries.length === 0) {
    return (
      <div className="alert-discoveries-page">
        <AlertSummary discoveries={[]} currencyFormatter={currencyFormatter} />
        <div className="empty-state">
          <h3>No Alert Discoveries</h3>
          <p>No critical discoveries have been analyzed yet. Upload and analyze alerts to see them here.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="alert-discoveries-page">
      {/* Toast Notification */}
      {toastMessage && (
        <div className={`toast-notification toast-${toastMessage.type}`}>
          <span className="toast-icon">{toastMessage.type === 'success' ? '✓' : '✗'}</span>
          <span className="toast-message">{toastMessage.message}</span>
          <button className="toast-close" onClick={() => setToastMessage(null)}>×</button>
        </div>
      )}

      {/* Progress Bar */}
      {deleteProgress && deleteProgress.isActive && (
        <div className="delete-progress-bar">
          <div className="progress-bar-container">
            <div className="progress-bar-fill" style={{ width: `${(deleteProgress.current / deleteProgress.total) * 100}%` }}></div>
          </div>
          <div className="progress-bar-text">
            Deleting {deleteProgress.current} of {deleteProgress.total} discoveries...
          </div>
        </div>
      )}

      {/* Alert Summary Header */}
      <AlertSummary discoveries={discoveries} currencyFormatter={currencyFormatter} />

      {/* Delete Selected Discoveries Confirmation Modal */}
      {showDeleteSelectedModal && selectedForDeletion.size > 0 && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }}>
          <div className="modal-dialog modal-lg">
            <div className="modal-content">
              <div className="modal-header bg-warning text-dark">
                <h5 className="modal-title">Delete Selected Discoveries</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => {
                    setShowDeleteSelectedModal(false);
                    setDiscoveryToDelete(null);
                  }}
                ></button>
              </div>
              <div className="modal-body">
                <div className="alert alert-warning">
                  <strong>WARNING:</strong> This will permanently delete <strong>{selectedForDeletion.size} selected discoveries</strong>, all their analyses, and all related data.
                  <br /><br />
                  This action cannot be undone!
                </div>
                <div className="mt-3">
                  <p className="mb-2"><strong>Selected Discoveries ({selectedForDeletion.size}):</strong></p>
                  <div className="table-responsive" style={{ maxHeight: '300px', overflowY: 'auto' }}>
                    <table className="table table-sm table-hover">
                      <thead className="table-light sticky-top">
                        <tr>
                          <th style={{ width: '40px' }}>
                            <input
                              type="checkbox"
                              checked={true}
                              disabled
                            />
                          </th>
                          <th>Alert Name</th>
                          <th>Alert ID</th>
                          <th>Severity</th>
                          <th>Financial Impact</th>
                        </tr>
                      </thead>
                      <tbody>
                        {discoveries
                          .filter(d => selectedForDeletion.has(d.alert_id))
                          .map(d => (
                            <tr key={d.alert_id}>
                              <td>
                                <input
                                  type="checkbox"
                                  checked={true}
                                  disabled
                                />
                              </td>
                              <td><strong>{d.alert_name}</strong></td>
                              <td><code>{d.alert_id}</code></td>
                              <td>
                                <span className={`badge ${
                                  d.severity === 'CRITICAL' ? 'bg-danger' :
                                  d.severity === 'HIGH' ? 'bg-warning' :
                                  d.severity === 'MEDIUM' ? 'bg-info' : 'bg-secondary'
                                }`}>
                                  {d.severity}
                                </span>
                              </td>
                              <td>
                                {d.financial_impact_usd
                                  ? currencyFormatter.format(parseFloat(d.financial_impact_usd))
                                  : 'N/A'}
                              </td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setShowDeleteSelectedModal(false);
                    setDiscoveryToDelete(null);
                  }}
                >
                  Cancel
                </button>
                <button
                  type="button"
                  className="btn btn-warning"
                  onClick={confirmDeleteSelected}
                  disabled={deleteInstanceMutation.isPending || deleteProgress?.isActive}
                >
                  {deleteInstanceMutation.isPending || deleteProgress?.isActive ? 'Deleting...' : `Delete ${selectedForDeletion.size} Discoveries`}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete Single Discovery Confirmation Modal */}
      {showDeleteSingleModal && discoveryToDelete && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header bg-danger text-white">
                <h5 className="modal-title">Delete Discovery</h5>
                <button
                  type="button"
                  className="btn-close btn-close-white"
                  onClick={() => {
                    setShowDeleteSingleModal(false);
                    setDiscoveryToDelete(null);
                  }}
                ></button>
              </div>
              <div className="modal-body">
                <div className="alert alert-danger">
                  <strong>WARNING:</strong> This will permanently delete the discovery <strong>"{discoveryToDelete.alert_name}"</strong> (ID: {discoveryToDelete.alert_id}), all its analyses, and all related data.
                  <br /><br />
                  This action cannot be undone!
                </div>
                <div className="mt-3">
                  <p className="mb-1"><strong>Alert Details:</strong></p>
                  <ul className="mb-0">
                    <li>Alert ID: <code>{discoveryToDelete.alert_id}</code></li>
                    <li>Focus Area: {discoveryToDelete.focus_area}</li>
                    <li>Severity: {discoveryToDelete.severity}</li>
                    {discoveryToDelete.financial_impact_usd && (
                      <li>Financial Impact: {currencyFormatter.format(parseFloat(discoveryToDelete.financial_impact_usd))}</li>
                    )}
                  </ul>
                </div>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setShowDeleteSingleModal(false);
                    setDiscoveryToDelete(null);
                  }}
                >
                  Cancel
                </button>
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={confirmDeleteSingle}
                  disabled={deleteInstanceMutation.isPending}
                >
                  {deleteInstanceMutation.isPending ? 'Deleting...' : 'Delete Discovery'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete All Confirmation Modal */}
      {showDeleteAllModal && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header bg-danger text-white">
                <h5 className="modal-title">Delete All Discoveries</h5>
                <button
                  type="button"
                  className="btn-close btn-close-white"
                  onClick={() => {
                    setShowDeleteAllModal(false);
                    setDeleteAllConfirm('');
                  }}
                ></button>
              </div>
              <div className="modal-body">
                <div className="alert alert-danger">
                  <strong>WARNING:</strong> This will permanently delete ALL {discoveries.length} discoveries, all alert analyses, and all related data.
                  This action cannot be undone!
                </div>
                <p>Type <strong>DELETE ALL</strong> to confirm:</p>
                <input
                  type="text"
                  className="form-control"
                  value={deleteAllConfirm}
                  onChange={(e) => setDeleteAllConfirm(e.target.value)}
                  placeholder="DELETE ALL"
                />
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setShowDeleteAllModal(false);
                    setDeleteAllConfirm('');
                  }}
                >
                  Cancel
                </button>
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={handleDeleteAll}
                  disabled={deleteAllMutation.isPending || deleteAllConfirm !== 'DELETE ALL'}
                >
                  {deleteAllMutation.isPending ? 'Deleting...' : 'Delete All'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Content - Full width detail view */}
      <div className="discovery-main-content">
        {selectedDiscovery ? (
          <div className="discovery-detail-wrapper">
            <DiscoveryDetailPanel
              discovery={selectedDiscovery}
              mode="page"
              onClose={() => {}}
              currencyFormatter={currencyFormatter}
              onCreateAction={handleCreateAction}
            />
          </div>
        ) : (
          <div className="discovery-list-view">
            <div className="select-discovery-prompt mb-3">
              <p>Select a discovery from the sidebar to view details, or use the controls above to manage discoveries.</p>
            </div>
            
            {/* Discovery List with Checkboxes for Bulk Operations */}
            {discoveries.length > 0 && (
              <div className="card">
                <div className="card-header">
                  <h5 className="mb-0">All Discoveries ({discoveries.length})</h5>
                </div>
                <div className="card-body p-0">
                  <div className="table-responsive">
                    <table className="table table-hover mb-0">
                      <thead>
                        <tr>
                          <th style={{ width: '40px' }}>
                            <input
                              type="checkbox"
                              checked={selectedForDeletion.size === discoveries.length && discoveries.length > 0}
                              onChange={handleSelectAll}
                            />
                          </th>
                          <th>Alert Name</th>
                          <th>Alert ID</th>
                          <th>Focus Area</th>
                          <th>Severity</th>
                          <th>Financial Impact</th>
                          <th>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {discoveries.map((discovery) => (
                          <tr key={discovery.alert_id}>
                            <td>
                              <input
                                type="checkbox"
                                checked={selectedForDeletion.has(discovery.alert_id)}
                                onChange={(e) => handleToggleSelection(discovery.alert_id, e)}
                              />
                            </td>
                            <td>
                              <a
                                href={`#/alert-discoveries/${discovery.alert_id}`}
                                onClick={(e) => {
                                  e.preventDefault();
                                  navigate(`/alert-discoveries/${discovery.alert_id}`);
                                }}
                                className="text-decoration-none"
                              >
                                {discovery.alert_name}
                              </a>
                            </td>
                            <td>{discovery.alert_id}</td>
                            <td>
                              <span className="badge bg-secondary">{discovery.focus_area}</span>
                            </td>
                            <td>
                              <span className={`badge ${
                                discovery.severity === 'CRITICAL' ? 'bg-danger' :
                                discovery.severity === 'HIGH' ? 'bg-warning' :
                                discovery.severity === 'MEDIUM' ? 'bg-info' : 'bg-secondary'
                              }`}>
                                {discovery.severity}
                              </span>
                            </td>
                            <td>
                              {discovery.financial_impact_usd
                                ? currencyFormatter.format(parseFloat(discovery.financial_impact_usd))
                                : 'N/A'}
                            </td>
                            <td>
                              <button
                                className="btn btn-sm btn-danger"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleDeleteDiscovery(discovery, e);
                                }}
                                disabled={deleteInstanceMutation.isPending}
                                title="Delete this discovery"
                              >
                                🗑️ Delete
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer with Action Buttons */}
      <div className="discovery-footer">
        <div className="discovery-footer-content">
          {/* Left side - Selection controls */}
          <div className="discovery-footer-left">
            <button
              className="btn btn-footer-select"
              onClick={handleSelectAll}
              disabled={discoveries.length === 0}
            >
              {selectedForDeletion.size === discoveries.length && discoveries.length > 0 ? 'Deselect All' : 'Select All'}
            </button>
            {selectedForDeletion.size > 0 && (
              <>
                <span className="discovery-footer-separator">|</span>
                <span className="discovery-footer-selection-count">
                  {selectedForDeletion.size} selected
                </span>
                <button
                  className="btn btn-footer-clear"
                  onClick={() => setSelectedForDeletion(new Set())}
                >
                  Clear Selection
                </button>
              </>
            )}
          </div>

          {/* Right side - Delete actions */}
          <div className="discovery-footer-right">
            {/* Delete Selected - appears ONLY when multiple (but not all) are selected via checkboxes */}
            {selectedForDeletion.size > 0 && selectedForDeletion.size < discoveries.length && (
              <button
                className="btn btn-footer-delete-selected"
                onClick={handleDeleteSelected}
                disabled={deleteInstanceMutation.isPending || deleteAllMutation.isPending || deleteProgress?.isActive}
                title={`Delete ${selectedForDeletion.size} selected discoveries`}
              >
                {deleteInstanceMutation.isPending || deleteProgress?.isActive ? 'Deleting...' : `🗑️ Delete Selected (${selectedForDeletion.size})`}
              </button>
            )}
            {/* Delete This Discovery - appears when viewing a single discovery AND no checkboxes are selected */}
            {selectedDiscovery && selectedForDeletion.size === 0 && (
              <button
                className="btn btn-footer-delete-single"
                onClick={() => handleDeleteDiscovery(selectedDiscovery)}
                disabled={deleteInstanceMutation.isPending || deleteAllMutation.isPending || deleteProgress?.isActive}
                title="Delete the currently selected discovery"
              >
                {deleteInstanceMutation.isPending ? 'Deleting...' : '🗑️ Delete This Discovery'}
              </button>
            )}
            {/* Delete All - always visible when discoveries exist */}
            <button
              className="btn btn-footer-delete-all"
              onClick={() => setShowDeleteAllModal(true)}
              disabled={discoveries.length === 0 || deleteAllMutation.isPending || deleteInstanceMutation.isPending || deleteProgress?.isActive}
              title="Delete all discoveries"
            >
              {deleteAllMutation.isPending ? 'Deleting All...' : '🗑️ Delete All Discoveries'}
            </button>
          </div>
        </div>
      </div>

      {/* Create Action Item Modal */}
      {actionModalOpen && selectedForAction && (
        <CreateActionItemModal
          discovery={selectedForAction}
          onClose={() => {
            setActionModalOpen(false);
            setSelectedForAction(null);
          }}
          onSuccess={() => {
            setActionModalOpen(false);
            setSelectedForAction(null);
            // Invalidate action queue to refresh
            queryClient.invalidateQueries({ queryKey: ['action-queue'] });
          }}
        />
      )}
    </div>
  );
};

export default AlertDiscoveries;
