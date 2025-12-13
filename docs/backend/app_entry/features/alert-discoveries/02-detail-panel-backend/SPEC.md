# Detail Panel Backend - Specification

**Feature:** 02-detail-panel-backend  
**Frontend Feature:** [02-detail-panel](../../../frontend/app_entry/features/alert-discoveries/02-detail-panel/)  
**API Endpoint:** `GET /alert-dashboard/critical-discoveries`  
**Status:** ✅ Working

---

## Requirements

### Functional Requirements

1. **Provide Critical Discoveries with Drilldown**
   - Return alerts grouped by alert_id
   - Include all critical discoveries for each alert
   - Include concentration metrics
   - Include key findings
   - Include summary data from AlertAnalysis

2. **Support Filtering**
   - Limit number of results (default: 10, max: 100)
   - Order by financial impact (descending)

3. **Include Alert Configuration**
   - Business purpose (from AlertInstance)
   - Parameters (from AlertInstance)
   - Module and focus area information

### API Specification

**Endpoint:** `GET /alert-dashboard/critical-discoveries`

**Query Parameters:**

- `limit` (int, optional): Number of results to return (default: 10, min: 1, max: 100)

**Response Model:** `List[CriticalDiscoveryDrilldown]`

```python
[
    {
        "alert_id": str,
        "alert_name": str,
        "module": str,
        "focus_area": str,
        "severity": str,
        "discovery_count": int,
        "financial_impact_usd": Decimal,
        "discoveries": List[CriticalDiscoveryResponse],
        "concentration_metrics": List[ConcentrationMetricResponse],
        "key_findings": List[KeyFindingResponse],
        "records_affected": int,
        "unique_entities": int,
        "period_start": date,
        "period_end": date,
        "risk_score": int,
        "raw_summary_data": Dict[str, Any],
        "business_purpose": str,
        "parameters": Dict[str, Any]
    }
]
```

---

## Expected Behavior

1. **Data Aggregation**
   - Query `AlertAnalysis` with `joinedload` for related data
   - Filter to only analyses with critical discoveries
   - Order by `financial_impact_usd` descending
   - Limit results

2. **Module Resolution**
   - Try to get module from `ExceptionIndicator` (via `AlertInstance.ei_id`)
   - Fall back to `AlertInstance.subcategory` if no EI linked
   - Default to "N/A" if neither available

3. **Performance**
   - Uses SQLAlchemy eager loading to avoid N+1 queries
   - Should handle large datasets efficiently

---

## Related Frontend Feature

The frontend `DiscoveryDetailPanel` component uses this endpoint to display detailed discovery information.
