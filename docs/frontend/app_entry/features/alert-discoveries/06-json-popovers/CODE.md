# Output/Params JSON Popovers - Code Reference

**Feature:** 06-json-popovers  
**Component:** `JsonDataPopover`

---

## File Locations

### Main Component

- **File:** `frontend/src/pages/alert-discoveries/features/json-popovers/JsonDataPopover.tsx`
- **Export:** `frontend/src/pages/alert-discoveries/features/json-popovers/index.ts`

### Usage

**In DiscoveryDetailPanel.tsx:**
```typescript
import JsonDataPopover from '../json-popovers';

<JsonDataPopover
  data={discovery.raw_summary_data}
  title="Alert Output Data"
  buttonLabel="Output"
  buttonIcon="📄"
/>
```

---

## Component Structure

```typescript
interface JsonDataPopoverProps {
  data: Record<string, unknown> | null | undefined;
  title: string;
  buttonLabel: string;
  buttonIcon?: string;
  variant?: 'default' | 'secondary';
}
```

### Key Functions

1. **formatValue** - Formats values for display
2. **formatKey** - Converts keys to readable labels
3. **flattenObject** - Flattens nested objects

---

## CSS Classes

- `.json-popover-container` - Container
- `.json-popover-btn` - Button
- `.json-popover` - Popover
- `.json-popover-header` - Header
- `.json-popover-body` - Body
- `.json-data-table` - Data table

**Location:** `frontend/src/pages/AlertDashboard.css` (lines 3613-3768)

---

## Related Files

- `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx` - Usage

