# Cursor Worktree Configuration Guide

**Date:** 2025-12-12  
**Problem:** Cursor automatically creates new git worktrees, causing workspace switching  
**Goal:** Force Cursor to use main directory only, prevent automatic worktree creation

---

## Understanding the Problem

**What's Happening:**
- Cursor creates git worktrees automatically when you open the project
- Each worktree is a separate directory: `C:\Users\USER\.cursor\worktrees\tha-new\{random}`
- Cursor switches between worktrees, causing AI to edit in wrong location
- Docker builds from main directory, so changes don't appear

**Why Cursor Does This:**
- Cursor uses worktrees to isolate different sessions/contexts
- This is intended for multi-branch development
- But it causes problems when you only want one workspace

---

## Solution: Configure Cursor Settings

### Option 1: Cursor Settings UI (Recommended)

1. **Open Cursor Settings:**
   - Press `Ctrl+,` (or `Cmd+,` on Mac)
   - Or: File → Preferences → Settings

2. **Search for "worktree" or "git":**
   - Look for settings related to:
     - `git.worktree.enabled`
     - `git.worktree.autoCreate`
     - `workspace.trust.enabled`
     - `files.watcherExclude`

3. **Disable Worktree Creation:**
   - If you find `git.worktree.enabled` → Set to `false`
   - If you find `git.worktree.autoCreate` → Set to `false`

4. **Set Default Workspace:**
   - Look for workspace-related settings
   - Set default workspace path to: `C:\Users\USER\Desktop\tha-new`

### Option 2: Cursor Settings JSON (If UI Doesn't Have Option)

1. **Open Settings JSON:**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type: "Preferences: Open User Settings (JSON)"
   - Press Enter

2. **Add These Settings:**
   ```json
   {
     "git.worktree.enabled": false,
     "git.worktree.autoCreate": false,
     "files.watcherExclude": {
       "**/.cursor/worktrees/**": true
     }
   }
   ```

3. **Save and Restart Cursor**

### Option 3: Workspace Settings (Project-Specific)

1. **Create `.vscode/settings.json` in your project:**
   ```json
   {
     "git.worktree.enabled": false,
     "git.worktree.autoCreate": false
   }
   ```

2. **This applies only to this project**

### Option 4: Always Open from Main Directory

**Workaround if settings don't exist:**

1. **Always open Cursor from main directory:**
   ```powershell
   cd C:\Users\USER\Desktop\tha-new
   cursor .
   ```

2. **Or create a shortcut:**
   - Target: `C:\Users\USER\AppData\Local\Programs\cursor\Cursor.exe`
   - Start in: `C:\Users\USER\Desktop\tha-new`
   - Arguments: `"C:\Users\USER\Desktop\tha-new"`

3. **This forces Cursor to use main directory, not worktrees**

---

## Verification

**After Configuration:**

1. **Close Cursor completely**
2. **Open Cursor from main directory:**
   ```powershell
   cd C:\Users\USER\Desktop\tha-new
   cursor .
   ```
3. **Check workspace path:**
   - Look at bottom-left of Cursor window
   - Should show: `C:\Users\USER\Desktop\tha-new`
   - NOT: `C:\Users\USER\.cursor\worktrees\tha-new\{random}`
4. **Verify worktrees:**
   ```powershell
   cd C:\Users\USER\Desktop\tha-new
   git worktree list
   ```
   - Should only show main directory
   - No new worktrees should be created

---

## If Settings Don't Exist

**Cursor may not have these settings yet. In that case:**

1. **Use the workaround:** Always open from main directory
2. **Clean up worktrees regularly:** Run `CLEANUP_WORKTREES.ps1` periodically
3. **Report to Cursor team:** Request worktree configuration options

---

## Alternative: Disable Git Integration (Not Recommended)

**If nothing else works, you can disable Git integration:**

```json
{
  "git.enabled": false
}
```

**Warning:** This disables ALL Git features in Cursor, not just worktrees. Not recommended unless absolutely necessary.

---

## Current Status

**As of 2025-12-12:**
- Cursor settings for worktree control: **UNKNOWN** (need to check)
- Workaround available: **YES** (open from main directory)
- Cleanup script available: **YES** (`CLEANUP_WORKTREES.ps1`)

**Next Steps:**
1. Check Cursor settings UI for worktree options
2. If found, configure them
3. If not found, use workaround (open from main directory)
4. Run cleanup script to remove existing worktrees

---

**END OF GUIDE**


