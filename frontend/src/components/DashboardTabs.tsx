import React from 'react';

export type DashboardTabType = 'overview' | 'alerts' | 'actions';

interface DashboardTabsProps {
  activeTab: DashboardTabType;
  onTabChange: (tab: DashboardTabType) => void;
}

const DashboardTabs: React.FC<DashboardTabsProps> = ({ activeTab, onTabChange }) => {
  const tabs: { id: DashboardTabType; label: string; icon: string }[] = [
    { id: 'overview', label: 'Overview', icon: '◐' },
    { id: 'alerts', label: 'Alert Analysis', icon: '⚡' },
    { id: 'actions', label: 'Action Queue', icon: '✓' },
  ];

  return (
    <div className="dashboard-tabs">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`dashboard-tab ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => onTabChange(tab.id)}
        >
          <span className="tab-icon">{tab.icon}</span>
          {tab.label}
        </button>
      ))}
    </div>
  );
};

export default DashboardTabs;
