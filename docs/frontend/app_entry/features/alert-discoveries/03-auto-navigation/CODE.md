# Auto-Navigation to First Discovery - Code Reference

**Feature:** 03-auto-navigation  
**Hook:** `useAutoNavigation`

---

## File Locations

### Hook

- **File:** `frontend/src/pages/alert-discoveries/features/auto-navigation/useAutoNavigation.ts`
- **Export:** `frontend/src/pages/alert-discoveries/features/auto-navigation/index.ts`

### Usage

**In AlertDiscoveries.tsx:**
```typescript
import { useAutoNavigation } from './alert-discoveries/features/auto-navigation';

const { id } = useParams<{ id: string }>();
const { data: discoveries = [] } = useQuery(...);

useAutoNavigation({ id, discoveries, replace: true });
```

---

## Hook Structure

```typescript
interface UseAutoNavigationOptions {
  id: string | undefined;
  discoveries: CriticalDiscoveryDrilldown[];
  replace?: boolean;
}

export const useAutoNavigation = ({ id, discoveries, replace = true }: UseAutoNavigationOptions) => {
  const navigate = useNavigate();
  
  useEffect(() => {
    if (!id && discoveries.length > 0 && discoveries[0]?.alert_id) {
      navigate(`/alert-discoveries/${discoveries[0].alert_id}`, { replace });
    }
  }, [id, discoveries, navigate, replace]);
};
```

---

## Dependencies

- `react-router-dom` - `useNavigate`
- `CriticalDiscoveryDrilldown` type from `services/api`

---

## Related Files

- `frontend/src/pages/AlertDiscoveries.tsx` - Main usage

