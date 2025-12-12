# Concentration Metrics - Code Reference

**Feature:** 08-concentration-metrics  
**Location:** `DiscoveryDetailPanel` component

---

## File Locations

### Implementation

- **File:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`
- **Lines:** 271-312

### Usage

**In DiscoveryDetailPanel.tsx:**
```typescript
{discovery.concentration_metrics && discovery.concentration_metrics.length > 0 && (
  <div className="concentration-block">
    <h4 className="concentration-title">CONCENTRATION PATTERN</h4>
    <table className="concentration-table">
      {/* Table rows */}
    </table>
    <div className="concentration-explanation">
      {/* Explanation text */}
    </div>
  </div>
)}
```

---

## Data Source

**Field:** `discovery.concentration_metrics`  
**Type:** `ConcentrationMetric[]`  
**Source:** `AlertAnalysis.concentration_metrics` from backend

**Backend:** `backend/app/api/alert_dashboard.py` (lines 177-180)

---

## Data Structure

```typescript
interface ConcentrationMetric {
  id: number;
  dimension_name?: string;
  dimension_code?: string;
  record_count: number;
  percentage_of_total: number;
  rank?: number;
}
```

---

## CSS Classes

- `.concentration-block` - Container
- `.concentration-table` - Table
- `.concentration-explanation` - Explanation text
- `.entity-cell` - Entity name cell
- `.percent-cell` - Percentage cell

**Location:** `frontend/src/pages/AlertDashboard.css`

