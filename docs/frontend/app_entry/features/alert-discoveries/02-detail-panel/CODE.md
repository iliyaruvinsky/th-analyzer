# Full-Page Discovery Detail View - Code Reference

**Feature:** 02-detail-panel  
**Component:** `DiscoveryDetailPanel`

---

## File Locations

### Main Component

- **File:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`
- **Export:** `frontend/src/pages/alert-discoveries/features/detail-panel/index.ts`

### Usage

**In AlertDiscoveries.tsx:**

```typescript
import DiscoveryDetailPanel from './alert-discoveries/features/detail-panel';

<DiscoveryDetailPanel
  discovery={selectedDiscovery}
  mode="page"
  onClose={() => {}}
  currencyFormatter={currencyFormatter}
  onCreateAction={handleCreateAction}
/>
```

**In Dashboard.tsx:**

```typescript
import DiscoveryDetailPanel from './alert-discoveries/features/detail-panel';

<DiscoveryDetailPanel
  discovery={selectedDiscovery}
  mode="popover"
  onClose={() => setSelectedDiscovery(null)}
  currencyFormatter={currencyFormatter}
/>
```

---

## Component Structure

```typescript
interface DiscoveryDetailPanelProps {
  discovery: CriticalDiscoveryDrilldown;
  mode: 'modal' | 'inline' | 'popover' | 'page';
  onClose: () => void;
  currencyFormatter: Intl.NumberFormat;
  onViewAnalysis?: (discovery: CriticalDiscoveryDrilldown) => void;
  onCreateAction?: (discovery: CriticalDiscoveryDrilldown) => void;
}
```

### Key Sections

1. **Header** (lines 53-94)
   - Title and ID
   - Business purpose explanation
   - Output/Params buttons
   - Create Action Item button

2. **Body** (lines 104-317)
   - Summary strip (badges)
   - Two-pane layout
   - Left pane: Critical discovery text, Key findings
   - Right pane: Impact analysis, Concentration metrics

---

## Dependencies

- `JsonDataPopover` from `../json-popovers`
- `CriticalDiscoveryDrilldown` type from `services/api`
- CSS from `AlertDashboard.css`

---

## Related Files

- `frontend/src/pages/AlertDiscoveries.tsx` - Main page
- `frontend/src/pages/Dashboard.tsx` - Dashboard popover usage
- `frontend/src/pages/AlertDashboard.css` - Styles
