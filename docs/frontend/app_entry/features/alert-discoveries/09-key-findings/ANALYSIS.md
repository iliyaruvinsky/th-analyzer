# Key Findings - Analysis

**Feature:** 09-key-findings  
**Date:** 2025-12-11  
**Status:** ⚠️ Silently fails

---

## Current State

### What Works

- ✅ Table displays when data exists
- ✅ Shows: Rank (#), Finding text, Category
- ✅ Sorted by `finding_rank`
- ✅ Falls back to count in KPI metrics

### Issues Identified

1. **Silent Failure**
   - Table only renders if `discovery.key_findings.length > 0`
   - No indication when data is missing
   - Section just doesn't appear

2. **Missing Link**
   - No link to full analysis report
   - No indication of data source
   - User can't access detailed findings

3. **Fallback Behavior**
   - Falls back to showing count in KPI metrics (line 235)
   - Not ideal - should show table or message
   - Confusing for users

---

## Code Location

**Component:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`

**Key Code:**
```typescript
// Conditional rendering (lines 161-187)
{discovery.key_findings && discovery.key_findings.length > 0 && (
  <div className="findings-block">
    <h4 className="findings-title">KEY FINDINGS</h4>
    <table className="findings-table">
      {/* Table rows */}
    </table>
  </div>
)}

// Fallback in KPI metrics (line 235)
const findingsCount = discovery.key_findings?.length || discovery.discovery_count || 0;
```

---

## Recommendations

1. **Add Empty State**
   - Show "No key findings available" message
   - Don't hide section completely

2. **Add Link**
   - Link to full analysis report
   - Show source of findings
   - Provide access to detailed data

3. **Improve Fallback**
   - Better handling when no findings
   - Clear user messaging
   - Don't confuse with KPI metrics

