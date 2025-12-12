# Key Findings - Specification

**Feature:** 09-key-findings  
**Location:** `DiscoveryDetailPanel` left pane  
**Status:** ⚠️ Silently fails

---

## Requirements

### Functional Requirements

1. **Display Findings Table**
   - Rank (#), Finding text, Category columns
   - Sorted by `finding_rank`
   - All findings displayed

2. **User Feedback**
   - Show message when no findings available
   - Don't silently hide section
   - Link to full analysis report

3. **Data Source**
   - Should link to analysis report
   - Should show source of findings
   - Should indicate if findings are missing

---

## Expected Behavior

- Table displays all key findings
- Sorted by rank
- Clear message when no data
- Link to full analysis report

---

## Current Implementation Issues

See [ANALYSIS.md](ANALYSIS.md) for detailed issues.

**Key Problems:**
- Silently fails if no data
- No link to analysis report
- Falls back to count in KPI metrics

