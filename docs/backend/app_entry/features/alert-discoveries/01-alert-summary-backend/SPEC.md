# AlertSummary KPI Backend - Specification

**Feature:** 01-alert-summary-backend  
**Frontend Feature:** [01-alert-summary](../../../frontend/app_entry/features/alert-discoveries/01-alert-summary/)  
**API Endpoint:** `GET /alert-dashboard/kpis`  
**Status:** ✅ Working

---

## Requirements

### Functional Requirements

1. **Provide Dashboard KPI Metrics**
   - Total critical discoveries count
   - Total alerts analyzed count
   - Total financial exposure (USD)
   - Average risk score (0-100)

2. **Provide Distribution Breakdowns**
   - Alerts by severity (CRITICAL, HIGH, MEDIUM, LOW)
   - Alerts by focus area (BUSINESS_PROTECTION, etc.)
   - Alerts by module (FI, SD, MM, MD, PUR)

3. **Provide Action Queue Metrics**
   - Open investigations count (fraud_indicator == "INVESTIGATE")
   - Open action items count (status == "OPEN")

### API Specification

**Endpoint:** `GET /alert-dashboard/kpis`

**Response Model:** `DashboardKPIsResponse`

```python
{
    "total_critical_discoveries": int,
    "total_alerts_analyzed": int,
    "total_financial_exposure_usd": Decimal,
    "avg_risk_score": float,
    "alerts_by_severity": {
        "CRITICAL": int,
        "HIGH": int,
        "MEDIUM": int,
        "LOW": int
    },
    "alerts_by_focus_area": Dict[str, int],
    "alerts_by_module": Dict[str, int],
    "open_investigations": int,
    "open_action_items": int
}
```

### Data Sources

- `CriticalDiscovery` table - for total discoveries count
- `AlertAnalysis` table - for alerts analyzed, financial exposure, risk scores
- `AlertInstance` table - for focus area and module distribution
- `ActionItem` table - for action queue metrics

---

## Expected Behavior

1. **Aggregation Logic**
   - Count all `CriticalDiscovery` records
   - Count all `AlertAnalysis` records
   - Sum `financial_impact_usd` from `AlertAnalysis`
   - Calculate average `risk_score` from `AlertAnalysis`

2. **Distribution Calculations**
   - Group `AlertAnalysis` by `severity` field
   - Join `AlertAnalysis` → `AlertInstance` to get `focus_area`
   - Join `AlertAnalysis` → `AlertInstance` → `ExceptionIndicator` to get `module` (or use `subcategory`)

3. **Performance**
   - Should use efficient SQL aggregations
   - Should handle null/empty data gracefully
   - Should return quickly (< 500ms)

---

## Related Frontend Feature

The frontend `AlertSummary` component should use this endpoint instead of client-side aggregation. Currently, frontend aggregates data from `critical-discoveries` endpoint, which is inefficient.

