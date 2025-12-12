# Create Action Item Functionality - Code Reference

**Feature:** 04-create-action-item  
**Component:** `CreateActionItemModal`

---

## File Locations

### Main Component

- **File:** `frontend/src/pages/alert-discoveries/features/create-action-item/CreateActionItemModal.tsx`
- **Export:** `frontend/src/pages/alert-discoveries/features/create-action-item/index.ts`

### Usage

**In AlertDiscoveries.tsx:**
```typescript
import CreateActionItemModal from './alert-discoveries/features/create-action-item';

{actionModalOpen && selectedForAction && (
  <CreateActionItemModal
    discovery={selectedForAction}
    onClose={() => {...}}
    onSuccess={() => {...}}
  />
)}
```

---

## Component Structure

```typescript
interface CreateActionItemModalProps {
  discovery: CriticalDiscoveryDrilldown;
  onClose: () => void;
  onSuccess: () => void;
}
```

### Form Fields

- Title (pre-filled from alert name)
- Description (pre-filled from discovery headline)
- Type (IMMEDIATE, SHORT_TERM, PROCESS_IMPROVEMENT)
- Priority (P1-P5)
- Assigned To (optional)
- Due Date (optional)

---

## API Calls

**Endpoint:** `POST /alert-dashboard/action-items`

**Payload:**
```typescript
{
  alert_analysis_id: number;
  action_type: string;
  priority: number;
  title: string;
  description: string;
  assigned_to?: string;
  due_date?: string;
}
```

---

## Dependencies

- `CriticalDiscoveryDrilldown` type from `services/api`
- `createActionItem` function from `services/api`
- CSS from `AlertDashboard.css` (`.action-modal-*` classes)

---

## Related Files

- `frontend/src/pages/AlertDiscoveries.tsx` - Main usage
- `frontend/src/services/api.ts` - API function

