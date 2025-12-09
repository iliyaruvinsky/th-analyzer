# KPI Specification Document - Treasure Hunt Analyzer

**Version**: 1.0.0
**Last Updated**: 2025-12-06
**Document Type**: Frontend Specification

---

## Purpose

This document consolidates all KPI definitions, dashboard specifications, and user interaction descriptions for the Treasure Hunt Analyzer (THA) frontend. It explains:
- **WHAT** is measured
- **HOW** it is measured
- **WHAT FUNCTIONALITY** it has in the application

---

## Dashboard Architecture

The unified dashboard uses a tabbed navigation structure:

```
+----------------------------------------------------------------+
|  TREASURE HUNT ANALYZER                                         |
+-----------------------------------------------------------------+
|  [ Overview ]  [ Alert Analysis ]  [ Action Queue ]             |
+-----------------------------------------------------------------+
|                                                                  |
|  TAB CONTENT AREA                                               |
|                                                                  |
+----------------------------------------------------------------+
```

### Data Sources

| Tab | API Endpoints | Refresh Interval |
|-----|---------------|------------------|
| Overview | `/api/v1/dashboard/kpis`, `/api/v1/analysis/findings` | 5 seconds |
| Alert Analysis | `/api/v1/alert-dashboard/kpis`, `/api/v1/alert-dashboard/critical-discoveries` | 10 seconds |
| Action Queue | `/api/v1/alert-dashboard/action-queue` | 10 seconds |

**Note**: Data only loads when the respective tab is active (conditional React Query).

---

## Tab 1: Overview

### Purpose
Summary view of all analyzed findings across the Treasure Hunt Analyzer. Shows aggregated KPIs, distribution by focus area and risk level, and a timeline of financial exposure trends.

### KPI Cards (4 total)

#### 1. Total Findings
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Count of all findings detected by the analysis pipeline |
| **Calculation** | `COUNT(findings.id)` |
| **Data Source** | `findings` table |
| **Display Format** | Integer |
| **Update Frequency** | Real-time (5s polling) |
| **User Interaction** | Display only |

#### 2. Average Risk Score
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Mean risk score across all risk assessments |
| **Calculation** | `AVG(risk_assessments.risk_score)` |
| **Data Source** | `risk_assessments` table |
| **Display Format** | Decimal (0-100 scale, 1 decimal place) |
| **Visual Indicator** | Color coded: 0-25 green, 26-50 yellow, 51-75 orange, 76-100 red |
| **Update Frequency** | Real-time (5s polling) |
| **User Interaction** | Display only |

#### 3. Total Financial Exposure
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Sum of all estimated money losses across findings |
| **Calculation** | `SUM(money_loss_calculations.estimated_loss)` |
| **Data Source** | `money_loss_calculations` table |
| **Display Format** | Currency (USD), formatted with Intl.NumberFormat |
| **Example** | $5,000,000 |
| **Update Frequency** | Real-time (5s polling) |
| **User Interaction** | Display only |

#### 4. Analysis Runs
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Total number of analysis pipeline executions |
| **Calculation** | `COUNT(analysis_runs.id)` |
| **Data Source** | `analysis_runs` table |
| **Display Format** | Integer |
| **Update Frequency** | Real-time (5s polling) |
| **User Interaction** | Display only |

### Charts

#### Focus Area Distribution
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Count of findings per focus area classification |
| **Categories** | BUSINESS_PROTECTION, BUSINESS_CONTROL, ACCESS_GOVERNANCE, TECHNICAL_CONTROL, JOBS_CONTROL, S/4HANA_EXCELLENCE |
| **Chart Type** | Horizontal bar chart |
| **Calculation** | `COUNT(findings.id) GROUP BY focus_area` |
| **User Interaction** | Hover for tooltip with exact count |

#### Risk Level Distribution
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Count of findings per severity level |
| **Categories** | CRITICAL, HIGH, MEDIUM, LOW |
| **Chart Type** | Pie chart or bar chart |
| **Calculation** | `COUNT(findings.id) GROUP BY severity` |
| **User Interaction** | Hover for tooltip with exact count |

#### Financial Exposure Timeline
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Financial exposure over time |
| **X-Axis** | Date/time |
| **Y-Axis** | USD amount |
| **Chart Type** | Line chart |
| **User Interaction** | Hover for tooltip with date and amount |

### Findings Table
| Column | Data Type | Description |
|--------|-----------|-------------|
| Title | String | Finding title/name |
| Focus Area | Badge | Classification category |
| Severity | Badge | CRITICAL/HIGH/MEDIUM/LOW |
| Risk Score | Number | 0-100 scale |
| Financial Impact | Currency | Estimated loss in USD |
| Status | Badge | OPEN/IN_REVIEW/REMEDIATED |
| Created Date | Date | When finding was created |

**User Interactions**:
- Click row to view finding details
- Sort by any column
- Filter by focus area, severity, status

---

## Tab 2: Alert Analysis

