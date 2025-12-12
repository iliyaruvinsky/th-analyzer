# Alert Explanation (business_purpose) - Code Reference

**Feature:** 05-alert-explanation  
**Location:** `DiscoveryDetailPanel` component

---

## File Locations

### Implementation

- **File:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`
- **Lines:** 60-65

### Usage

**In DiscoveryDetailPanel.tsx:**
```typescript
{discovery.business_purpose && (
  <div className="discovery-explanation-box-inline">
    <span className="explanation-icon">ℹ</span>
    <span className="explanation-text">{discovery.business_purpose}</span>
  </div>
)}
```

---

## Data Source

**Field:** `discovery.business_purpose`  
**Type:** `string | null | undefined`  
**Source:** `alert_instance.business_purpose` from backend

**Backend:** `backend/app/api/alert_dashboard.py` (line 193)

---

## CSS Classes

- `.discovery-explanation-box-inline` - Container
- `.explanation-icon` - Info icon
- `.explanation-text` - Text content

**Location:** `frontend/src/pages/AlertDashboard.css`

---

## Related Features

- Part of detail panel header
- Used alongside Output/Params buttons
- Related to alert explanation from Explanation_* files

