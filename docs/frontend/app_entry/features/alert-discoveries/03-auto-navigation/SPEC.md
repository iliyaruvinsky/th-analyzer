# Auto-Navigation to First Discovery - Specification

**Feature:** 03-auto-navigation  
**Hook:** `useAutoNavigation`  
**Status:** ⚠️ Poor UX (removes history)

---

## Requirements

### Functional Requirements

1. **Automatic Navigation**
   - Navigate to first discovery if no ID in URL
   - Should preserve browser history
   - Should handle empty states gracefully

2. **User Experience**
   - User should be able to go back
   - Should not lose navigation state
   - Should handle loading states

---

## Expected Behavior

- Automatically select first discovery when page loads
- Preserve browser history (user can go back)
- Handle edge cases (empty discoveries, loading states)
- No race conditions

---

## Current Implementation Issues

See [ANALYSIS.md](ANALYSIS.md) for detailed issues.

**Key Problems:**
- Uses `replace: true` - removes history entry
- No handling for empty state
- Possible race conditions

