# Git Workflow Rules - Branching and Commit Strategy

**Version:** 1.0  
**Last Updated:** 2025-12-11  
**Purpose:** Define git branching strategy, commit practices, and workflow for THA project

---

## 🔴 CRITICAL: Safety Rules (MUST READ FIRST)

**Before ANY git operation, see:** `.claude/rules/preserve-working-code.md`

**Core Safety Principles:**
- ✅ Always check `git status` before destructive operations
- ✅ Ask user before `git checkout`, `git reset --hard`, `git clean`
- ✅ Backup uncommitted changes before reverting
- ✅ Never destroy working code

---

## Branching Strategy

### When to Use Feature Branches

**USE FEATURE BRANCHES for:**
- ✅ Major features (new pages, major refactoring)
- ✅ Risky changes (breaking changes, architectural changes)
- ✅ Experimental work (testing new approaches)
- ✅ Multi-session work (work that spans multiple days)

**COMMIT DIRECTLY TO MAIN for:**
- ✅ Small bug fixes (< 50 lines changed)
- ✅ Documentation updates
- ✅ Non-breaking improvements
- ✅ Quick fixes (single file, obvious fix)

### Branch Naming Convention

```
feature/[descriptive-name]     # Feature development
fix/[issue-description]        # Bug fixes
refactor/[component-name]      # Refactoring
docs/[update-type]             # Documentation only
```

**Examples:**
- `feature/discoveries-entry` - Major feature work
- `fix/action-item-creation` - Bug fix
- `refactor/alert-dashboard` - Component refactoring
- `docs/development-state` - Documentation update

---

## Workflow: Feature Branch Development

### Creating a Feature Branch

```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/[name]

# 3. Work on feature
# ... make changes ...

# 4. Commit frequently with descriptive messages
git add [files]
git commit -m "feat: [descriptive message]"

# 5. Push branch to remote
git push origin feature/[name]
```

### Completing a Feature Branch

```bash
# 1. Ensure all work is committed
git status  # Should be clean

# 2. Update main branch
git checkout main
git pull origin main

# 3. Merge feature branch
git merge feature/[name]

# 4. Push to remote
git push origin main

# 5. Delete local branch (optional)
git branch -d feature/[name]

# 6. Delete remote branch (optional)
git push origin --delete feature/[name]
```

---

## Commit Message Standards

### Commit Message Format

```
[type]: [short description]

[optional longer description]

[optional references to issues]
```

### Commit Types

- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring (no behavior change)
- `docs:` - Documentation changes
- `style:` - Formatting, missing semicolons, etc. (no code change)
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks, dependency updates

### Good Commit Messages

✅ **Good:**
```
feat: add Discoveries entry feature documentation structure

- Created DEVELOPMENT_STATE.md for tracking development status
- Organized 9 features into feature folders with SPEC/ANALYSIS/CODE docs
- Moved components to feature-specific folders
- Updated workflow to require DEVELOPMENT_STATE.md for all entries
```

✅ **Good:**
```
fix: action item creation dependency on nested data structure

Resolves issue where action items couldn't be created if discoveries array was empty.
Now uses alert_analysis_id directly from drilldown object.
```

❌ **Bad:**
```
update files
fix stuff
changes
```

---

## Workflow: Direct to Main (Small Changes)

### When Appropriate

- Single file changes
- Obvious bug fixes
- Documentation updates
- Non-breaking improvements

### Process

```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Make changes
# ... edit files ...

# 3. Commit with descriptive message
git add [files]
git commit -m "fix: [description]"

# 4. Push immediately
git push origin main
```

---

## Branch Management

### Regular Maintenance

**Weekly:**
- Review and delete merged feature branches
- Clean up stale branches

**Before Starting New Work:**
- Ensure main is up to date
- Check for existing branches for same feature

### Branch Cleanup

```bash
# List all branches
git branch -a

# Delete local merged branches
git branch -d feature/[name]

# Delete remote merged branches
git push origin --delete feature/[name]

# Prune remote tracking branches
git remote prune origin
```

---

## Conflict Resolution

### When Conflicts Occur

