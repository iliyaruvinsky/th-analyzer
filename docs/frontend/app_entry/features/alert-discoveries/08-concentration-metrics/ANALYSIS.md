# Concentration Metrics - Analysis

**Feature:** 08-concentration-metrics  
**Date:** 2025-12-11  
**Status:** ⚠️ Silently fails

---

## Current State

### What Works

- ✅ Table displays when data exists
- ✅ Shows: Entity, Records, % Share
- ✅ Sorts by rank, shows top 6
- ✅ Includes explanation text

### Issues Identified

1. **Silent Failure**
   - Table only renders if `discovery.concentration_metrics.length > 0`
   - No indication when data is missing
   - Section just doesn't appear

2. **No Highlighting**
   - No visual highlighting for >50% concentration
   - No bold entity names
   - No warning indicators

3. **Generic Explanation**
   - Explanation text doesn't adapt to data
   - Always shows same generic text
   - Doesn't highlight critical concentrations

---

## Code Location

**Component:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`

**Key Code:**
```typescript
// Conditional rendering (lines 271-312)
{discovery.concentration_metrics && discovery.concentration_metrics.length > 0 && (
  <div className="concentration-block">
    {/* Table and explanation */}
  </div>
)}
```

---

## Recommendations

1. **Add Empty State**
   - Show "No concentration data available" message
   - Don't hide section completely

2. **Highlight High Concentration**
   - Bold entities with >50%
   - Add warning styling
   - Visual indicators

3. **Adaptive Explanation**
   - Adapt text to actual data
   - Highlight critical concentrations
   - Provide actionable insights

