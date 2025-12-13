# Alert Explanation Backend - Specification

**Feature:** 05-alert-explanation-backend  
**Frontend Feature:** [05-alert-explanation](../../../frontend/app_entry/features/alert-discoveries/05-alert-explanation/)  
**API Endpoint:** Part of `GET /alert-dashboard/critical-discoveries`  
**Status:** ✅ Working

---

## Requirements

### Functional Requirements

1. **Provide Business Purpose**
   - Return `business_purpose` field from `AlertInstance`
   - This comes from Explanation artifact files
   - Explains what the alert monitors and why it matters

### API Specification

**Endpoint:** `GET /alert-dashboard/critical-discoveries`

**Response Field:** `business_purpose` (in `CriticalDiscoveryDrilldown`)

```python
{
    "business_purpose": str | None  # From AlertInstance.business_purpose
}
```

---

## Expected Behavior

1. **Data Source**
   - `business_purpose` is stored in `AlertInstance` table
   - Populated from Explanation artifact during content analysis
   - May be `None` if not provided

2. **Inclusion in Response**
   - Included in `CriticalDiscoveryDrilldown` response
   - Available for all alerts returned by the endpoint

---

## Related Frontend Feature

The frontend displays `business_purpose` as the alert explanation below the title in the detail panel.

