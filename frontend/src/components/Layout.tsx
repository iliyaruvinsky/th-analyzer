import React from 'react'
import { Link, useLocation } from 'react-router-dom'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/upload', label: 'Upload' },
    { path: '/alert-analysis', label: 'Alert Analysis' },
    { path: '/findings', label: 'Findings' },
    { path: '/reports', label: 'Reports' },
    { path: '/maintenance', label: 'Maintenance' },
    { path: '/logs', label: 'Logs' },
  ]

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <nav style={{
        width: '200px',
        backgroundColor: '#2c3e50',
        color: 'white',
        padding: '20px'
      }}>
        <h2 style={{ marginBottom: '30px' }}>THA</h2>
        <ul style={{ listStyle: 'none' }}>
          {navItems.map(item => (
            <li key={item.path} style={{ marginBottom: '10px' }}>
              <Link
                to={item.path}
                style={{
                  color: location.pathname === item.path ? '#3498db' : 'white',
                  textDecoration: 'none',
                  display: 'block',
                  padding: '10px',
                  borderRadius: '4px',
                  backgroundColor: location.pathname === item.path ? '#34495e' : 'transparent'
                }}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
      <main style={{ flex: 1, padding: '20px', backgroundColor: '#ecf0f1' }}>
        {children}
      </main>
    </div>
  )
}

export default Layout

