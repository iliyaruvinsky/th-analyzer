# Risk Score Backend - Specification

**Feature:** 07-risk-score-backend  
**Frontend Feature:** [07-risk-score](../../../frontend/app_entry/features/alert-discoveries/07-risk-score/)  
**API Endpoint:** Part of `GET /alert-dashboard/critical-discoveries`  
**Status:** ✅ Working

---

## Requirements

### Functional Requirements

1. **Provide Risk Score**
   - Return `risk_score` field from `AlertAnalysis`
   - Integer value 0-100
   - Calculated during content analysis

### API Specification

**Endpoint:** `GET /alert-dashboard/critical-discoveries`

**Response Field:** `risk_score` (in `CriticalDiscoveryDrilldown`)

```python
{
    "risk_score": int | None  # 0-100, from AlertAnalysis.risk_score
}
```

---

## Expected Behavior

1. **Data Source**
   - `risk_score` is stored in `AlertAnalysis` table
   - Calculated by content analyzer service
   - May be `None` if not calculated

2. **Inclusion in Response**
   - Included in `CriticalDiscoveryDrilldown` response
   - Available for all alerts returned by the endpoint

---

## Related Frontend Feature

The frontend displays `risk_score` with a "Risk Score Explanation" section. Currently, the explanation is just categorization, not a real explanation.

