# Risk Score Backend - Code References

**Feature:** 07-risk-score-backend  
**Last Updated:** 2025-12-12

---

## Code Locations

### API Endpoint

**File:** `backend/app/api/alert_dashboard.py`

**Field Inclusion:**
```190:190:backend/app/api/alert_dashboard.py
risk_score=analysis.risk_score,
```

### Schema Definition

**File:** `backend/app/schemas/alert_dashboard.py`

**Field in Response Schema:**
```339:339:backend/app/schemas/alert_dashboard.py
risk_score: Optional[int] = None
```

### Database Model

**File:** `backend/app/models/alert_analysis.py`

**Field Definition:**
- `risk_score` column in `AlertAnalysis` table (Integer, 0-100)

### Content Analyzer Service

**File:** `backend/app/services/content_analyzer/`

**Calculated by:** Content analyzer service calculates risk score during analysis

---

## Related Code

### Frontend Usage

**Used by:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`

The frontend displays `risk_score` with explanation (currently just categorization).