### Purpose
Detailed breakdown of 4C quantitative alerts processed through the analysis pipeline. Critical discoveries highlight high-risk findings that require immediate attention.

### KPI Cards (4 total)

#### 1. Critical Discoveries
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Count of high-priority findings flagged for investigation |
| **Calculation** | `COUNT(critical_discoveries.id)` |
| **Data Source** | `critical_discoveries` table |
| **Display Format** | Integer |
| **Significance** | These require immediate attention from analysts |
| **Update Frequency** | Real-time (10s polling when tab active) |

#### 2. Alerts Analyzed
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Number of distinct 4C alerts that have been processed |
| **Calculation** | `COUNT(DISTINCT alert_analyses.id)` |
| **Data Source** | `alert_analyses` table |
| **Display Format** | Integer |
| **Update Frequency** | Real-time (10s polling when tab active) |

#### 3. Financial Exposure (USD)
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Sum of all financial impacts from analyzed alerts |
| **Calculation** | `SUM(alert_analyses.financial_impact_usd)` |
| **Data Source** | `alert_analyses` table |
| **Display Format** | Currency (USD), Decimal precision |
| **Update Frequency** | Real-time (10s polling when tab active) |

#### 4. Avg Risk Score
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Average risk score across all alert analyses |
| **Calculation** | `AVG(alert_analyses.risk_score)` |
| **Data Source** | `alert_analyses` table |
| **Display Format** | Decimal (0-100 scale) |
| **Visual Indicator** | Color coded by risk level |
| **Update Frequency** | Real-time (10s polling when tab active) |

### Distribution Charts

#### By Severity
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Count of alerts per severity level |
| **Categories** | CRITICAL, HIGH, MEDIUM, LOW |
| **Calculation** | `COUNT(alert_analyses.id) GROUP BY severity` |
| **Chart Type** | Bar chart |

#### By SAP Module
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Count of alerts per source system module |
| **Categories** | FI (Finance), SD (Sales), MM (Materials), MD (Master Data), PUR (Purchasing), etc. |
| **Calculation** | `COUNT(alert_analyses.id) GROUP BY module` |
| **Chart Type** | Bar chart |

#### By Focus Area
| Attribute | Value |
|-----------|-------|
| **What It Measures** | Count of alerts per focus area classification |
| **Categories** | 6 focus area categories |
| **Calculation** | `COUNT(alert_analyses.id) GROUP BY focus_area` |
| **Chart Type** | Bar chart |

### Critical Discoveries Table

| Column | Data Type | Description |
|--------|-----------|-------------|
| Alert ID | String | Unique identifier (e.g., "200025_001455") |
| Alert Name | String | Descriptive name |
| Module | Badge | SAP module (FI, SD, MM, etc.) |
| Focus Area | Badge | Classification category |
| Severity | Badge | CRITICAL/HIGH/MEDIUM/LOW |
| Discovery Count | Integer | Number of findings for this alert |
| Financial Impact | Currency | Total USD impact |
| Avg Risk Score | Number | 0-100 scale |

**User Interactions**:
- Click row to expand inline OR open modal (configurable)
- View Mode Toggle: Modal view / Inline expansion
- Expanded view shows: detailed metrics, risk breakdown, action buttons

---

## Tab 3: Action Queue

### Purpose
Investigation and remediation tracking for identified issues. Items are prioritized P1-P5 (P1 = most critical). Users track progress through workflow statuses.

### Priority Definitions
| Priority | Color | Urgency | Expected Response Time |
|----------|-------|---------|----------------------|
| P1 | Red | Critical/Emergency | Within 24 hours |
| P2 | Orange | High | Within 48 hours |
| P3 | Yellow | Medium | Within 1 week |
| P4 | Green | Low | Within 2 weeks |
| P5 | Gray | Minimal | Best effort / Process improvement |

### Status Workflow
```
OPEN --> IN_REVIEW --> REMEDIATED
  |                       ^
  +---> FALSE_POSITIVE ---+
```

| Status | Description |
|--------|-------------|
| OPEN | New action item, not yet assigned or investigated |
| IN_REVIEW | Currently being investigated by an analyst |
| REMEDIATED | Issue has been resolved |
| FALSE_POSITIVE | Investigation determined this is not a real issue |

### Action Queue Fields

| Field | Data Type | Description | Required |
|-------|-----------|-------------|----------|
| **id** | Integer | Database identifier | Auto |
| **action_type** | Enum | IMMEDIATE / SHORT_TERM / PROCESS_IMPROVEMENT | Yes |
| **priority** | Integer | 1-5 (1 = highest priority) | Yes |
| **title** | String | Brief description of required action | Yes |
| **description** | Text | Detailed explanation and context | Yes |
| **status** | Enum | OPEN / IN_REVIEW / REMEDIATED / FALSE_POSITIVE | Yes |
| **assigned_to** | String | Person responsible (name or username) | No |
| **due_date** | Date | Expected completion date | No |
| **alert_analysis_id** | Integer | Link to source analysis | Yes |
| **created_at** | Timestamp | When item was created | Auto |
| **resolution_notes** | Text | Notes about how issue was resolved | No |
| **resolved_at** | Timestamp | When item was resolved | Auto |
| **resolved_by** | String | Person who resolved the item | No |

