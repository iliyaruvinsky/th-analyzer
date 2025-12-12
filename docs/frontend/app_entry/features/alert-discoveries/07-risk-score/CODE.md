# Risk Score Explanation - Code Reference

**Feature:** 07-risk-score  
**Location:** `DiscoveryDetailPanel` component

---

## File Locations

### Implementation

- **File:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`
- **Lines:** 242-265

### Usage

**In DiscoveryDetailPanel.tsx:**
```typescript
// KPI metrics block (lines 194-268)
{hasDiscoveries && (
  <div className="kpi-metrics-block">
    {/* Risk score display */}
    {discovery.risk_score && (
      <div className="kpi-metric-card accent">
        <span className="kpi-metric-value">{discovery.risk_score}</span>
        <span className="kpi-metric-label">RISK SCORE</span>
      </div>
    )}
    
    {/* Hardcoded explanation */}
    <div className="kpi-explanations">
      {discovery.risk_score && discovery.risk_score >= 70 && (
        <p className="risk-warning">...</p>
      )}
    </div>
  </div>
)}
```

---

## Data Source

**Field:** `discovery.risk_score`  
**Type:** `number | null | undefined`  
**Source:** `AlertAnalysis.risk_score` from backend

**Backend:** `backend/app/api/alert_dashboard.py` (line 190)

---

## Related Documentation

- `docs/scoring-rules/BUSINESS_PROTECTION.md` - Scoring methodology
- Should link to this for real explanation

---

## CSS Classes

- `.kpi-metrics-block` - Container
- `.kpi-metric-card` - Score card
- `.kpi-explanations` - Explanation text
- `.risk-warning` - High risk styling

**Location:** `frontend/src/pages/AlertDashboard.css`

