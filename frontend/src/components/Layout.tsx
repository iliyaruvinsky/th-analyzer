import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import SkywindLogo from './SkywindLogo'
import './Layout.css'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '◆' },
    { path: '/upload', label: 'Upload', icon: '↑' },
    { path: '/alert-analysis', label: 'Alert Analysis', icon: '⚡' },
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
        </ul>

        {/* Footer */}
        <div className="sidebar-footer">
          <div className="app-version">THA v1.0</div>
        </div>
      </nav>
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}

export default Layout
