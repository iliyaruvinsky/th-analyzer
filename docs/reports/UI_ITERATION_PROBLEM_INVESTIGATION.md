# UI Iteration Problem - Root Cause Investigation

**Date:** 2025-12-12  
**Investigator:** AI Agent  
**Problem:** Simple UI changes require 20-30 iterations instead of 1-2  
**Severity:** CRITICAL - Blocks efficient development

---

## Executive Summary

**ROOT CAUSE IDENTIFIED:** Git worktree switching by Cursor causes AI to edit files in different directories than where Docker builds from, leading to changes not being reflected in running containers.

**Impact:**
- 20-30 rebuild cycles instead of 1-2
- User frustration and wasted time
- Loss of trust in AI accuracy
- Increased development costs

**Solution:** Establish single source of truth for file edits and Docker operations.

---

## Problem Statement

### Observed Behavior

1. **User requests simple UI change** (e.g., remove button, change text)
2. **AI makes changes** and claims success
3. **User rebuilds Docker** - no changes visible
4. **User reports "no changes"**
5. **AI makes changes again** - cycle repeats 20-30 times
6. **Finally works** when AI accidentally edits correct directory

### Example: Refresh Button Removal

**What Should Have Happened:**
1. Remove button from `Layout.tsx` (1 edit)
2. Rebuild frontend (1 rebuild)
3. Verify with Playwright (1 verification)
4. **Total: 3 steps**

**What Actually Happened:**
1. AI edited file in worktree `bep` → Docker builds from main → no change
2. AI edited file in worktree `sst` → Docker builds from main → no change
3. AI edited file in worktree `izd` → Docker builds from main → no change
4. AI edited file in worktree `kfe` → Docker builds from main → no change
5. Finally edited in main directory → **48 rebuilds later** → works

---

## Root Cause Analysis

### Primary Cause: Git Worktree Confusion + Docker Build Root Mismatch