### Action Type Definitions

| Type | Description | Typical Priority |
|------|-------------|------------------|
| IMMEDIATE | Requires urgent investigation or action | P1-P2 |
| SHORT_TERM | Should be addressed within days/weeks | P2-P3 |
| PROCESS_IMPROVEMENT | Long-term process change to prevent recurrence | P4-P5 |

### User Interactions

1. **View Details**: Click to open modal with full context
2. **Assign**: Assign to a team member
3. **Change Status**: Update workflow status
4. **Add Notes**: Document investigation progress
5. **Filter by Status**: Show only OPEN, IN_REVIEW, etc.
6. **Sort by Priority**: Order by urgency

---

## API Response Schemas

### Dashboard KPIs Response (`/api/v1/dashboard/kpis`)
```json
{
  "total_findings": 42,
  "total_risk_score": 67.5,
  "total_money_loss": 5000000.00,
  "analysis_runs": 15
}
```

### Alert Dashboard KPIs Response (`/api/v1/alert-dashboard/kpis`)
```json
{
  "total_critical_discoveries": 5,
  "total_alerts_analyzed": 12,
  "total_financial_exposure_usd": "5000000.00",
  "avg_risk_score": 75.0,
  "alerts_by_severity": {
    "CRITICAL": 2,
    "HIGH": 5,
    "MEDIUM": 3,
    "LOW": 2
  },
  "alerts_by_focus_area": {
    "BUSINESS_PROTECTION": 3,
    "BUSINESS_CONTROL": 5,
    "ACCESS_GOVERNANCE": 2,
    "TECHNICAL_CONTROL": 1,
    "JOBS_CONTROL": 1
  },
  "alerts_by_module": {
    "FI": 4,
    "SD": 3,
    "MM": 3,
    "MD": 2
  },
  "open_investigations": 3,
  "open_action_items": 8
}
```

### Critical Discovery Response
```json
{
  "alert_id": "200025_001455",
  "alert_name": "Comparison of monthly sales volume",
  "module": "SD",
  "focus_area": "BUSINESS_CONTROL",
  "severity": "HIGH",
  "discovery_count": 15,
  "financial_impact_usd": "2500000.00",
  "avg_risk_score": 72.5
}
```

### Action Item Response
```json
{
  "id": 1,
  "alert_analysis_id": 5,
  "action_type": "IMMEDIATE",
  "priority": 2,
  "title": "Investigate suspicious vendor payment pattern",
  "description": "Multiple payments to vendor KAMURU TRADING detected with unusual patterns...",
  "status": "OPEN",
  "assigned_to": null,
  "due_date": "2025-12-10",
  "resolution_notes": null,
  "resolved_at": null,
  "resolved_by": null,
  "created_at": "2025-12-05T10:30:00Z"
}
```

---

## Visual Component Mapping

| Data | Component | File Location |
|------|-----------|---------------|
| KPI Cards | `<div className="kpi-card">` | Dashboard.tsx |
| Distribution Charts | Recharts BarChart/PieChart | Dashboard.tsx |
| Findings Table | HTML table | Dashboard.tsx |
| Critical Discoveries Table | HTML table with expansion | Dashboard.tsx |
| Action Queue | Card-based layout | Dashboard.tsx |
| Discovery Detail Panel | DiscoveryDetailPanel | components/DiscoveryDetailPanel.tsx |
| Action Item Modal | ActionItemModal | components/ActionItemModal.tsx |
| Tab Navigation | DashboardTabs | components/DashboardTabs.tsx |

---

## Frontend Files Reference

| File | Purpose |
|------|---------|
| `frontend/src/pages/Dashboard.tsx` | Main dashboard with tabbed navigation |
| `frontend/src/pages/AlertDashboard.css` | Styles for alert analysis components |
| `frontend/src/styles/dashboard.css` | Core dashboard styles |
| `frontend/src/components/DashboardTabs.tsx` | Tab navigation component |
| `frontend/src/components/DiscoveryDetailPanel.tsx` | Discovery drilldown view |
| `frontend/src/components/ActionItemModal.tsx` | Action item detail modal |
| `frontend/src/services/api.ts` | API client functions |

---

## Backend Files Reference

| File | Purpose |
|------|---------|
| `backend/app/api/dashboard.py` | Main dashboard endpoints |
| `backend/app/api/alert_dashboard.py` | Alert dashboard endpoints |
| `backend/app/schemas/dashboard.py` | Dashboard response schemas |
| `backend/app/schemas/alert_dashboard.py` | Alert dashboard schemas |
| `backend/app/models/` | SQLAlchemy ORM models |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-06 | 1.0.0 | Initial consolidated documentation |
