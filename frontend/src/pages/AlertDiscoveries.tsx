import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { getCriticalDiscoveries, CriticalDiscoveryDrilldown } from '../services/api';
import AlertSummary from './alert-discoveries/features/alert-summary';
import DiscoveryDetailPanel from './alert-discoveries/features/detail-panel';
import CreateActionItemModal from './alert-discoveries/features/create-action-item';
import { useAutoNavigation } from './alert-discoveries/features/auto-navigation';
import '../pages/AlertDashboard.css';

const AlertDiscoveries: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const [actionModalOpen, setActionModalOpen] = useState(false);
  const [selectedForAction, setSelectedForAction] = useState<CriticalDiscoveryDrilldown | null>(null);

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
    staleTime: 30000,
  });

  // Find selected discovery by alert_id
  const selectedDiscovery = id
    ? discoveries.find(d => d.alert_id === id)
    : discoveries[0];

  // Auto-select first discovery if none selected
  useAutoNavigation({ id, discoveries, replace: true });

  const handleCreateAction = (discovery: CriticalDiscoveryDrilldown) => {
    setSelectedForAction(discovery);
    setActionModalOpen(true);
  };

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
      {/* Alert Summary Header */}
      <AlertSummary discoveries={discoveries} currencyFormatter={currencyFormatter} />

      {/* Main Content - Full width detail view */}
      <div className="discovery-main-content">
        {selectedDiscovery ? (
          <DiscoveryDetailPanel
            discovery={selectedDiscovery}
            mode="page"
            onClose={() => {}}
            currencyFormatter={currencyFormatter}
            onCreateAction={handleCreateAction}
          />
        ) : (
          <div className="select-discovery-prompt">
            <p>Select a discovery from the sidebar to view details</p>
          </div>
        )}
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
