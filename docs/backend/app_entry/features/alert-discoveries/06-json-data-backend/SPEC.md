# JSON Data Backend - Specification

**Feature:** 06-json-data-backend  
**Frontend Feature:** [06-json-popovers](../../../frontend/app_entry/features/alert-discoveries/06-json-popovers/)  
**API Endpoint:** Part of `GET /alert-dashboard/critical-discoveries`  
**Status:** ✅ Working

---

## Requirements

### Functional Requirements

1. **Provide Raw Summary Data**
   - Return `raw_summary_data` field from `AlertAnalysis`
   - Contains structured data from Summary artifact

2. **Provide Parameters**
   - Return `parameters` field from `AlertInstance`
   - Contains alert configuration from Metadata artifact

### API Specification

**Endpoint:** `GET /alert-dashboard/critical-discoveries`

**Response Fields:** (in `CriticalDiscoveryDrilldown`)

```python
{
    "raw_summary_data": Dict[str, Any] | None,  # From AlertAnalysis.raw_summary_data
    "parameters": Dict[str, Any] | None  # From AlertInstance.parameters
}
```

---

## Expected Behavior

1. **Raw Summary Data**
   - Stored in `AlertAnalysis.raw_summary_data`
   - Contains structured data from Summary artifact
   - May be `None` if not populated

2. **Parameters**
   - Stored in `AlertInstance.parameters`
   - Contains alert configuration from Metadata artifact
   - May be `None` if not provided

---

## Related Frontend Feature

The frontend displays these fields in JSON popovers ("Output" and "Params" buttons).

