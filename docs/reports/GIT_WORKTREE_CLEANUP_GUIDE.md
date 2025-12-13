# Git Worktree Cleanup Guide

**Date:** 2025-12-12  
**Problem:** 17 worktrees exist, some broken, causing workspace switching issues  
**Severity:** HIGH - Blocks efficient development

---

## Current State

**Worktrees Found:**
```
Main:     C:/Users/USER/Desktop/tha-new                   14e32b8 [main]
Worktree: C:/Users/.cursor/worktrees/tha-new/atv         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/aui         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/bep         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/eub         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/eyn         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/foy         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/gsp         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/hiw         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/izd         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/kfe         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/nlt         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/npe         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/qfr         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/sst         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/tjf         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/uhn         14e32b8 (detached HEAD)
Worktree: C:/Users/.cursor/worktrees/tha-new/vso         14e32b8 (detached HEAD) ← BROKEN
Worktree: C:/Users/.cursor/worktrees/tha-new/vvr         14e32b8 (detached HEAD)
```

**Total:** 17 worktrees (1 main + 16 Cursor worktrees)

---

## Problem: Broken Worktree

**Error:**
```
Failed to apply worktree to current branch: Unable to read file 
'c:\Users\USER\.cursor\worktrees\tha-new\vso\OMITTED_PROCEDURES_ANALYSIS.md' 
(Error: Unable to resolve nonexistent file)
```

**Root Cause:**
- File `OMITTED_PROCEDURES_ANALYSIS.md` was created in worktree `vso`
- File was never committed
- File was deleted or moved
- Worktree still references it
- Git tries to sync worktree and fails

**Impact:**
- Cannot apply/cleanup worktree `vso`
- Cursor keeps creating new worktrees instead of using existing ones
- Workspace switching problem compounds
- Development efficiency decreases

---

## Solution Options

### Option 1: Remove All Cursor Worktrees (RECOMMENDED)

**Why:** Cursor worktrees are causing the workspace switching problem. Removing them forces Cursor to use main directory only.

**CRITICAL:** Cursor has files locked. You MUST close Cursor first, or use manual deletion.

**Steps:**

```powershell
# STEP 0: CLOSE CURSOR FIRST (IMPORTANT!)
# Cursor locks worktree files, preventing deletion
# Close all Cursor windows before proceeding

# 1. Go to main directory
cd C:\Users\USER\Desktop\tha-new

# 2. Try to prune broken worktrees (may fail if Cursor is open)
git worktree prune

# 3. If prune fails with "Permission denied":
#    → Close Cursor and try again, OR
#    → Use Option 3 (Manual Cleanup) below

# 4. Remove each active Cursor worktree (one by one)
# Note: These will fail if Cursor is open - that's expected
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\atv --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\aui --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\bep --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\eub --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\eyn --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\fiy --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\foy --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\gsp --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\hiw --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\izd --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\kfe --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\kzl --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\nlt --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\npe --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\qfr --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\sst --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\tjf --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\uhn --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\vso --force
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\vvr --force

# 5. Prune again to clean up any remaining broken references
git worktree prune

# 6. Verify only main remains
git worktree list
```

**Expected Result:**
```
C:/Users/USER/Desktop/tha-new   14e32b8 [main]
```

**Benefits:**
- Cursor will use main directory only
- No more workspace switching
- AI edits will be in correct location
- Docker builds will see changes immediately

### Option 2: Fix Broken Worktree Only

**If you want to keep worktrees but fix the broken one:**

```powershell
# 1. Check what's in the broken worktree
cd C:\Users\USER\.cursor\worktrees\tha-new\vso
git status

# 2. If there are uncommitted changes you want to keep:
#    - Commit them first, OR
#    - Copy them to main directory

# 3. Force remove the broken worktree
cd C:\Users\USER\Desktop\tha-new
git worktree remove C:\Users\USER\.cursor\worktrees\tha-new\vso --force

# 4. Prune
git worktree prune
```

**Note:** This only fixes one worktree. Others may have similar issues.

