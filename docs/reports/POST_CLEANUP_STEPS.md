# Post-Cleanup Steps - Prevent Future Worktree Creation

**Date:** 2025-12-12  
**Status:** Cleanup script executed, but Cursor is STILL creating new worktrees  
**Next Steps:** Configure Cursor to use main directory only

---

## Current Situation

**What Happened:**
- ✅ Cleanup script ran with Cursor closed
- ❌ Cursor is STILL creating new worktrees (just created `sul`)
- ⚠️ Workspace keeps switching: `fiy` → `sul` → (will create more)

**Root Cause:**
- Cleanup removed existing worktrees
- But Cursor automatically creates NEW ones when you open it
- Need to prevent Cursor from creating worktrees in the first place

---

## Immediate Action Required

### Step 1: Verify Cleanup Worked

```powershell
cd C:\Users\USER\Desktop\tha-new
git worktree list
```

**Expected:** Should show only main directory (or very few worktrees)

**If you see many worktrees:** Cleanup didn't work completely - may need to run again

### Step 2: Close Cursor Completely

**CRITICAL:** Cursor must be completely closed before proceeding.

1. Close all Cursor windows
2. Check Task Manager for any `Cursor.exe` processes
3. Kill any remaining processes

### Step 3: Open Cursor from Main Directory (CRITICAL)

**This is the KEY step to prevent new worktrees:**

```powershell
# 1. Navigate to main directory
cd C:\Users\USER\Desktop\tha-new

# 2. Open Cursor from HERE (not from a shortcut or file explorer)
cursor .
```

**Why This Works:**
- Opening from main directory forces Cursor to use that location
- Cursor won't create a new worktree if you open from the main repo
- This is the most reliable workaround

### Step 4: Verify Workspace Path

**After opening Cursor:**

1. **Check bottom-left of Cursor window** - shows current workspace path
2. **Should show:** `C:\Users\USER\Desktop\tha-new`
3. **Should NOT show:** `C:\Users\USER\.cursor\worktrees\tha-new\{random}`

**If it shows a worktree path:**
- Close Cursor
- Make sure you're in main directory: `cd C:\Users\USER\Desktop\tha-new`
- Open again: `cursor .`

### Step 5: Create Shortcut (Optional but Recommended)

**To always open from main directory:**

1. **Create new shortcut:**
   - Right-click desktop → New → Shortcut

2. **Target:**
   ```
   C:\Users\USER\AppData\Local\Programs\cursor\Cursor.exe "C:\Users\USER\Desktop\tha-new"
   ```

3. **Start in:**
   ```
   C:\Users\USER\Desktop\tha-new
   ```

4. **Name:** "THA Project - Main Directory"

5. **Use this shortcut** to open Cursor (not file explorer or other methods)

---

## Alternative: Check Cursor Settings

**If opening from main directory doesn't work:**

1. **Open Cursor Settings:**
   - Press `Ctrl+,`
   - Or: File → Preferences → Settings

2. **Search for:**
   - `worktree`
   - `git.worktree`
   - `workspace`

3. **Look for settings like:**
   - `git.worktree.enabled` → Set to `false`
   - `git.worktree.autoCreate` → Set to `false`

4. **If settings don't exist:** Cursor doesn't support disabling worktrees yet → Use the workaround (open from main directory)

---

## Verification Checklist

After following steps above:

- [ ] Cleanup script ran successfully
- [ ] Cursor is closed
- [ ] Opened Cursor from main directory: `cd C:\Users\USER\Desktop\tha-new && cursor .`
- [ ] Workspace path shows: `C:\Users\USER\Desktop\tha-new` (not a worktree)
- [ ] No new worktrees created when opening Cursor
- [ ] AI edits will be in correct location
- [ ] Docker builds will see changes immediately

---

## If Worktrees Keep Getting Created

**If Cursor STILL creates worktrees after opening from main directory:**

1. **Check if you're opening from the right place:**
   ```powershell
   # Verify you're in main directory
   cd C:\Users\USER\Desktop\tha-new
   pwd  # Should show: C:\Users\USER\Desktop\tha-new
   
   # Then open Cursor
   cursor .
   ```

2. **Check Cursor version:**
   - Older versions may not respect workspace settings
   - Update Cursor to latest version

3. **Report to Cursor team:**
   - Request worktree configuration option
   - This is a known limitation

4. **Workaround:**
   - Run cleanup script periodically
   - Always open from main directory
   - Accept that some worktrees may be created, but cleanup regularly

---

## Expected Behavior After Fix

**Before Fix:**
- Workspace: `C:\Users\USER\.cursor\worktrees\tha-new\{random}`
- AI edits in worktree
- Docker builds from main
- Changes don't appear
- 20-30 rebuild cycles

**After Fix:**
- Workspace: `C:\Users\USER\Desktop\tha-new`
- AI edits in main directory
- Docker builds from main
- Changes appear immediately
- 1-2 rebuild cycles

---

## Next Steps Summary

1. ✅ **Verify cleanup:** `git worktree list` (should show only main)
2. ✅ **Close Cursor completely**
3. ✅ **Open from main directory:** `cd C:\Users\USER\Desktop\tha-new && cursor .`
4. ✅ **Verify workspace path** (should be main, not worktree)
5. ✅ **Test with a simple UI change** (should work in 1-2 iterations)

---

**END OF GUIDE**

