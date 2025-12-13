# Concentration Metrics Backend - Specification

**Feature:** 08-concentration-metrics-backend  
**Frontend Feature:** [08-concentration-metrics](../../../frontend/app_entry/features/alert-discoveries/08-concentration-metrics/)  
**API Endpoint:** Part of `GET /alert-dashboard/critical-discoveries`  
**Status:** ✅ Working

---

## Requirements

### Functional Requirements

1. **Provide Concentration Metrics**
   - Return `concentration_metrics` array from `AlertAnalysis`
   - Contains metrics showing concentration patterns
   - Includes dimension type, code, name, counts, values, percentages

### API Specification

**Endpoint:** `GET /alert-dashboard/critical-discoveries`

**Response Field:** `concentration_metrics` (in `CriticalDiscoveryDrilldown`)

```python
{
    "concentration_metrics": List[ConcentrationMetricResponse]
}
```

**ConcentrationMetricResponse:**
```python
{
    "id": int,
    "alert_analysis_id": int,
    "dimension_type": str,  # SALES_ORG, CUSTOMER, REGION, etc.
    "dimension_code": str,
    "dimension_name": str,
    "record_count": int,
    "value_local": Decimal,
    "value_usd": Decimal,
    "percentage_of_total": Decimal,
    "rank": int,
    "created_at": datetime
}
```

---

## Expected Behavior

1. **Data Source**
   - Stored in `ConcentrationMetric` table
   - Linked to `AlertAnalysis` via `alert_analysis_id`
   - Created during content analysis

2. **Inclusion in Response**
   - Included in `CriticalDiscoveryDrilldown` response
   - Eager loaded via `joinedload(AlertAnalysis.concentration_metrics)`
   - May be empty list `[]` if no metrics

---

## Related Frontend Feature

The frontend displays concentration metrics in a table. Currently, frontend may silently fail if data is missing.