### Option 3: Quick Fix - Remove All Cursor Worktrees at Once

**Fastest way to clean up all 17+ worktrees:**

```powershell
cd C:\Users\USER\Desktop\tha-new

# Remove all Cursor worktrees in one command
$worktrees = @('atv','aui','bep','eub','eyn','foy','gsp','hiw','izd','kfe','nlt','npe','qfr','sst','tjf','uhn','vso','vvr')
foreach ($wt in $worktrees) {
    $path = "C:\Users\USER\.cursor\worktrees\tha-new\$wt"
    if (Test-Path $path) {
        git worktree remove $path --force 2>$null
    }
}

# Prune broken ones
git worktree prune

# Verify
git worktree list
```

### Option 3: Nuclear Option - Manual Cleanup (RECOMMENDED IF CURSOR IS OPEN)

**If `git worktree remove` fails with "Permission denied" (Cursor has files locked):**

```powershell
# STEP 0: CLOSE CURSOR COMPLETELY
# This is CRITICAL - Cursor locks worktree files
# Close all Cursor windows, check Task Manager for any Cursor processes

# 1. Go to main directory
cd C:\Users\USER\Desktop\tha-new

# 2. Manually delete ALL Cursor worktree directories
# This bypasses Git locks
Remove-Item -Recurse -Force "C:\Users\USER\.cursor\worktrees\tha-new\*" -ErrorAction SilentlyContinue

# 3. Manually delete Git worktree references (if they exist)
# These are in .git/worktrees/ directory
Remove-Item -Recurse -Force ".git\worktrees\*" -ErrorAction SilentlyContinue

# 4. Prune to clean up Git references
git worktree prune

# 5. Verify only main remains
git worktree list
```

**Warning:** This will lose any uncommitted changes in worktrees. Make sure to commit or copy important changes first.

**Note:** With 53+ worktrees (17 active + 36+ broken), manual cleanup may be faster than removing one-by-one.

**Why This Works:**
- Cursor locks files in worktree directories
- Git can't delete locked files
- Manual deletion bypasses Git and removes directories directly
- `git worktree prune` then cleans up Git's internal references

---

## Prevention: Configure Cursor to Use Main Directory Only

**After cleanup, configure Cursor to prevent future worktree creation:**

**See:** `docs/reports/CURSOR_WORKTREE_CONFIGURATION.md` for detailed instructions.

**Quick Options:**

1. **Check Cursor Settings:**
   - Press `Ctrl+,` to open settings
   - Search for "worktree" or "git"
   - Disable worktree creation if option exists

2. **Always Open from Main Directory (Workaround):**
   ```powershell
   cd C:\Users\USER\Desktop\tha-new
   cursor .
   ```
   This forces Cursor to use main directory, not worktrees.

3. **Create Workspace Settings:**
   - Create `.vscode/settings.json` in project root:
   ```json
   {
     "git.worktree.enabled": false,
     "git.worktree.autoCreate": false
   }
   ```

**Note:** Cursor may not have these settings yet. If not found, use the workaround (always open from main directory).

---

## Verification After Cleanup

**Check worktree status:**
```powershell
cd C:\Users\USER\Desktop\tha-new
git worktree list
```

**Should show:**
```
C:/Users/USER/Desktop/tha-new   14e32b8 [main]
```

**If other worktrees remain, they should be intentional (not Cursor auto-created).**

---

## Impact of Cleanup

**Before:**
- 17 worktrees (16 Cursor + 1 main)
- Cursor switches between worktrees automatically
- AI edits in wrong directory
- Docker doesn't see changes
- 20-30 rebuild cycles

**After:**
- 1 worktree (main only)
- Cursor uses main directory
- AI edits in correct directory
- Docker sees changes immediately
- 1-2 rebuild cycles

---

## Next Steps After Cleanup

1. ✅ Verify only main worktree exists
2. ✅ Configure Cursor to use main directory
3. ✅ Test UI change (should work in 1-2 iterations)
4. ✅ Document in llm_handover.md

---

**END OF GUIDE**

