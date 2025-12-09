# CRITICAL RULE: Preserve Working Code

## NEVER LOSE WORKING CODE

### Before ANY git checkout, git reset, or revert operation:

1. **CHECK if file has uncommitted changes**: `git status <file>`
2. **If file is modified (M) or untracked (??)**:
   - DO NOT run git checkout on it
   - ASK USER first: "This file has uncommitted changes. Should I backup first?"
   - Create backup: `cp <file> <file>.backup`
3. **If user says "revert"**:
   - First verify what will be lost
   - Offer to commit current state first
   - NEVER blindly run git checkout on modified files

### After ANY successful development:

1. **Immediately document** what was created/changed in llm_handover.md
2. **Suggest committing** the working code to user
3. **If user declines commit**, warn them the code could be lost

### Git Commands That Destroy Uncommitted Work:
- `git checkout <file>` - DESTROYS local changes
- `git reset --hard` - DESTROYS all uncommitted changes
- `git clean -fd` - DESTROYS untracked files
- `git stash` without `git stash pop` - Can lose work

### Before Running These Commands:
1. List what will be affected
2. Confirm with user
3. Backup if necessary

## VIOLATION OF THIS RULE WASTES USER TIME AND DESTROYS THEIR WORK

This rule exists because on 2024-12-09, working Dashboard.tsx code with tabs integration was destroyed by carelessly running `git checkout` without checking for uncommitted changes. This cost the user 30+ minutes of rebuild time.

**NO EXCEPTIONS.**
