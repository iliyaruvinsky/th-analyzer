# AlertSummary Header with KPI Cards - Specification

**Feature:** 01-alert-summary  
**Component:** `AlertSummary`  
**Status:** ⚠️ Simulated (client-side aggregation)

---

## Requirements

### Functional Requirements

1. **Display KPI Summary Cards**
   - Total Alerts count
   - Total Financial Exposure (sum of all discoveries)
   - Severity breakdown (Critical, High, Medium, Low counts)
   - SAP Modules breakdown (FI, MM, SD, etc.)

2. **Data Source**
   - Should use authoritative backend data
   - Should refresh in real-time
   - Should match backend calculations

3. **Visual Design**
   - Clean, professional KPI cards
   - Color-coded severity badges
   - Module badges with counts

---

## Expected Behavior

- KPI values should match backend calculations exactly
- Updates should reflect real-time changes
- Empty states should be handled gracefully
- Loading states should be shown during data fetch

---

## Current Implementation Issues

See [ANALYSIS.md](ANALYSIS.md) for detailed issues.

**Key Problems:**

- Client-side aggregation instead of backend data
- 30s staleTime prevents real-time updates
- May not match backend reality

---

## Related Features

- Part of Alert Discoveries entry
- Used in Dashboard Alerts tab
- Displays data from `GET /alert-dashboard/critical-discoveries`
