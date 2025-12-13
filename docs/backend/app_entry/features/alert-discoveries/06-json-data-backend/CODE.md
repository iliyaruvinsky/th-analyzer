# JSON Data Backend - Code References

**Feature:** 06-json-data-backend  
**Last Updated:** 2025-12-12

---

## Code Locations

### API Endpoint

**File:** `backend/app/api/alert_dashboard.py`

**Field Inclusion:**
```191:194:backend/app/api/alert_dashboard.py
raw_summary_data=analysis.raw_summary_data,
# Alert configuration from AlertInstance
business_purpose=alert_instance.business_purpose if alert_instance else None,
parameters=alert_instance.parameters if alert_instance else None
```

### Schema Definition

**File:** `backend/app/schemas/alert_dashboard.py`

**Fields in Response Schema:**
```340:343:backend/app/schemas/alert_dashboard.py
raw_summary_data: Optional[Dict[str, Any]] = None
# Alert configuration from AlertInstance
business_purpose: Optional[str] = None  # From Explanation_* file
parameters: Optional[Dict[str, Any]] = None  # From Metadata_* file
```

### Database Models

**File:** `backend/app/models/alert_analysis.py`
- `raw_summary_data` column in `AlertAnalysis` table

**File:** `backend/app/models/alert_instance.py`
- `parameters` column in `AlertInstance` table

---

## Related Code

### Frontend Usage

**Used by:** `frontend/src/pages/alert-discoveries/features/json-popovers/JsonDataPopover.tsx`

The frontend displays these fields in JSON popovers.

