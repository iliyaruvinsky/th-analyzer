# Alert Discoveries Entry - Backend Documentation

**Last Updated:** 2025-12-12  
**Status:** ⚠️ Partially Working - Multiple backend features need fixes  
**API Prefix:** `/alert-dashboard`

---

## Overview

The Alert Discoveries backend provides API endpoints and services for managing critical discoveries from analyzed alerts. This documentation maps backend features to frontend features and tracks development status.

---

## Feature List

| # | Feature | Frontend Feature | Backend Endpoint | Status | Documentation |
|---|---------|-----------------|------------------|--------|---------------|
| 01 | [AlertSummary KPI Backend](01-alert-summary-backend/) | 01-alert-summary | `GET /alert-dashboard/kpis` | ⚠️ Working | [SPEC](01-alert-summary-backend/SPEC.md) \| [ANALYSIS](01-alert-summary-backend/ANALYSIS.md) \| [CODE](01-alert-summary-backend/CODE.md) |
| 02 | [Detail Panel Backend](02-detail-panel-backend/) | 02-detail-panel | `GET /alert-dashboard/critical-discoveries` | ⚠️ Working | [SPEC](02-detail-panel-backend/SPEC.md) \| [ANALYSIS](02-detail-panel-backend/ANALYSIS.md) \| [CODE](02-detail-panel-backend/CODE.md) |
| 03 | [Auto-Navigation Backend](03-auto-navigation-backend/) | 03-auto-navigation | N/A (Frontend only) | ✅ N/A | [SPEC](03-auto-navigation-backend/SPEC.md) \| [ANALYSIS](03-auto-navigation-backend/ANALYSIS.md) \| [CODE](03-auto-navigation-backend/CODE.md) |
| 04 | [Create Action Item Backend](04-create-action-item-backend/) | 04-create-action-item | `POST /alert-dashboard/action-items` | ⚠️ Working | [SPEC](04-create-action-item-backend/SPEC.md) \| [ANALYSIS](04-create-action-item-backend/ANALYSIS.md) \| [CODE](04-create-action-item-backend/CODE.md) |
| 05 | [Alert Explanation Backend](05-alert-explanation-backend/) | 05-alert-explanation | Part of `GET /alert-dashboard/critical-discoveries` | ⚠️ Working | [SPEC](05-alert-explanation-backend/SPEC.md) \| [ANALYSIS](05-alert-explanation-backend/ANALYSIS.md) \| [CODE](05-alert-explanation-backend/CODE.md) |
| 06 | [JSON Data Backend](06-json-data-backend/) | 06-json-popovers | Part of `GET /alert-dashboard/critical-discoveries` | ⚠️ Working | [SPEC](06-json-data-backend/SPEC.md) \| [ANALYSIS](06-json-data-backend/ANALYSIS.md) \| [CODE](06-json-data-backend/CODE.md) |
| 07 | [Risk Score Backend](07-risk-score-backend/) | 07-risk-score | Part of `GET /alert-dashboard/critical-discoveries` | ⚠️ Working | [SPEC](07-risk-score-backend/SPEC.md) \| [ANALYSIS](07-risk-score-backend/ANALYSIS.md) \| [CODE](07-risk-score-backend/CODE.md) |
| 08 | [Concentration Metrics Backend](08-concentration-metrics-backend/) | 08-concentration-metrics | Part of `GET /alert-dashboard/critical-discoveries` | ⚠️ Working | [SPEC](08-concentration-metrics-backend/SPEC.md) \| [ANALYSIS](08-concentration-metrics-backend/ANALYSIS.md) \| [CODE](08-concentration-metrics-backend/CODE.md) |
| 09 | [Key Findings Backend](09-key-findings-backend/) | 09-key-findings | Part of `GET /alert-dashboard/critical-discoveries` | ⚠️ Working | [SPEC](09-key-findings-backend/SPEC.md) \| [ANALYSIS](09-key-findings-backend/ANALYSIS.md) \| [CODE](09-key-findings-backend/CODE.md) |

---

## Code Structure

```
backend/app/
├── api/
│   └── alert_dashboard.py          # Main API endpoints
├── models/
│   ├── critical_discovery.py       # CriticalDiscovery model
│   ├── alert_analysis.py           # AlertAnalysis model
│   ├── alert_instance.py           # AlertInstance model
│   ├── key_finding.py              # KeyFinding model
│   ├── concentration_metric.py     # ConcentrationMetric model
│   └── action_item.py              # ActionItem model
├── schemas/
│   └── alert_dashboard.py          # Pydantic schemas
└── services/
    └── content_analyzer/            # Creates discoveries from alerts
        ├── analyzer.py             # Main orchestrator
        └── (other service files)
```

---

## API Endpoints Summary

### Main Endpoints

- `GET /alert-dashboard/kpis` - Dashboard KPI metrics
- `GET /alert-dashboard/critical-discoveries` - Get discoveries with drilldown
- `POST /alert-dashboard/action-items` - Create action items
- `GET /alert-dashboard/action-queue` - Get action queue

### Supporting Endpoints

- `GET /alert-dashboard/analyses/{analysis_id}` - Get full analysis details
- `POST /alert-dashboard/critical-discoveries/bulk` - Bulk create discoveries
- `POST /alert-dashboard/key-findings/bulk` - Bulk create key findings
- `POST /alert-dashboard/concentration-metrics/bulk` - Bulk create metrics

---

## Data Flow

```
Content Analyzer Service
    ↓
Creates AlertInstance, AlertAnalysis
    ↓
Creates CriticalDiscovery, KeyFinding, ConcentrationMetric
    ↓
Stored in Database
    ↓
API Endpoints Query Database
    ↓
Returns to Frontend
```

---

## Known Issues Summary

**Critical Issues:**
- Data completeness depends on content analyzer service
- Missing error handling for null/empty data
- No validation for required relationships

**High Priority:**
- Client-side aggregation in frontend (should use backend KPIs)
- Missing data handling in responses
- No pagination for large result sets

---

## Related Documentation

- **[DEVELOPMENT_STATE.md](DEVELOPMENT_STATE.md)** - Current backend development status ⭐
- [Frontend Documentation](../../../frontend/app_entry/features/alert-discoveries/README.md) - Corresponding frontend features
- [FEATURES.md](../../../FEATURES.md) - Overall feature inventory
- [llm_handover.md](../../../../llm_handover.md) - Project handover document

---

## Development Workflow

When working on a backend feature:

1. Read the feature's SPEC.md to understand API requirements
2. Read ANALYSIS.md to see current issues
3. Check CODE.md for code locations (api/, models/, schemas/, services/)
4. Make changes in appropriate backend files
5. Update ANALYSIS.md with fixes
6. Update CODE.md if structure changes
7. Test API endpoints via Swagger UI (`/docs`)

