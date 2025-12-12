# AlertSummary Header with KPI Cards - Analysis

**Feature:** 01-alert-summary  
**Date:** 2025-12-11  
**Status:** ⚠️ Simulated (not using authoritative backend data)

---

## Current State

### What Works

- ✅ Component renders and displays KPIs
- ✅ Shows: Total Alerts, Financial Exposure, Severity breakdown, SAP Modules
- ✅ Visual design is clean and professional

### Issues Identified

1. **Client-Side Aggregation**
   - KPIs calculated from `discoveries` array in frontend
   - Not using authoritative backend endpoint
   - May not match backend calculations

2. **Stale Data**
   - Uses `staleTime: 30000` (30 seconds)
   - No real-time updates
   - User may see outdated information

3. **Financial Exposure Calculation**
   - Sums `financial_impact_usd` from discovery objects
   - May not match backend aggregation
   - No validation against backend totals

4. **Severity Counts**
   - Derived from discovery objects
   - Not from authoritative source
   - May be inconsistent with backend

---

## Code Location

**Component:** `frontend/src/pages/alert-discoveries/features/alert-summary/AlertSummary.tsx`

**Key Code:**

```typescript
// Client-side aggregation (lines 11-28)
const totalDiscoveries = discoveries.length;
const totalFinancialExposure = discoveries.reduce((sum, d) => {
  const val = d.financial_impact_usd ? parseFloat(d.financial_impact_usd) : 0;
  return sum + val;
}, 0);
```

---

## Recommendations

1. **Use Backend KPIs Endpoint**
   - Call `GET /alert-dashboard/kpis` instead of calculating client-side
   - Ensure data matches backend reality

2. **Real-Time Updates**
   - Reduce staleTime or use real-time polling
   - Invalidate queries on data changes

3. **Validation**
   - Compare client calculations with backend
   - Show warnings if mismatch detected

---

## Related Documentation

- [SPEC.md](SPEC.md) - Requirements
- [CODE.md](CODE.md) - Code structure
