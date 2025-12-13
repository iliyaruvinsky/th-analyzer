# Root Cause Analysis: Why Cursor Creates Worktrees

**Date:** 2025-12-12  
**Question:** Why do other developers not encounter this problem?  
**Hypothesis:** Something in our Git repository setup is triggering Cursor's worktree feature

---

## The Real Question

**You're absolutely right:** This problem shouldn't exist. Other developers use Cursor + Docker without this issue. So why is it happening to us?

---

## Investigation Findings

### 1. Git Repository State

**Current State:**
- Repository: `https://github.com/iliyaruvinsky/th-analyzer.git`
- Branch: `main` (ahead of origin by 5 commits)
- Config: Normal (`bare = false`, standard setup)
- **Found:** `.git/worktrees/oye/gitdir` - leftover worktree reference

**Analysis:**
- Git config looks normal
- No worktree-specific config that would trigger this
- But there's a leftover worktree reference in `.git/worktrees/`

### 2. Possible Root Causes

#### Hypothesis A: Cursor Detects Existing Worktrees

**Theory:** Cursor sees the `.git/worktrees/` directory and thinks:
- "This repo uses worktrees"
- "I should create worktrees too"
- Creates new worktrees automatically

**Evidence:**
- `.git/worktrees/oye/` exists (leftover from previous worktree)
- Cursor keeps creating new worktrees

**Test:**
- Remove ALL worktree references from `.git/worktrees/`
- See if Cursor stops creating new ones

#### Hypothesis B: Repository Was Cloned/Initialized Unusually

**Theory:** The repository might have been:
- Cloned from a worktree
- Initialized in a worktree
- Set up in a way that makes Cursor think it's a worktree-based project

**Evidence:**
- Repository path: `C:\Users\USER\Desktop\tha-new`
- This is a normal path, not a worktree path
- But Cursor treats it like it needs worktrees

#### Hypothesis C: Cursor Version/Configuration Issue

**Theory:** 
- Cursor version might have a bug
- Cursor user settings might enable worktrees by default
- Cursor might be configured to use worktrees for this project

**Evidence:**
- Other developers don't have this issue
- Suggests it's environment-specific, not universal Cursor behavior

#### Hypothesis D: Git Repository Corruption

**Theory:**
- Repository might have corrupted state
- `.git/config` or `.git/worktrees/` might have bad references
- This triggers Cursor's worktree feature

**Evidence:**
- Multiple broken worktrees found earlier
- Leftover worktree references in `.git/worktrees/`

---

## Recommended Solution: Fresh Clone

**Your suggestion is correct:** Re-push to a brand new Git repository might fix this.

### Option 1: Clean Current Repository

**Steps:**

```powershell
# 1. Backup current work (commit or stash)
cd C:\Users\USER\Desktop\tha-new
git add .
git commit -m "WIP: before repository cleanup"

# 2. Remove ALL worktree references
Remove-Item -Recurse -Force .git\worktrees\* -ErrorAction SilentlyContinue
git worktree prune

# 3. Verify clean state
git worktree list  # Should show only main

# 4. Push to remote (sync with GitHub)
git push origin main

# 5. Test if Cursor still creates worktrees
```

### Option 2: Fresh Clone (Recommended)

**Steps:**

```powershell
# 1. Backup current work
cd C:\Users\USER\Desktop\tha-new
git add .
git commit -m "WIP: before fresh clone"
git push origin main

# 2. Clone fresh copy
cd C:\Users\USER\Desktop
Remove-Item -Recurse -Force tha-new  # Or rename it
git clone https://github.com/iliyaruvinsky/th-analyzer.git tha-new

# 3. Verify clean state
cd tha-new
git worktree list  # Should show only main (no worktrees)

# 4. Open Cursor from main directory
cursor .

# 5. Test if Cursor creates worktrees
```

### Option 3: New Repository (Nuclear Option)

**If fresh clone doesn't work:**

1. Create a brand new GitHub repository
2. Push all code to new repository
3. Clone fresh
4. This eliminates any repository-level corruption

---

## Why This Might Work

**Fresh Clone Benefits:**
- Removes all worktree references
- Removes any corrupted Git state
- Starts with clean `.git/` directory
- Cursor won't detect existing worktree setup
- Should behave like a normal repository

---

## Testing After Fix

**After fresh clone:**

1. **Open Cursor from main directory:**
   ```powershell
   cd C:\Users\USER\Desktop\tha-new
   cursor .
   ```

2. **Check workspace path:**
   - Should be: `C:\Users\USER\Desktop\tha-new`
   - Should NOT be: `C:\Users\USER\.cursor\worktrees\tha-new\{random}`

3. **Verify no worktrees created:**
   ```powershell
   git worktree list
   ```
   - Should show only main directory

4. **Test with a simple UI change:**
   - Should work in 1-2 iterations (not 20-30)

---

## Why Other Developers Don't Have This Problem

**Possible Reasons:**
1. **They clone fresh repositories** - no worktree history
2. **They don't have leftover worktree references** in `.git/worktrees/`
3. **Their Cursor version** doesn't have this behavior
4. **They open Cursor from main directory** (workaround we discovered)
5. **Their repository was never in a worktree state**

---

## Immediate Action

**Before trying fresh clone, try this first:**

```powershell
# Remove leftover worktree references
cd C:\Users\USER\Desktop\tha-new
Remove-Item -Recurse -Force .git\worktrees\* -ErrorAction SilentlyContinue
git worktree prune

# Verify
git worktree list

# Close Cursor, then open from main directory
cursor .
```

**If this doesn't work, then try fresh clone.**

---

**END OF ANALYSIS**

