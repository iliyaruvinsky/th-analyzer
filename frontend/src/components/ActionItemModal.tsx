import React, { useState } from 'react';
import { ActionItem } from '../services/api';

interface ActionItemModalProps {
  actionItem: ActionItem;
  onClose: () => void;
  onSave?: (updated: Partial<ActionItem>) => void;
}

const ActionItemModal: React.FC<ActionItemModalProps> = ({
  actionItem,
  onClose,
  onSave,
}) => {
  const [status, setStatus] = useState(actionItem.status);
  const [assignedTo, setAssignedTo] = useState(actionItem.assigned_to || '');
  const [notes, setNotes] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  const handleSave = () => {
    if (onSave) {
      onSave({
        id: actionItem.id,
        status,
        assigned_to: assignedTo || undefined,
      });
    }
    setIsEditing(false);
  };

  const statusOptions = ['OPEN', 'IN_REVIEW', 'REMEDIATED'];
  const priorityLabel = `P${actionItem.priority || 3}`;

  return (
    <div className="action-modal-overlay" onClick={onClose}>
      <div className="action-modal" onClick={(e) => e.stopPropagation()}>
        <div className="action-modal-header">
          <h3>Action Item Details</h3>
          <button className="action-modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="action-modal-body">
          {/* Title and Description */}
          <div className="action-field">
            <label className="action-label">Title</label>
            <div className="action-value title">{actionItem.title}</div>
          </div>

          {actionItem.description && (
            <div className="action-field">
              <label className="action-label">Description</label>
              <div className="action-value description">{actionItem.description}</div>
            </div>
          )}

          {/* Metadata Row */}
          <div className="action-metadata-row">
            <div className="action-metadata-item">
              <label className="action-label">Type</label>
              <span className={`ad-badge type-${actionItem.action_type.toLowerCase()}`}>
                {actionItem.action_type.replace('_', ' ')}
              </span>
            </div>
            <div className="action-metadata-item">
              <label className="action-label">Priority</label>
              <span className={`ad-priority p-${actionItem.priority || 3}`}>
                {priorityLabel}
              </span>
            </div>
            <div className="action-metadata-item">
              <label className="action-label">Created</label>
              <span className="action-date">
                {actionItem.created_at
                  ? new Date(actionItem.created_at).toLocaleDateString()
                  : '-'}
              </span>
            </div>
          </div>

          {/* Editable Fields */}
          <div className="action-editable-section">
            <div className="action-field">
              <label className="action-label">Status</label>
              {isEditing ? (
                <select
                  className="action-select"
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                >
                  {statusOptions.map((opt) => (
                    <option key={opt} value={opt}>
                      {opt.replace('_', ' ')}
                    </option>
                  ))}
                </select>
              ) : (
                <span className={`ad-status status-${status.toLowerCase()}`}>
                  {status.replace('_', ' ')}
                </span>
              )}
            </div>

            <div className="action-field">
              <label className="action-label">Assigned To</label>
              {isEditing ? (
                <input
                  type="text"
                  className="action-input"
                  value={assignedTo}
                  onChange={(e) => setAssignedTo(e.target.value)}
                  placeholder="Enter assignee name..."
                />
              ) : (
                <span className="action-value">{assignedTo || 'Unassigned'}</span>
              )}
            </div>

            <div className="action-field">
              <label className="action-label">Notes</label>
              {isEditing ? (
                <textarea
                  className="action-textarea"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Add notes about this action item..."
                  rows={3}
                />
              ) : (
                <span className="action-value notes">{notes || 'No notes added'}</span>
              )}
            </div>
          </div>

          {/* Related Finding if available */}
          {actionItem.finding_id && (
            <div className="action-field">
              <label className="action-label">Related Finding</label>
              <div className="action-related-finding">
                <span className="finding-id">Finding #{actionItem.finding_id}</span>
              </div>
            </div>
          )}
        </div>

        <div className="action-modal-footer">
          {isEditing ? (
            <>
              <button className="action-btn secondary" onClick={() => setIsEditing(false)}>
                Cancel
              </button>
              <button className="action-btn primary" onClick={handleSave}>
                Save Changes
              </button>
            </>
          ) : (
            <>
              <button className="action-btn secondary" onClick={onClose}>
                Close
              </button>
              <button className="action-btn primary" onClick={() => setIsEditing(true)}>
                <span>✎</span> Edit
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ActionItemModal;
