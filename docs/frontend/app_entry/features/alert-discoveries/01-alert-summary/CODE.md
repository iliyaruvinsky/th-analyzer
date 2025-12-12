# AlertSummary Header with KPI Cards - Code Reference

**Feature:** 01-alert-summary  
**Component:** `AlertSummary`

---

## File Locations

### Main Component

- **File:** `frontend/src/pages/alert-discoveries/features/alert-summary/AlertSummary.tsx`
- **Export:** `frontend/src/pages/alert-discoveries/features/alert-summary/index.ts`

### Usage

**In AlertDiscoveries.tsx:**

```typescript
import AlertSummary from './alert-discoveries/features/alert-summary';

<AlertSummary discoveries={discoveries} currencyFormatter={currencyFormatter} />
```

**In Dashboard.tsx:**

- Not currently used (uses different KPI source)

---

## Component Structure

```typescript
interface AlertSummaryProps {
  discoveries: CriticalDiscoveryDrilldown[];
  currencyFormatter: Intl.NumberFormat;
}
```

### Key Functions

1. **KPI Calculation** (lines 11-28)
   - `totalDiscoveries` - Count from array length
   - `totalFinancialExposure` - Sum of `financial_impact_usd`
   - `severityCounts` - Reduce to count by severity
   - `moduleCounts` - Reduce to count by module

2. **Rendering** (lines 33-74)
   - KPI cards with values
   - Severity badges
   - Module badges

---

## Dependencies

- `CriticalDiscoveryDrilldown` type from `services/api`
- CSS classes from `AlertDashboard.css`:
  - `.alert-summary-header`
  - `.alert-summary-kpis`
  - `.summary-kpi`
  - `.severity-badge`
  - `.module-badge`

---

## API Calls

**Current:** None (uses passed props)  
**Should Use:** `GET /alert-dashboard/kpis` for authoritative data

---

## Related Files

- `frontend/src/pages/AlertDiscoveries.tsx` - Main page using component
- `frontend/src/pages/AlertDashboard.css` - Styles (lines 3475-3615)
