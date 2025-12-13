# Fresh Clone Steps - Complete Guide

**Date:** 2025-12-12  
**Goal:** Create a fresh clone of the repository to eliminate worktree issues  
**Why:** Remove all corrupted Git state and worktree references

---

## ⚠️ IMPORTANT: Read This First

**Before starting:**
1. Make sure all your work is committed and pushed to GitHub
2. Close Cursor completely
3. Have your GitHub credentials ready
4. This will create a fresh copy - your current directory will be backed up

---

## Step-by-Step Instructions

### Step 1: Commit and Push Current Work

**Purpose:** Save all your current changes to GitHub before cloning fresh.

```powershell
# Navigate to current repository
cd C:\Users\USER\Desktop\tha-new

# Check what's uncommitted
git status

# Add all changes
git add .

# Commit everything
git commit -m "WIP: before fresh clone - fixing worktree issues"

# Push to GitHub
git push origin main
```

**Verify:** Go to GitHub and confirm your latest commit is there.

---

### Step 2: Close Cursor Completely

**Purpose:** Cursor locks files, preventing directory operations.

1. **Close all Cursor windows**
2. **Check Task Manager:**
   - Press `Ctrl+Shift+Esc`
   - Look for `Cursor.exe` processes
   - End any that are running

**Verify:** No Cursor processes in Task Manager.

---

### Step 3: Backup Current Directory (Optional but Recommended)

**Purpose:** Keep a backup just in case something goes wrong.

```powershell
# Navigate to Desktop
cd C:\Users\USER\Desktop

# Rename current directory (creates backup)
Rename-Item tha-new tha-new-backup-$(Get-Date -Format "yyyyMMdd-HHmmss")
```

**Example:** `tha-new-backup-20251212-143000`

**Note:** You can delete this backup later if everything works.

---

### Step 4: Clone Fresh Repository

**Purpose:** Get a clean copy from GitHub with no worktree references.

```powershell
# Make sure you're on Desktop
cd C:\Users\USER\Desktop

# Clone fresh repository
git clone https://github.com/iliyaruvinsky/th-analyzer.git tha-new

# Verify clone worked
cd tha-new
git status
```

**Expected:** Should show clean working tree (or only untracked files).

---

### Step 5: Verify Clean State

**Purpose:** Confirm no worktree references exist.

```powershell
# Check worktrees (should show only main)
git worktree list

# Check for worktree references
Test-Path .git\worktrees
```

**Expected:**
- `git worktree list` should show: `C:/Users/USER/Desktop/tha-new   14e32b8 [main]`
- `.git\worktrees` should NOT exist (or be empty)

---

### Step 6: Open Cursor from Main Directory

**Purpose:** Force Cursor to use main directory, not create worktrees.

```powershell
# Make sure you're in the fresh clone
cd C:\Users\USER\Desktop\tha-new

# Open Cursor from HERE (not from shortcut or file explorer)
cursor .
```

**CRITICAL:** Open from the main directory using `cursor .` command.

---

### Step 7: Verify Workspace Path

**Purpose:** Confirm Cursor is using main directory, not a worktree.

**After Cursor opens:**

1. **Look at bottom-left of Cursor window** - shows workspace path
2. **Should show:** `C:\Users\USER\Desktop\tha-new`
3. **Should NOT show:** `C:\Users\USER\.cursor\worktrees\tha-new\{random}`

**If it shows a worktree path:**
- Close Cursor
- Make sure you're in main directory: `cd C:\Users\USER\Desktop\tha-new`
- Open again: `cursor .`

---

### Step 8: Test with Simple UI Change

**Purpose:** Verify the fix worked - changes should appear immediately.

1. **Make a simple UI change** (e.g., change text in a component)
2. **Rebuild Docker:**
   ```powershell
   cd C:\Users\USER\Desktop\tha-new
   docker compose up -d --build frontend
   ```
3. **Check browser** - change should appear immediately
4. **Should work in 1-2 iterations** (not 20-30)

---

### Step 9: Verify No New Worktrees Created

**Purpose:** Confirm Cursor stopped creating worktrees.

```powershell
# After using Cursor for a while, check worktrees
cd C:\Users\USER\Desktop\tha-new
git worktree list
```

**Expected:** Should still show only main directory.

**If new worktrees appear:**
- Cursor is still creating them
- Try opening Cursor from main directory again
- Or check Cursor settings for worktree options

---

## Troubleshooting

### Problem: "Repository not found" during clone

**Solution:**
- Check GitHub URL is correct: `https://github.com/iliyaruvinsky/th-analyzer.git`
- Verify you have access to the repository
- Check your GitHub credentials

### Problem: "Permission denied" when renaming directory

**Solution:**
- Make sure Cursor is completely closed
- Check Task Manager for any processes using the directory
- Try closing other programs that might have files open

### Problem: Cursor still creates worktrees after fresh clone

**Solution:**
- Make sure you're opening Cursor from main directory: `cd C:\Users\USER\Desktop\tha-new && cursor .`
- Check Cursor settings for worktree options
- This might be a Cursor version issue - try updating Cursor

### Problem: Lost uncommitted changes

**Solution:**
- Check backup directory: `C:\Users\USER\Desktop\tha-new-backup-*`
- Copy any files you need from backup
- Or use `git stash` before Step 1 to save changes

---

## Success Criteria

After completing all steps:

- ✅ Fresh clone created successfully
- ✅ No worktree references in `.git/worktrees/`
- ✅ Cursor opens from main directory
- ✅ Workspace path shows main directory (not worktree)
- ✅ Simple UI changes work in 1-2 iterations
- ✅ No new worktrees created after using Cursor

---

## Cleanup (After Everything Works)

**Once you've verified everything works:**

```powershell
# Delete backup directory (optional)
cd C:\Users\USER\Desktop
Remove-Item -Recurse -Force tha-new-backup-*
```

**Only delete backup if:**
- Fresh clone works perfectly
- All your work is in the fresh clone
- You've tested it thoroughly

---

## Next Steps After Fresh Clone

1. ✅ Test with a simple UI change
2. ✅ Verify Docker builds see changes immediately
3. ✅ Document in `llm_handover.md` that fresh clone fixed the issue
4. ✅ Update team if this is a shared repository

---

**END OF GUIDE**

