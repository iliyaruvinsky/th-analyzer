import React, { useState } from 'react';
import { CriticalDiscoveryDrilldown, ActionItemCreate, createActionItem } from '../../../../services/api';

interface CreateActionItemModalProps {
  discovery: CriticalDiscoveryDrilldown;
  onClose: () => void;
  onSuccess: () => void;
}

const CreateActionItemModal: React.FC<CreateActionItemModalProps> = ({
  discovery,
  onClose,
  onSuccess,
}) => {
  const [actionType, setActionType] = useState('IMMEDIATE');
  const [priority, setPriority] = useState(1);
  const [title, setTitle] = useState(`Investigate: ${discovery.alert_name}`);
  const [description, setDescription] = useState(
    discovery.discoveries?.[0]?.headline || `Review ${discovery.discovery_count} discovery/ies for ${discovery.alert_name}`
  );
  const [assignedTo, setAssignedTo] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // We need alert_analysis_id - get it from first discovery
  const alertAnalysisId = discovery.discoveries?.[0]?.alert_analysis_id;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!alertAnalysisId) {
      setError('Cannot create action item: missing alert analysis ID');
      return;
    }

    setIsSubmitting(true);

    try {
      const actionItem: ActionItemCreate = {
        alert_analysis_id: alertAnalysisId,
        action_type: actionType,
        priority,
        title,
        description,
        assigned_to: assignedTo || undefined,
        due_date: dueDate || undefined,
      };

      await createActionItem(actionItem);
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create action item');
    } finally {
      setIsSubmitting(false);
    }
  };

  const actionTypes = [
    { value: 'IMMEDIATE', label: 'Immediate (24-48h)' },
    { value: 'SHORT_TERM', label: 'Short Term (1-2 weeks)' },
    { value: 'PROCESS_IMPROVEMENT', label: 'Process Improvement' },
  ];

  return (
    <div className="action-modal-overlay" onClick={onClose}>
      <div className="action-modal" onClick={(e) => e.stopPropagation()}>
        <div className="action-modal-header">
          <h3>Create Action Item</h3>
          <button className="action-modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="action-modal-body">
            {/* Alert Context */}
            <div className="action-field">
              <label className="action-label">Alert</label>
              <div className="action-value">
                <strong>{discovery.alert_name}</strong>
                <span className={`ad-badge severity-${discovery.severity.toLowerCase()}`} style={{ marginLeft: '8px' }}>
                  {discovery.severity}
                </span>
              </div>
            </div>

            {error && (
              <div className="action-error" style={{ color: '#dc3545', padding: '8px', marginBottom: '12px', background: '#fff3f3', borderRadius: '4px' }}>
                {error}
              </div>
            )}

            {/* Title */}
            <div className="action-field">
              <label className="action-label">Title *</label>
              <input
                type="text"
                className="action-input"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                maxLength={255}
              />
            </div>

            {/* Description */}
            <div className="action-field">
              <label className="action-label">Description</label>
              <textarea
                className="action-textarea"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
              />
            </div>

            {/* Action Type and Priority Row */}
            <div className="action-metadata-row">
              <div className="action-metadata-item" style={{ flex: 1 }}>
                <label className="action-label">Type *</label>
                <select
                  className="action-select"
                  value={actionType}
                  onChange={(e) => setActionType(e.target.value)}
                  required
                >
                  {actionTypes.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>
              <div className="action-metadata-item" style={{ flex: 1 }}>
                <label className="action-label">Priority *</label>
                <select
                  className="action-select"
                  value={priority}
                  onChange={(e) => setPriority(Number(e.target.value))}
                  required
                >
                  <option value={1}>P1 - Critical</option>
                  <option value={2}>P2 - High</option>
                  <option value={3}>P3 - Medium</option>
                  <option value={4}>P4 - Low</option>
                  <option value={5}>P5 - Minimal</option>
                </select>
              </div>
            </div>

            {/* Assigned To and Due Date Row */}
            <div className="action-metadata-row">
              <div className="action-metadata-item" style={{ flex: 1 }}>
                <label className="action-label">Assigned To</label>
                <input
                  type="text"
                  className="action-input"
                  value={assignedTo}
                  onChange={(e) => setAssignedTo(e.target.value)}
                  placeholder="Enter assignee name..."
                />
              </div>
              <div className="action-metadata-item" style={{ flex: 1 }}>
                <label className="action-label">Due Date</label>
                <input
                  type="date"
                  className="action-input"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                />
              </div>
            </div>
          </div>

          <div className="action-modal-footer">
            <button
              type="button"
              className="action-btn secondary"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="action-btn primary"
              disabled={isSubmitting || !alertAnalysisId}
            >
              {isSubmitting ? 'Creating...' : 'Create Action Item'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateActionItemModal;