**During Merge:**
1. **STOP** - Don't force merge
2. **Inform user** - "Merge conflict detected in [files]"
3. **Show conflicts** - `git status` shows conflicted files
4. **Wait for user** - Let user resolve or guide resolution

**Never:**
- ❌ Force merge with `--ours` or `--theirs` without user approval
- ❌ Delete conflicted files
- ❌ Skip conflict resolution

### Conflict Resolution Process

```bash
# 1. Identify conflicts
git status

# 2. Open conflicted files
# Look for <<<<<<< HEAD markers

# 3. Resolve conflicts manually
# Edit files to remove conflict markers

# 4. Stage resolved files
git add [resolved-files]

# 5. Complete merge
git commit -m "merge: resolve conflicts in [files]"
```

---

## Emergency Procedures

### Undo Last Commit (Keep Changes)

```bash
# Undo commit but keep changes staged
git reset --soft HEAD~1

# Undo commit and unstage changes
git reset HEAD~1

# Undo commit and discard changes (DANGEROUS - ask user first)
git reset --hard HEAD~1
```

### Revert a Commit (Create New Commit)

```bash
# Revert specific commit (safer)
git revert [commit-hash]

# This creates a new commit that undoes the changes
```

### Recover Lost Work

```bash
# Find lost commits
git reflog

# Recover from reflog
git checkout [commit-hash]
git checkout -b recovery/[name]
```

---

## AI Agent Specific Rules

### Before Any Git Operation

1. **Check current state:**
   ```bash
   git status
   git branch
   ```

2. **Verify what will be affected:**
   - List files that will be changed
   - Show user what will happen

3. **Ask for confirmation:**
   - For destructive operations (reset, checkout, clean)
   - For branch creation/deletion
   - For force pushes

### Commit Workflow for AI Agents

**After completing work:**

1. **Document in llm_handover.md** (MANDATORY)
2. **Stage changes:**
   ```bash
   git add [files]
   ```

3. **Show user what will be committed:**
   ```bash
   git status --short
   git diff --staged --stat
   ```

4. **Ask user for commit message** OR suggest one:
   ```
   Suggested commit: "feat: [description]"
   ```

5. **Commit only after user approval**

6. **Push only if user requests**

---

## Best Practices

### Do's ✅

- ✅ Commit frequently (small, logical commits)
- ✅ Write descriptive commit messages
- ✅ Use feature branches for major work
- ✅ Keep main branch stable
- ✅ Pull before starting work
- ✅ Test before committing
- ✅ Review changes before committing (`git diff`)

### Don'ts ❌

- ❌ Commit directly to main for major features
- ❌ Force push to main without user approval
- ❌ Commit broken code
- ❌ Commit large unrelated changes together
- ❌ Use vague commit messages
- ❌ Delete branches without checking if merged
- ❌ Skip conflict resolution

---

## Integration with Workflow

**This git workflow integrates with:**
- `.claude/WORKFLOW.md` - Main development workflow
- `.claude/rules/preserve-working-code.md` - Safety rules
- `llm_handover.md` - Must update after commits

**After every commit:**
1. Update `llm_handover.md` changelog
2. Document what was changed
3. Note any breaking changes

---

## Examples

### Example 1: Major Feature (Use Branch)

```bash
# Starting Discoveries Entry Development
git checkout main
git pull origin main
git checkout -b feature/discoveries-entry

# Work session 1
git add docs/frontend/app_entry/features/alert-discoveries/
git commit -m "docs: add Discoveries entry feature documentation structure"

# Work session 2
git add frontend/src/pages/alert-discoveries/features/
git commit -m "refactor: move components to feature-specific folders"

# When complete
git checkout main
git merge feature/discoveries-entry
git push origin main
```

### Example 2: Small Fix (Direct to Main)

```bash
# Fix typo in README
git checkout main
git pull origin main
# ... fix typo ...
git add README.md
git commit -m "docs: fix typo in README"
git push origin main
```

---

## Related Documents

- [Preserve Working Code Rules](preserve-working-code.md) - Safety rules
- [Development Workflow](../WORKFLOW.md) - Main workflow
- [llm_handover.md](../../llm_handover.md) - Project handover (update after commits)

---

## Version History

- **v1.0 (2025-12-11)** - Initial git workflow rules

