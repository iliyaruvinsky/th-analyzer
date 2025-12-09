import React, { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getCriticalDiscoveries, CriticalDiscoveryDrilldown } from '../services/api'
import SkywindLogo from './SkywindLogo'
import './Layout.css'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation()
  const navigate = useNavigate()
  const [expandedSections, setExpandedSections] = useState<string[]>(['discoveries'])

  // Fetch discoveries for sidebar
  const { data: discoveries = [] } = useQuery<CriticalDiscoveryDrilldown[]>({
    queryKey: ['critical-discoveries-sidebar'],
    queryFn: () => getCriticalDiscoveries(50),
    staleTime: 60000,
  })

  const toggleSection = (section: string) => {
    setExpandedSections(prev =>
      prev.includes(section)
        ? prev.filter(s => s !== section)
        : [...prev, section]
    )
  }

  const isDiscoveriesExpanded = expandedSections.includes('discoveries')
  const isOnDiscoveriesPage = location.pathname.startsWith('/alert-discoveries')

  // Get severity color class
  const getSeverityClass = (severity: string): string => {
    switch (severity?.toUpperCase()) {
      case 'CRITICAL': return 'severity-critical'
      case 'HIGH': return 'severity-high'
      case 'MEDIUM': return 'severity-medium'
      case 'LOW': return 'severity-low'
      default: return 'severity-unknown'
    }
  }

  // Format currency for sidebar
  const formatCurrency = (value: string | undefined): string => {
    if (!value) return '-'
    const num = parseFloat(value)
    if (isNaN(num)) return '-'
    if (num >= 1000000000) return `$${(num / 1000000000).toFixed(1)}B`
    if (num >= 1000000) return `$${(num / 1000000).toFixed(1)}M`
    if (num >= 1000) return `$${(num / 1000).toFixed(0)}K`
    return `$${num.toFixed(0)}`
  }

  // Check if a discovery is selected
  const isDiscoverySelected = (alertId: string): boolean => {
    return location.pathname === `/alert-discoveries/${alertId}`
  }

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '◆' },
    { path: '/upload', label: 'Upload', icon: '↑' },
  ]

  const navItemsAfterDiscoveries = [
    { path: '/findings', label: 'Findings', icon: '⬢' },
    { path: '/reports', label: 'Reports', icon: '▤' },
    { path: '/maintenance', label: 'Maintenance', icon: '⚙' },
    { path: '/logs', label: 'Logs', icon: '☰' },
  ]

  return (
    <div className="app-layout">
      <nav className="sidebar">
        {/* Skywind Logo */}
        <div className="sidebar-header">
          <SkywindLogo size="medium" showText={true} variant="light" />
        </div>

        {/* Divider */}
        <div className="sidebar-divider"></div>

        {/* Navigation */}
        <ul className="nav-list">
          {/* Dashboard and Upload */}
          {navItems.map(item => (
            <li key={item.path} className="nav-item">
              <Link
                to={item.path}
                className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </Link>
            </li>
          ))}

          {/* Alert Discoveries - Expandable Section */}
          <li className="nav-item expandable-section">
            <div
              className={`nav-link expandable-header ${isOnDiscoveriesPage ? 'active' : ''}`}
              onClick={() => {
                toggleSection('discoveries')
                if (!isOnDiscoveriesPage && discoveries.length > 0) {
                  navigate(`/alert-discoveries/${discoveries[0]?.alert_id || ''}`)
                }
              }}
            >
              <span className="nav-icon">⚡</span>
              <span className="nav-label">Discoveries</span>
              <span className="nav-badge">{discoveries.length}</span>
              <span className="nav-chevron">{isDiscoveriesExpanded ? '▼' : '▶'}</span>
            </div>

            {/* Expandable Discovery List - Card Layout */}
            {isDiscoveriesExpanded && (
              <div className="discovery-cards-container">
                {discoveries.map((discovery) => (
                  <div
                    key={discovery.alert_id}
                    className={`discovery-card ${isDiscoverySelected(discovery.alert_id) ? 'selected' : ''} ${getSeverityClass(discovery.severity)}`}
                    onClick={() => navigate(`/alert-discoveries/${discovery.alert_id}`)}
                  >
                    {/* Alert Name - Full */}
                    <div className="card-alert-name">{discovery.alert_name}</div>

                    {/* Simplified KPI: Focus Area + Financial Impact */}
                    <div className="card-kpi-row">
                      <div className="card-kpi">
                        <span className="card-kpi-label">Focus Area</span>
                        <span className="card-kpi-value focus-area">{discovery.focus_area}</span>
                      </div>
                      <div className="card-kpi">
                        <span className="card-kpi-label">Financial Impact</span>
                        <span className="card-kpi-value impact">
                          {formatCurrency(discovery.financial_impact_usd)}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
                {discoveries.length === 0 && (
                  <div className="discovery-card empty">
                    <span className="empty-text">No discoveries yet</span>
                  </div>
                )}
              </div>
            )}
          </li>

          {/* Other nav items */}
          {navItemsAfterDiscoveries.map(item => (
            <li key={item.path} className="nav-item">
              <Link
                to={item.path}
                className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </Link>
            </li>
          ))}
        </ul>

        {/* Footer */}
        <div className="sidebar-footer">
          <div className="app-version">ver 3.1</div>
        </div>
      </nav>
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}

export default Layout
