# Alert Discoveries Entry - Feature Documentation

**Last Updated:** 2025-12-11  
**Status:** ⚠️ Partially Working - Multiple features need fixes  
**Location:** `/alert-discoveries/:id?`

---

## Overview

The Alert Discoveries entry is the **most important entry** in the application as it provides users with real value based on combined LLM and application analysis. It displays critical discoveries from analyzed alerts with detailed drill-down capabilities.

---

## Feature List

| # | Feature | Status | Documentation |
|---|---------|--------|---------------|
| 01 | [AlertSummary Header with KPI Cards](01-alert-summary/) | ⚠️ Simulated | [SPEC](01-alert-summary/SPEC.md) \| [ANALYSIS](01-alert-summary/ANALYSIS.md) \| [CODE](01-alert-summary/CODE.md) |
| 02 | [Full-Page Discovery Detail View](02-detail-panel/) | ⚠️ Incomplete | [SPEC](02-detail-panel/SPEC.md) \| [ANALYSIS](02-detail-panel/ANALYSIS.md) \| [CODE](02-detail-panel/CODE.md) |
| 03 | [Auto-Navigation to First Discovery](03-auto-navigation/) | ⚠️ Poor UX | [SPEC](03-auto-navigation/SPEC.md) \| [ANALYSIS](03-auto-navigation/ANALYSIS.md) \| [CODE](03-auto-navigation/CODE.md) |
| 04 | [Create Action Item Functionality](04-create-action-item/) | ⚠️ Fragile | [SPEC](04-create-action-item/SPEC.md) \| [ANALYSIS](04-create-action-item/ANALYSIS.md) \| [CODE](04-create-action-item/CODE.md) |
| 05 | [Alert Explanation (business_purpose)](05-alert-explanation/) | ⚠️ No Error Handling | [SPEC](05-alert-explanation/SPEC.md) \| [ANALYSIS](05-alert-explanation/ANALYSIS.md) \| [CODE](05-alert-explanation/CODE.md) |
| 06 | [Output/Params JSON Popovers](06-json-popovers/) | ⚠️ May Show Empty Data | [SPEC](06-json-popovers/SPEC.md) \| [ANALYSIS](06-json-popovers/ANALYSIS.md) \| [CODE](06-json-popovers/CODE.md) |
| 07 | [Risk Score Explanation](07-risk-score/) | ⚠️ Not Real Explanation | [SPEC](07-risk-score/SPEC.md) \| [ANALYSIS](07-risk-score/ANALYSIS.md) \| [CODE](07-risk-score/CODE.md) |
| 08 | [Concentration Metrics](08-concentration-metrics/) | ⚠️ Silently Fails | [SPEC](08-concentration-metrics/SPEC.md) \| [ANALYSIS](08-concentration-metrics/ANALYSIS.md) \| [CODE](08-concentration-metrics/CODE.md) |
| 09 | [Key Findings](09-key-findings/) | ⚠️ Silently Fails | [SPEC](09-key-findings/SPEC.md) \| [ANALYSIS](09-key-findings/ANALYSIS.md) \| [CODE](09-key-findings/CODE.md) |

---

## Code Structure

```
frontend/src/pages/alert-discoveries/
├── AlertDiscoveries.tsx (main page component)
├── AlertDashboard.css (shared styles)
└── features/
    ├── alert-summary/
    │   ├── AlertSummary.tsx
    │   └── index.ts
    ├── detail-panel/
    │   ├── DiscoveryDetailPanel.tsx
    │   └── index.ts
    ├── auto-navigation/
    │   ├── useAutoNavigation.ts
    │   └── index.ts
    ├── create-action-item/
    │   ├── CreateActionItemModal.tsx
    │   └── index.ts
    ├── json-popovers/
    │   ├── JsonDataPopover.tsx
    │   └── index.ts
    └── shared/
        └── (shared utilities, types)
```

---

## API Dependencies

- `GET /alert-dashboard/critical-discoveries` - Fetches all critical discoveries
- `POST /alert-dashboard/action-items` - Creates action items from discoveries

---

## Known Issues Summary

See [ANALYSIS_DISCOVERIES_INCONSISTENCIES.md](../../../ANALYSIS_DISCOVERIES_INCONSISTENCIES.md) for complete analysis.

**Critical Issues:**
- Action Item Creation depends on nested data structure
- Missing data handling (no indication when data is null/empty)
- Data completeness depends on database relationships

**High Priority:**
- Auto-navigation removes browser history
- No error states for empty data
- Risk score "explanation" is just categorization

---

## Related Documentation

- **[DEVELOPMENT_STATE.md](DEVELOPMENT_STATE.md)** - Current development status and assessment ⭐
- [FEATURES.md](../../../FEATURES.md) - Overall feature inventory
- [ANALYSIS_DISCOVERIES_INCONSISTENCIES.md](../../../ANALYSIS_DISCOVERIES_INCONSISTENCIES.md) - Detailed inconsistency analysis
- [llm_handover.md](../../../../llm_handover.md) - Project handover document

---

## Development Workflow

When working on a feature:

1. Read the feature's SPEC.md to understand requirements
2. Read ANALYSIS.md to see current issues
3. Check CODE.md for code locations
4. Make changes in feature folder
5. Update ANALYSIS.md with fixes
6. Update CODE.md if structure changes

