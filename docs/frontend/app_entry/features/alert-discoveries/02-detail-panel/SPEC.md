# Full-Page Discovery Detail View - Specification

**Feature:** 02-detail-panel  
**Component:** `DiscoveryDetailPanel`  
**Status:** ⚠️ Incomplete (navigation and layout issues)

---

## Requirements

### Functional Requirements

1. **Full-Page Layout**
   - Should render as full-width page view
   - Should not be constrained by parent container
   - Should utilize full viewport width

2. **Navigation**
   - Breadcrumb navigation to show path
   - Back button to return to discoveries list
   - Browser back/forward button support

3. **Content Display**
   - Alert title and ID
   - Alert explanation (business_purpose)
   - Output/Params buttons
   - Create Action Item button
   - Summary badges (Module, Severity, Records, Period, Financial Exposure)
   - Critical discovery text block
   - Key findings table
   - Impact analysis (KPI metrics)
   - Concentration pattern table

---

## Expected Behavior

- Truly full-page layout (not just full-width within container)
- Clear navigation back to list
- All content sections visible and accessible
- Responsive design for different screen sizes

---

## Current Implementation Issues

See [ANALYSIS.md](ANALYSIS.md) for detailed issues.

**Key Problems:**

- Layout depends on CSS, not truly "full-page"
- No breadcrumb navigation
- No back button
- Browser navigation not properly handled
