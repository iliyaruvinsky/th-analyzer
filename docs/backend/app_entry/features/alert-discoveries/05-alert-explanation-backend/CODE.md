# Alert Explanation Backend - Code References

**Feature:** 05-alert-explanation-backend  
**Last Updated:** 2025-12-12

---

## Code Locations

### API Endpoint

**File:** `backend/app/api/alert_dashboard.py`

**Field Inclusion:**
```193:193:backend/app/api/alert_dashboard.py
business_purpose=alert_instance.business_purpose if alert_instance else None,
```

### Schema Definition

**File:** `backend/app/schemas/alert_dashboard.py`

**Field in Response Schema:**
```342:342:backend/app/schemas/alert_dashboard.py
business_purpose: Optional[str] = None  # From Explanation_* file
```

### Database Model

**File:** `backend/app/models/alert_instance.py`

**Field Definition:**
- `business_purpose` column in `AlertInstance` table

### Content Analyzer Service

**File:** `backend/app/services/content_analyzer/` (various files)

**Populated by:** Content analyzer service reads Explanation artifacts and stores in `AlertInstance.business_purpose`

---

## Related Code

### Frontend Usage

**Used by:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`

The frontend displays `discovery.business_purpose` as the alert explanation.