**Critical Understanding:**
- `docker-compose.yml` exists in BOTH main directory AND worktrees (they're copies)
- **Docker build root = WHERE user runs `docker compose` command**
- NOT where docker-compose.yml file exists
- User runs commands from: `C:\Users\USER\Desktop\tha-new` (main directory)

**Evidence:**

```bash
$ git worktree list
C:/Users/USER/Desktop/tha-new                   14e32b8 [main]  ← User runs docker compose from here
C:/Users/.cursor/worktrees/tha-new/atv         14e32b8 (detached HEAD)
C:/Users/.cursor/worktrees/tha-new/aui         14e32b8 (detached HEAD)  ← AI editing here
C:/Users/.cursor/worktrees/tha-new/bep         14e32b8 (detached HEAD)  ← AI editing here
C:/Users/.cursor/worktrees/tha-new/eub         14e32b8 (detached HEAD)  ← AI editing here
... (16 total worktrees)

# docker-compose.yml exists in ALL of these locations
# But Docker builds from WHERE user runs the command
```

**Problem Flow:**

1. **Cursor automatically switches workspace** to different worktrees
2. **AI receives workspace path** like `C:\Users\USER\.cursor\worktrees\tha-new\bep`
3. **AI edits files** in that worktree directory
4. **User runs `docker compose` from** `C:\Users\USER\Desktop\tha-new` (main directory)
5. **Docker builds from main directory** (where command was executed)
6. **Changes never appear** because they're in worktree, not main
7. **AI claims success** without verifying WHERE user runs docker commands
8. **User rebuilds** - sees no changes
9. **Cycle repeats** until AI accidentally edits main directory

### Secondary Causes

#### 1. No Verification of Docker Build Context

**Anti-Hallucination Rule 1 Violation:**
- AI never verified WHERE Docker actually builds from
- AI assumed workspace path = Docker build path
- No `read_file` verification after edits in correct location

**Evidence:**
```yaml
# docker-compose.yml
frontend:
  build:
    context: ./frontend  # Relative to WHERE docker-compose.yml is located
```

Docker build context is **relative to docker-compose.yml location**, not workspace path.

#### 2. No Playwright Verification

**Rule 15 Violation (Screenshot Examination):**
- User asked AI to use Playwright to verify changes
- AI attempted but failed due to connection issues
- AI never persisted to actually verify visually
- AI claimed success without visual confirmation

#### 3. Workspace Path Changes Not Detected

**Problem:**
- Cursor switches worktrees automatically
- AI doesn't detect workspace path changes
- AI continues editing in wrong directory
- No validation that current workspace = Docker build directory

**Evidence from Session:**
```
Workspace: bep → sst → izd → kfe → aui (kept changing)
Docker builds from: C:\Users\USER\Desktop\tha-new (never changed)
```

#### 4. File Verification in Wrong Location

**Anti-Hallucination Rule 1 Violation:**
- AI used `read_file` to verify changes
- But verified in worktree, not main directory
- Verified "success" in wrong location
- Reported success based on wrong file

**Example:**
```typescript
// AI edited: C:\Users\USER\.cursor\worktrees\tha-new\bep\frontend\src\components\Layout.tsx
// AI verified: C:\Users\USER\.cursor\worktrees\tha-new\bep\frontend\src\components\Layout.tsx
// Docker builds from: C:\Users\USER\Desktop\tha-new\frontend\src\components\Layout.tsx
// Result: Verification passed, but Docker didn't see changes
```

---

## Contributing Factors

### 1. No Pre-Edit Validation

**Missing Step:**
- Before editing, AI should verify: "Is current workspace = Docker build directory?"
- Should check: `docker-compose.yml` location vs workspace path
- Should warn if mismatch detected

### 2. No Post-Edit Docker Context Verification

**Missing Step:**
- After editing, AI should verify: "Did I edit the file Docker will build from?"
- Should read file from Docker build context location
- Should compare with edited file

### 3. Assumption That Workspace = Build Directory

**False Assumption:**
- AI assumed workspace path is where Docker builds from
- Never verified this assumption
- Never checked `docker-compose.yml` location

### 4. No Visual Verification Protocol

**Missing:**
- Playwright verification after rebuild
- Screenshot comparison
- Visual confirmation of changes

---

## Impact Analysis

### Time Waste

**Per Simple Change:**
- Expected: 5-10 minutes (1-2 iterations)
- Actual: 2-3 hours (20-30 iterations)
- **Waste: 12-36x longer than necessary**

### Cost Impact

**Per Session:**
- Expected tokens: ~50K (simple UI change)
- Actual tokens: ~500K-1M (20-30 iterations)
- **Cost multiplier: 10-20x**

### Trust Impact

- User loses confidence in AI accuracy
- User questions every AI claim
- User must manually verify every change
- Development velocity decreases

### Developer Experience

- Frustration: "48 rebuilds for one button removal"
- Time lost: 3 days for simple changes
- Blocks other work: Can't proceed until UI works

---

## Solution Design

### Immediate Fix: Single Source of Truth Protocol

**MANDATORY WORKFLOW FOR UI CHANGES:**

```markdown
## UI Change Protocol (MANDATORY)

### Step 1: Identify Docker Build Directory
1. **ASK USER:** "Where do you run `docker compose` commands from?"
2. **OR detect:** Check user's terminal working directory (usually `C:\Users\USER\Desktop\tha-new`)
3. **This is the build root** - NOT where docker-compose.yml exists
4. Calculate absolute path: `{build root}/frontend` or `{build root}/backend`
5. **Note:** docker-compose.yml exists in multiple places, but build root = command execution location

### Step 2: Verify Current Workspace
1. Check current workspace path
2. Compare with Docker build root
3. If mismatch: WARN USER and ask which to use

### Step 3: Edit in Correct Location
1. Use absolute path to Docker build directory
2. Edit: `C:\Users\USER\Desktop\tha-new\frontend\src\...`
3. NOT: `{workspace}\frontend\src\...`

### Step 4: Verify in Docker Build Location
1. Read file from Docker build directory (absolute path)
2. Verify change exists there
3. NOT from workspace path

### Step 5: Visual Verification (After Rebuild)
1. User rebuilds Docker
2. AI uses Playwright to navigate to page
3. AI takes screenshot
4. AI verifies change is visible
5. Only then claim success
```

### Long-Term Fix: Workspace Detection & Validation

**Add to WORKFLOW.md:**

```markdown
## Workspace Validation Protocol

### Before ANY File Edit:

1. **Detect Current Workspace:**
   ```bash
   # Check workspace path
   pwd  # or equivalent
   ```

2. **Detect Docker Build Root:**
   ```bash
   # Find docker-compose.yml
   find . -name "docker-compose.yml" -type f
   # Note its directory - this is build root
   ```

3. **Compare:**
   - If workspace != build root: WARN USER
   - Ask: "Edit in workspace or build root?"
   - Default: Build root (where Docker builds from)

4. **Use Absolute Paths:**
   - Always use absolute path to build root
   - Never rely on workspace-relative paths
   ```

### Enhanced Verification Protocol

**Add to Anti-Hallucination Rules:**

```markdown
### RULE 16: DOCKER BUILD CONTEXT VERIFICATION

**Before editing files for Docker-based projects:**

1. **Identify Docker build root:**
   - Read docker-compose.yml
   - Note location of docker-compose.yml
   - This is the build root

2. **Verify edit location:**
   - Edit files using absolute path to build root
   - NOT workspace-relative paths
   - NOT worktree paths

3. **Verify in build root:**
   - After edit, read file from build root (absolute path)
   - Verify change exists there
   - NOT from workspace path

4. **Visual verification:**
   - After user rebuilds, use Playwright
   - Navigate to page
   - Take screenshot
   - Verify change is visible
   - Only then claim success

**Violation:** Editing in wrong directory and claiming success = immediate correction required.
```

---

## Implementation Plan

### Phase 1: Immediate (This Session)

1. ✅ Document root cause (this document)
2. ✅ Add workspace validation to WORKFLOW.md
3. ✅ Add Docker build context verification to anti-hallucination rules
4. ✅ Create UI change protocol

### Phase 2: Next Session

1. Test protocol with simple UI change
2. Verify it works in 1-2 iterations
3. Refine based on results

### Phase 3: Long-Term

1. Add automated workspace detection
2. Add pre-edit validation checks
3. Add post-edit Docker context verification
4. Integrate Playwright verification into workflow

---

## Verification Checklist

**Before claiming UI change is complete:**

- [ ] Did I identify Docker build root from docker-compose.yml?
- [ ] Did I edit file using absolute path to build root?
- [ ] Did I verify change in build root (not workspace)?
- [ ] Did user rebuild Docker?
- [ ] Did I use Playwright to verify change is visible?
- [ ] Can I show screenshot proving change exists?

**If any answer is NO → DO NOT claim success**

---

## Lessons Learned

1. **Never assume workspace = build directory**
2. **Always verify Docker build context before editing**
3. **Always use absolute paths for Docker-related edits**
4. **Always verify visually after rebuild**
5. **Workspace switching is a real problem - detect and handle it**

---

## Related Issues

- Anti-Hallucination Rule 1 violations (no verification)
- Rule 15 violations (no screenshot examination)
- Workspace management confusion
- Docker build context misunderstanding

---

## Next Steps

1. User reviews this investigation
2. Implement immediate fix protocol
3. Test with next UI change
4. Refine based on results
5. Update WORKFLOW.md with permanent solution

---

## Additional Issue: Git Worktree Corruption

### Problem Discovered (2025-12-12)

**Symptom:**
```
Failed to apply worktree to current branch: Unable to read file 
'c:\Users\USER\.cursor\worktrees\tha-new\vso\OMITTED_PROCEDURES_ANALYSIS.md' 
(Error: Unable to resolve nonexistent file)
```

**Root Cause:**
- Worktrees reference files that were never committed or were deleted
- File `OMITTED_PROCEDURES_ANALYSIS.md` was created in a worktree but never committed
- Worktree tries to sync and fails because file doesn't exist
- This prevents worktree application/cleanup

**Evidence:**
- File doesn't exist in main repo: `Test-Path OMITTED_PROCEDURES_ANALYSIS.md` → False
- File doesn't exist in JUNK: `Test-Path JUNK\OMITTED_PROCEDURES_ANALYSIS.md` → False
- File doesn't exist in worktree: `Test-Path C:\Users\USER\.cursor\worktrees\tha-new\vso\OMITTED_PROCEDURES_ANALYSIS.md` → False
- Git status shows file is not tracked: `git ls-files | Select-String "OMITTED"` → No results
- But worktree still references it

**Impact:**
- Cannot apply/cleanup worktrees
- Worktree management broken
- Cursor keeps creating new worktrees instead of using existing ones
- Compounds the workspace switching problem

### Solution: Clean Up Broken Worktrees

**Recommended Actions:**

1. **Remove all Cursor worktrees:**
   ```bash
   cd C:\Users\USER\Desktop\tha-new
   git worktree prune
   # Manually remove broken worktrees if needed
   ```

2. **Configure Cursor to use main directory only:**
   - Disable automatic worktree creation
   - Use main repo directory: `C:\Users\USER\Desktop\tha-new`

3. **Prevent future worktree corruption:**
   - Commit or delete files before switching workspaces
   - Don't create files in worktrees without committing
   - Use main directory for all development

**Alternative: Fix Current Worktrees**

If worktrees have uncommitted changes:
1. Check each worktree for uncommitted changes
2. Commit or discard changes
3. Remove worktree: `git worktree remove <path>`
4. Prune: `git worktree prune`

---

**END OF INVESTIGATION**

