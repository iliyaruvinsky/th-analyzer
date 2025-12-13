import React, { useState, useMemo } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { getCriticalDiscoveries, CriticalDiscoveryDrilldown } from '../services/api'
import SkywindLogo from './SkywindLogo'
import SidebarFilters, { FilterValues } from './SidebarFilters'
import './Layout.css'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [expandedSections, setExpandedSections] = useState<string[]>(['discoveries'])
  const [filters, setFilters] = useState<FilterValues>({
    focusArea: '',
    module: '',
    severity: '',
  })

  // Fetch discoveries for sidebar
  const { data: discoveries = [] } = useQuery<CriticalDiscoveryDrilldown[]>({
    queryKey: ['critical-discoveries-sidebar'],
    queryFn: () => getCriticalDiscoveries(50),
    staleTime: 60000,
  })

  // Extract unique filter options from discoveries
  const filterOptions = useMemo(() => {
    const focusAreas = new Set<string>()
    const modules = new Set<string>()
    const severities = new Set<string>()

    discoveries.forEach((d) => {
      if (d.focus_area) focusAreas.add(d.focus_area)
      if (d.module) modules.add(d.module)
      if (d.severity) severities.add(d.severity)
    })

    return {
      focusAreas: Array.from(focusAreas).sort(),
      modules: Array.from(modules).sort(),
      severities: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].filter((s) => severities.has(s)),
    }
  }, [discoveries])

  // Filter discoveries based on selected filters
  const filteredDiscoveries = useMemo(() => {
    return discoveries.filter((d) => {
      if (filters.focusArea && d.focus_area !== filters.focusArea) return false
      if (filters.module && d.module !== filters.module) return false
      if (filters.severity && d.severity !== filters.severity) return false
      return true
    })
  }, [discoveries, filters])

  const hasActiveFilters = filters.focusArea !== '' || filters.module !== '' || filters.severity !== ''

  const clearFilters = () => {
    setFilters({ focusArea: '', module: '', severity: '' })
  }

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
    { path: '/alert-analysis', label: 'Alert Analysis', icon: '⚡' },
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
                if (!isOnDiscoveriesPage && filteredDiscoveries.length > 0) {
                  navigate(`/alert-discoveries/${filteredDiscoveries[0]?.alert_id || ''}`)
                }
              }}
            >
              <span className="nav-icon">⚡</span>
              <span className="nav-label">Discoveries</span>
              <span className={`nav-badge ${hasActiveFilters ? 'filtered' : ''}`}>
                {hasActiveFilters ? `${filteredDiscoveries.length}/${discoveries.length}` : discoveries.length}
              </span>
              <button
                className="nav-refresh-icon"
                onClick={(e) => {
                  e.stopPropagation();
                  queryClient.refetchQueries({ queryKey: ['critical-discoveries-sidebar'] });
                  queryClient.refetchQueries({ queryKey: ['critical-discoveries'] });
                }}
                title="Refresh discoveries"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"></path>
                  <path d="M21 3v5h-5"></path>
                  <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"></path>
                  <path d="M3 21v-5h5"></path>
                </svg>
              </button>
              <span className="nav-chevron">{isDiscoveriesExpanded ? '▼' : '▶'}</span>
            </div>

            {/* Expandable Discovery List - Card Layout */}
            {isDiscoveriesExpanded && (
              <>
                {/* Sidebar Filters */}
                <SidebarFilters
                  filters={filters}
                  onFilterChange={setFilters}
                  onClearFilters={clearFilters}
                  focusAreaOptions={filterOptions.focusAreas}
                  moduleOptions={filterOptions.modules}
                  severityOptions={filterOptions.severities}
                  hasActiveFilters={hasActiveFilters}
                />

                <div className="discovery-cards-container">
                  {filteredDiscoveries.map((discovery) => (
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
                  {filteredDiscoveries.length === 0 && discoveries.length > 0 && (
                    <div className="no-results-message">
                      No discoveries match your filters
                    </div>
                  )}
                  {discoveries.length === 0 && (
                    <div className="discovery-card empty">
                      <span className="empty-text">No discoveries yet</span>
                    </div>
                  )}
                </div>
              </>
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
