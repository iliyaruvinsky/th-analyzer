# Concentration Metrics - Specification

**Feature:** 08-concentration-metrics  
**Location:** `DiscoveryDetailPanel` right pane  
**Status:** ⚠️ Silently fails

---

## Requirements

### Functional Requirements

1. **Display Concentration Table**
   - Entity, Records, % Share columns
   - Top 6 entities by concentration
   - Sorted by rank

2. **Highlight High Concentration**
   - Visual highlighting for >50% concentration
   - Bold entity name
   - Warning indicator

3. **User Feedback**
   - Show message when no data available
   - Don't silently hide section
   - Explain what data means

---

## Expected Behavior

- Table displays concentration distribution
- High concentrations (>50%) highlighted
- Explanation text adapts to actual data
- Clear message when no data available

---

## Current Implementation Issues

See [ANALYSIS.md](ANALYSIS.md) for detailed issues.

**Key Problems:**
- Silently fails if no data
- No highlighting of >50% concentrations
- Generic explanation text

