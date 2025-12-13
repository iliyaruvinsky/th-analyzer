# Key Findings Backend - Specification

**Feature:** 09-key-findings-backend  
**Frontend Feature:** [09-key-findings](../../../frontend/app_entry/features/alert-discoveries/09-key-findings/)  
**API Endpoint:** Part of `GET /alert-dashboard/critical-discoveries`  
**Status:** ✅ Working

---

## Requirements

### Functional Requirements

1. **Provide Key Findings**
   - Return `key_findings` array from `AlertAnalysis`
   - Contains top findings (ranked 1, 2, 3)
   - Includes finding text, category, financial impact

### API Specification

**Endpoint:** `GET /alert-dashboard/critical-discoveries`

**Response Field:** `key_findings` (in `CriticalDiscoveryDrilldown`)

```python
{
    "key_findings": List[KeyFindingResponse]
}
```

**KeyFindingResponse:**
```python
{
    "id": int,
    "alert_analysis_id": int,
    "finding_rank": int,  # 1, 2, 3
    "finding_text": str,
    "finding_category": str,  # Concentration, Anomaly, Data Quality, Process Gap
    "financial_impact_usd": Decimal,
    "created_at": datetime
}
```

---

## Expected Behavior

1. **Data Source**
   - Stored in `KeyFinding` table
   - Linked to `AlertAnalysis` via `alert_analysis_id`
   - Created during content analysis

2. **Inclusion in Response**
   - Included in `CriticalDiscoveryDrilldown` response
   - Eager loaded via `joinedload(AlertAnalysis.key_findings)`
   - May be empty list `[]` if no findings

---

## Related Frontend Feature

The frontend displays key findings in a list. Currently, frontend may silently fail if data is missing.

