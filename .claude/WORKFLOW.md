# THA Development Workflow - AI Agent Work Process

**Version:** 2.0  
**Last Updated:** 2025-12-11  
**Purpose:** Define complete workflow for AI agents working on THA project

---

## ⚠️ CRITICAL: Mandatory Rules (MUST READ FIRST)

**Before using this workflow, you MUST internalize these rules:**

### 📋 Rule Files Location

- `.claude/rules/anti-hallucination-rules.md` - **Behavioral rules (MANDATORY)**
- `.claude/rules/preserve-working-code.md` - **Git safety (CRITICAL)**
- `.claude/rules/llm-handover-maintenance.md` - **Documentation rules**
- `.claude/rules/quantitative-alert-analysis.md` - **Alert analysis standards**

### 🔴 Core Principles (NO EXCEPTIONS)

**1. VERIFY BEFORE CLAIMING** (Anti-Hallucination Rule 1)

- NEVER report a change was made without reading the file afterward
- ALWAYS use `read_file` IMMEDIATELY after any edit to verify
- ONLY report success after verification shows change exists

**2. PRESERVE WORKING CODE** (Git Safety)

- NEVER run `git checkout` without checking `git status` first
- ASK USER before any destructive git operation
- Backup files before reverting if they have uncommitted changes

**3. UPDATE llm_handover.md** (Documentation Rule)

- MUST update llm_handover.md after every significant change
- CANNOT mark task complete without updating handover doc
- This is the project's memory - keep it current

**4. NO "YESMAN" BEHAVIOR** (Truth Over Convenience)

- Admit uncertainty instead of making up plausible answers
- Truth is highest value - even if disappointing
- Real limitations > fake capabilities

**5. LITERAL VALUE COMPLIANCE** (Precision)

- When user specifies exact value ("16px"), use THAT EXACT VALUE
- Do not substitute your judgment
- Specific beats general

**Full details:** See [Mandatory Rules Reference](#mandatory-rules-reference) at end of document.

**Why These Rules Exist:**

- User has 1M token context window capacity
- User pays real money for accurate work
- Unverified claims require expensive re-work
- Trust is lost through inaccurate reporting
- Professional work requires verification before claiming success
- Previous incidents (2024-12-09): Working code destroyed by careless git operations

**Violation Consequences:**

- Wasted user money and time
- Loss of working code
- Inconsistent documentation
- Rejected reports (for alert analysis)
- Loss of trust

---

## 📚 Document Overview

This workflow guide shows **which documents to use during each development phase** in the THA (Treasure Hunt Analyzer) project.

### The 6-Document Core System

1. **README.md** - User entry point
2. **CLAUDE.md** - AI assistant technical guide  
3. **llm_handover.md** - Current state, changelog (THE source of truth)
4. **prompt_read_the_flow.md** - Reading sequence for alert analysis
5. **TESTING.md** - Consolidated testing guide
6. **DEPLOYMENT.md** - Deployment + Docker troubleshooting
7. **CONTRIBUTING.md** - Optional contribution guidelines

---

## 📋 Phase 1: Planning + Documentation

### When You're Planning a Feature/Fix

**SEQUENCE:**

```
1. READ: llm_handover.md
   ├── Current Work in Progress (check if already being worked on)
   ├── Known Issues (check if already documented)
   ├── Roadmap (check if already planned)
   └── Recent Changelog (understand recent changes)

2. READ: CLAUDE.md (if needed)
   ├── Project Structure (understand architecture)
   ├── API Endpoints (see what exists)
   ├── Key Files Reference (find relevant code)
   └── Code Conventions (follow standards)

3. READ: prompt_read_the_flow.md (if first time on project)
   └── Follow PHASE 1-7 reading sequence

4. DOCUMENT YOUR PLAN:
   └── UPDATE: llm_handover.md
       ├── Add to "Current Work in Progress" section
       ├── Describe: What you're building
       ├── Describe: Why it's needed
       └── Describe: Approach/strategy
```

**Example Planning Entry in llm_handover.md:**

```markdown
## CRITICAL: Current Work in Progress

### ACTIVE: Fix _fallback_analysis() to Use Structured Data (2025-12-11)

**Problem:** `_fallback_analysis()` ignores `artifacts.summary_data` and uses primitive regex extraction.

**Plan:**
1. Read `analyzer.py` and `artifact_reader.py`
2. Update `_fallback_analysis()` to check for `summary_data` first
3. Fall back to text extraction only if `summary_data` is None
4. Test with real alert files
5. Update documentation

**Files to Modify:**
- `backend/app/services/content_analyzer/analyzer.py`
```

---

## 💻 Phase 2: Development + Documentation

### During Active Development

**SEQUENCE:**

```
1. CODE CHANGES
   ├── Make changes to source files
   ├── Add inline comments for complex logic
   └── Follow conventions from CLAUDE.md

2. VERIFY CHANGES (Anti-Hallucination Rule 1-3)
   ├── Execute change (search_replace, write, etc.)
   ├── IMMEDIATELY run read_file to verify
   ├── Compare actual vs intended result
   ├── If failed, try alternative method
   └── ONLY report success after verification

3. AS YOU WORK (Real-time updates):
   └── UPDATE: llm_handover.md "Current Work in Progress"
       ├── Mark tasks completed ✅
       ├── Note blockers/issues
       └── Update status

4. AFTER VERIFICATION (Feature works):
   └── UPDATE: llm_handover.md "Changelog"
       ├── Add date section (e.g., "### 2025-12-11")
       ├── Describe what was changed
       ├── List files created/modified
       └── Note any breaking changes

5. IF ARCHITECTURAL CHANGE:
   └── UPDATE: CLAUDE.md
       ├── Update Project Structure (if new directories)
       ├── Update API Endpoints (if new endpoints)
       ├── Update Key Files Reference (if critical files)
       └── Update Domain Model (if data model changed)

6. IF USER-FACING CHANGE:
   └── UPDATE: README.md
       └── Only if Quick Start or main features affected
```

**Anti-Hallucination Checkpoints:**

After EVERY file edit:

```
✅ Did I read_file to verify the change?
✅ Does the file actually contain what I claim?
✅ Am I reporting facts or assumptions?
✅ Can I prove this by showing actual file content?
```

**Preserve Code Checkpoints:**

Before ANY git operation:

```
✅ Did I run git status first?
✅ Are there uncommitted changes?
✅ Did I ask user before destructive operation?
✅ Did I create backup if needed?
```

**What NOT to Do:**

- ❌ Create new root-level .md file
- ❌ Create FEATURE_XYZ.md
- ❌ Create IMPLEMENTATION_ABC.md
- ❌ Update multiple docs with same info

**Example Development Update in llm_handover.md:**

```markdown
## Changelog

### 2025-12-11 (FIX FALLBACK ANALYSIS)

**Problem Fixed:** `_fallback_analysis()` was ignoring structured data from `ArtifactReader`.

**Changes:**
1. Updated `_fallback_analysis()` to use `artifacts.summary_data` when available
2. Falls back to regex extraction only if `summary_data` is None
3. Now properly extracts currency, key_metrics, and notable_items

**Files Modified:**
- `backend/app/services/content_analyzer/analyzer.py` (lines 366-406)

**Verification:**
- Tested with FI alert: Currency now "USD" instead of missing
- Tested with MM alert: key_metrics now populated instead of {}
- All 15 test alerts pass

**Impact:**
- ✅ Quantitative analysis now uses real extracted data
- ✅ No breaking changes
- ✅ Backward compatible (falls back if no structured data)
```

---

## 🐛 Phase 3: Debugging + Documentation

### When Debugging an Issue

**SEQUENCE:**

```
1. READ: llm_handover.md "Known Issues"
   └── Check if issue already documented

2. INVESTIGATE:
   ├── Use grep/codebase_search to find relevant code
   ├── Read source files
   ├── Check logs (DEPLOYMENT.md has troubleshooting)
   └── Reproduce issue

3. DOCUMENT INVESTIGATION:
   
   IF bug in existing code:
   ├── Add inline code comments explaining the bug
   └── UPDATE: llm_handover.md "Known Issues" section
   
   IF architectural issue:
   ├── Create GitHub issue (NOT a root .md file)
   └── UPDATE: llm_handover.md with link to issue
   
   IF temporary investigation:
   └── DO NOT create document - use inline notes only

4. AFTER FIX:
   └── UPDATE: llm_handover.md "Changelog"
       ├── Describe bug
       ├── Describe fix
       ├── Note files changed
       └── Mark "Known Issue" as resolved

5. IF COMMON ISSUE:
   └── UPDATE: DEPLOYMENT.md "Troubleshooting" section
       └── Add to appropriate category
```

**Example Bug Documentation:**

```markdown
## Known Issues

### ~~Fallback Analysis Returns Placeholder Data~~ ✅ FIXED 2025-12-11

**Status:** RESOLVED

**Issue:** Single/batch alert analysis produced placeholder data instead of real extracted data.

**Root Cause:** `_fallback_analysis()` in analyzer.py ignored `artifacts.summary_data` and used primitive regex on raw text.

**Fix Applied:** Updated `_fallback_analysis()` to prioritize structured data from `ArtifactReader`.

**See:** Changelog entry 2025-12-11
```

---

## ✅ Phase 4: Testing & Validation + Documentation

### During Testing

**SEQUENCE:**

```
1. READ: TESTING.md
   ├── Quick Test (5 min) - for fast verification
   ├── Full Testing Checklist - for comprehensive testing
   └── Troubleshooting - if issues found

2. EXECUTE TESTS:
   ├── Follow Quick Test sequence
   ├── Check specific features from checklist
   └── Note any failures

3. DOCUMENT TEST RESULTS:
   
   IF tests pass:
   └── UPDATE: llm_handover.md "Changelog"
       └── Add "Verified Working" note
   
   IF tests fail:
   └── UPDATE: llm_handover.md "Known Issues"
       ├── Document the failure
       ├── Note reproduction steps
       └── Link to related code

4. IF NEW TEST PROCEDURE:
   └── UPDATE: TESTING.md
       └── Add to appropriate section (Quick Test or Full Checklist)

5. IF DEPLOYMENT ISSUE:
   └── UPDATE: DEPLOYMENT.md "Troubleshooting"
       └── Add solution for future reference
```

**Example Test Documentation:**

```markdown
## Changelog

### 2025-12-11 (FIX FALLBACK ANALYSIS)

...

**Testing:**
- ✅ Tested with 15 different alert types
- ✅ Currency extraction: 15/15 pass
- ✅ Key metrics extraction: 15/15 pass  
- ✅ Notable items extraction: 12/15 pass (3 alerts have no sample data)
- ✅ Backward compatibility: Old alerts still work
- ✅ Frontend displays new data correctly

**Test Commands Used:**
```bash
curl -X POST "http://localhost:3011/api/v1/content-analysis/analyze-and-save" \
  -H "Content-Type: application/json" \
  -d '{"directory_path": "/app/docs/skywind-4c-alerts-output/FI/..."}'
```

```

---

## 🚀 Phase 5: Moving to Production + Documentation

### When Deploying to Production

**SEQUENCE:**

```

1. READ: DEPLOYMENT.md
   ├── Production Deployment section
   ├── Environment Variables
   └── Security checklist

2. PRE-DEPLOYMENT:
   └── UPDATE: llm_handover.md
       ├── Note version being deployed (e.g., v1.8.3)
       ├── List new features in this release
       └── Note any migration steps required

3. DURING DEPLOYMENT:
   ├── Follow DEPLOYMENT.md steps
   └── Document any deviations/issues

4. POST-DEPLOYMENT:
   └── UPDATE: llm_handover.md "Changelog"
       ├── Note deployment date
       ├── Note deployment environment (staging/prod)
       ├── Note any post-deployment fixes
       └── Update "Current Version" at top

5. IF DEPLOYMENT ISSUE:
   └── UPDATE: DEPLOYMENT.md "Troubleshooting"
       └── Add solution for future deployments

6. IF NEW DEPLOYMENT PROCEDURE:
   └── UPDATE: DEPLOYMENT.md
       └── Add to appropriate section

```

**Example Production Move Documentation:**

```markdown
## Changelog

### 2025-12-11 (PRODUCTION DEPLOYMENT - v1.8.3)

**Version:** 1.8.3  
**Environment:** Production  
**Deployed:** 2025-12-11 14:30 UTC

**New Features in This Release:**
- Fixed fallback analysis to use structured data
- Consolidated documentation (21 → 6 files)
- Enhanced error handling in content analyzer

**Migration Steps:**
- None required (backward compatible)

**Deployment Notes:**
- Rebuild required for frontend (CSS changes)
- Database migrations: None
- Environment variables: No changes
- Downtime: 2 minutes for container restart

**Post-Deployment Verification:**
- ✅ Health check passed
- ✅ Sample upload test passed
- ✅ Dashboard loads correctly
- ✅ All 9 pages functional
```

---

## 🔧 Phase 6: Other Activities + Documentation

### Alert Analysis (SAP/Skywind Alerts)

**SEQUENCE:**

```
1. READ REQUIREMENTS (MANDATORY):
   ├── prompt_read_the_flow.md (PHASE 3-7 for domain knowledge)
   ├── docs/th-context/analysis-rules/templates/quantitative-alert.yaml
   ├── .claude/rules/quantitative-alert-analysis.md
   └── .claude/rules/anti-hallucination-rules.md (Rule 11: No Embellishment)

2. READ ALERT ARTIFACTS:
   ├── Code_* (Alert logic)
   ├── Explanation_* (Business context)
   ├── Metadata_* (Parameters - ALL of them)
   └── Summary_* (Actual data to analyze)

3. ANALYZE ALERT (Following Template):
   ├── Extract metrics EXACTLY as they appear (no interpretation)
   ├── Apply analysis rules from template
   ├── Generate findings
   └── Calculate risk score

4. VERIFY DATA INTEGRITY (Anti-Hallucination Rule 11):
   ├── Report values EXACTLY as in source
   ├── DO NOT interpret or "fix" ambiguous fields
   ├── If parameters contradict data, REPORT discrepancy
   ├── Cross-check: Does data match metadata parameters?
   └── Flag uncertainties explicitly

5. DOCUMENT ANALYSIS:
   ├── CREATE: docs/analysis/{Module}_{AlertName}_Analysis.md
   ├── Follow EXACT structure from quantitative-alert.yaml
   ├── NOT in root directory!
   └── VERIFY structure matches template before saving

6. QUALITY CHECK (Quantitative Alert Analysis Checklist):
   ├── [ ] Key Findings is FIRST?
   ├── [ ] Business Context is SECOND?
   ├── [ ] Executive Summary has ALL 7 sections?
   ├── [ ] ALL parameters included (even empty ones)?
   ├── [ ] Source system identified?
   ├── [ ] Fraud indicator explicit (YES/NO/INVESTIGATE)?
   ├── [ ] Concentrations >50% flagged?
   ├── [ ] Manual override checked?
   └── [ ] Multi-currency converted to USD?

7. IF PATTERN DISCOVERED:
   └── UPDATE: llm_handover.md "Known Issues" or "Findings"
       └── Note the pattern for future reference
```

**Critical Alert Analysis Rules:**

**Template Adherence (NO EXCEPTIONS):**

```
⛔ BEFORE writing report:
   1. READ quantitative-alert.yaml
   2. FOLLOW structure EXACTLY
   3. DO NOT rename sections
   4. DO NOT omit subsections
   5. VIOLATION = REJECTED REPORT
```

**Data Integrity (Anti-Hallucination Rule 11):**

```
✅ Report values EXACTLY as they appear
✅ DO NOT interpret ambiguous fields
✅ If uncertain, state what source says AND flag uncertainty
❌ NEVER add ranges not in source
❌ NEVER "fix" data based on assumptions
```

**Multi-Currency Handling:**

```
1. Group data by currency first
2. Look up current exchange rates
3. Convert all to USD for totals
4. Show BOTH local AND USD
5. Document exchange rates used
```

### Code Investigation/Research

**SEQUENCE:**

```
1. INVESTIGATE:
   ├── Use grep/codebase_search
   ├── Read relevant files
   └── Take notes in temporary text file

2. DOCUMENT FINDINGS:
   
   IF architectural discovery:
   ├── Create GitHub issue
   └── UPDATE: llm_handover.md with link
   
   IF bug found:
   └── UPDATE: llm_handover.md "Known Issues"
   
   IF improvement idea:
   └── UPDATE: llm_handover.md "Roadmap"
   
   DO NOT:
   └── ❌ Create INVESTIGATION_XYZ.md in root

3. CLEANUP:
   └── Delete temporary notes (don't commit)
```

### Audit/Review

**SEQUENCE:**

```
1. PERFORM AUDIT:
   ├── Review codebase
   ├── Check for issues
   └── Document findings

2. DOCUMENT AUDIT:
   └── CREATE: docs/reports/AUDIT_YYYY-MM-DD.md
       └── NOT in root directory!

3. TRACK FIXES:
   └── UPDATE: llm_handover.md "Changelog"
       └── Reference audit report
```

### Refactoring

**SEQUENCE:**

```
1. PLAN REFACTORING:
   └── UPDATE: llm_handover.md "Current Work in Progress"
       ├── Describe what's being refactored
       ├── Describe why
       └── List affected files

2. DURING REFACTORING:
   ├── Make changes
   └── Keep llm_handover.md updated with progress

3. AFTER REFACTORING:
   └── UPDATE: llm_handover.md "Changelog"
       ├── Describe refactoring
       ├── Note breaking changes (if any)
       └── Update CLAUDE.md if structure changed
```

---

## 📊 Document Usage Matrix

Quick reference for which document to use when:

| Activity | Read | Update | Never Create |
|----------|------|--------|--------------|
| **Plan feature** | llm_handover.md, CLAUDE.md | llm_handover.md (Work in Progress) | ❌ PLAN_XYZ.md |
| **Develop code** | CLAUDE.md (conventions) | llm_handover.md (Changelog) | ❌ FEATURE_XYZ.md |
| **Debug issue** | llm_handover.md (Known Issues) | llm_handover.md (Known Issues, Changelog) | ❌ DEBUG_XYZ.md |
| **Test** | TESTING.md | llm_handover.md (Changelog) | ❌ TEST_RESULTS.md |
| **Deploy** | DEPLOYMENT.md | llm_handover.md (Changelog) | ❌ DEPLOY_NOTES.md |
| **Analyze alert** | prompt_read_the_flow.md | docs/analysis/*.md | ❌ Root ANALYSIS.md |
| **Audit** | All code | docs/reports/AUDIT_*.md | ❌ Root AUDIT.md |
| **Investigate** | Relevant code | GitHub issue OR llm_handover.md | ❌ INVESTIGATION.md |
| **Refactor** | CLAUDE.md | llm_handover.md, maybe CLAUDE.md | ❌ REFACTOR_XYZ.md |

---

## 🎯 The Single Source of Truth Rule

**ALWAYS REMEMBER:**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  llm_handover.md = THE SINGLE SOURCE OF TRUTH              │
│                                                             │
│  - Current state                                            │
│  - Current work                                             │
│  - Known issues                                             │
│  - Recent changes (Changelog)                               │
│  - Feature inventory                                        │
│  - Roadmap                                                  │
│                                                             │
│  When in doubt: UPDATE llm_handover.md                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 The 6-Document System Explained

### 1. **README.md** - User Entry Point

- **When to read:** User wants to get started
- **When to update:** Major user-facing features change
- **Contains:** Quick start, features overview, links to other docs
- **Never:** Create duplicate getting-started docs

### 2. **CLAUDE.md** - AI Assistant Technical Guide

- **When to read:** Need to understand project structure, conventions, file locations
- **When to update:** Project structure changes, new conventions, critical file changes
- **Contains:** Tech stack, project structure, API endpoints, conventions, key files
- **Never:** Document current work here (use llm_handover.md)

### 3. **llm_handover.md** - THE Source of Truth

- **When to read:** ALWAYS at session start
- **When to update:** ALWAYS after any significant work
- **Contains:** Current state, work in progress, known issues, changelog, features, roadmap
- **This is your primary document**

### 4. **prompt_read_the_flow.md** - Reading Sequence

- **When to read:** First time on project, doing alert analysis
- **When to update:** Rarely (only if reading sequence changes)
- **Contains:** Phase-by-phase reading order, domain knowledge paths
- **Never:** Document work here

### 5. **TESTING.md** - Testing Guide

- **When to read:** Running tests, verifying features
- **When to update:** New test procedures discovered
- **Contains:** Quick test (5 min), full checklist, troubleshooting, non-Docker testing
- **Never:** Document test results here (use llm_handover.md)

### 6. **DEPLOYMENT.md** - Deployment & Ops

- **When to read:** Deploying, troubleshooting Docker/infra issues
- **When to update:** New deployment procedures, new troubleshooting solutions
- **Contains:** Docker setup, deployment steps, troubleshooting, environment vars
- **Never:** Document code changes here (use llm_handover.md)

### 7. **CONTRIBUTING.md** - Optional

- **When to read:** Contributing to the project
- **When to update:** Contribution process changes
- **Contains:** How to contribute, coding standards, PR process
- **Optional:** Only if accepting external contributions

---

## ✅ Decision Tree: Where Should I Document This?

```
START: I need to document something
│
├─ Is it current work/state?
│  └─ YES → UPDATE llm_handover.md
│
├─ Is it a completed feature/bug fix?
│  └─ YES → UPDATE llm_handover.md "Changelog"
│
├─ Is it a known issue/bug?
│  └─ YES → UPDATE llm_handover.md "Known Issues"
│
├─ Is it a future enhancement?
│  └─ YES → UPDATE llm_handover.md "Roadmap"
│
├─ Is it an alert analysis?
│  └─ YES → CREATE docs/analysis/{Module}_{Alert}_Analysis.md
│
├─ Is it an audit report?
│  └─ YES → CREATE docs/reports/AUDIT_YYYY-MM-DD.md
│
├─ Is it a test procedure?
│  └─ YES → UPDATE TESTING.md
│
├─ Is it deployment/ops related?
│  └─ YES → UPDATE DEPLOYMENT.md
│
├─ Is it architectural/design?
│  └─ YES → Create GitHub issue + link in llm_handover.md
│
├─ Is it project structure change?
│  └─ YES → UPDATE CLAUDE.md
│
├─ Is it temporary investigation?
│  └─ YES → Use inline comments or temporary file (don't commit)
│
└─ Still unsure?
   └─ DEFAULT → UPDATE llm_handover.md
```

---

## ⚠️ Common Mistakes to Avoid

### ❌ DON'T DO THIS

1. **Creating new root-level .md files**

   ```
   ❌ ANALYSIS_XYZ.md
   ❌ FEATURE_ABC.md
   ❌ BUG_INVESTIGATION.md
   ❌ NOTES.md
   ```

2. **Updating multiple docs with same info**

   ```
   ❌ Update llm_handover.md AND create FEATURE.md
   ❌ Update CLAUDE.md AND README.md with same content
   ```

3. **Creating temporary analysis documents**

   ```
   ❌ OMITTED_PROCEDURES_ANALYSIS.md in root
   ✅ Create in docs/reports/ OR GitHub issue
   ```

4. **Documenting test results in separate file**

   ```
   ❌ TEST_RESULTS_2025-12-11.md
   ✅ Update llm_handover.md "Changelog" with test results
   ```

5. **Creating roadmap/feature docs**

   ```
   ❌ NEXT_STEPS.md
   ❌ FEATURES.md
   ✅ Update llm_handover.md "Roadmap" and "Feature Inventory"
   ```

### ✅ DO THIS INSTEAD

1. **Document current work**

   ```
   ✅ UPDATE llm_handover.md "Current Work in Progress"
   ```

2. **Document completed work**

   ```
   ✅ UPDATE llm_handover.md "Changelog"
   ```

3. **Document investigations**

   ```
   ✅ Create GitHub issue
   ✅ OR add to docs/reports/
   ✅ Link from llm_handover.md
   ```

4. **Document tests**

   ```
   ✅ UPDATE TESTING.md with new procedures
   ✅ UPDATE llm_handover.md with test results
   ```

5. **Document future plans**

   ```
   ✅ UPDATE llm_handover.md "Roadmap"
   ```

---

## 🔄 Session Start Checklist

At the beginning of every session:

```
□ INTERNALIZE MANDATORY RULES
  □ Review .claude/rules/anti-hallucination-rules.md key points
  □ Remember: VERIFY before claiming
  □ Remember: NO assumptions as facts
  □ Remember: Truth is highest value

□ Read llm_handover.md completely
  □ Note current version
  □ Check "Current Work in Progress"
  □ Review "Known Issues"
  □ Read recent changelog entries (last 2-3)

□ Check if working on existing task
  □ If YES: Continue from llm_handover.md notes
  □ If NO: Plan new task in llm_handover.md

□ Check CLAUDE.md if needed
  □ Only if unclear on project structure
  □ Only if need to find specific files
  □ Only if need coding conventions

□ If doing alert analysis:
  □ READ .claude/rules/quantitative-alert-analysis.md
  □ READ docs/th-context/analysis-rules/templates/quantitative-alert.yaml
  □ Understand template MUST be followed exactly

□ Begin work
  □ Update llm_handover.md as you progress
  □ Document decisions inline in code
  □ VERIFY all changes with read_file
  □ Test changes
```

---

## 🎓 Session End Checklist

Before ending a session:

```
□ VERIFY ALL CLAIMS (Anti-Hallucination Protocol)
  □ Did I read_file after EVERY edit to verify?
  □ Am I reporting facts or assumptions?
  □ Can I prove every claim with actual file content?
  □ Did I use tentative language until verified?

□ Update llm_handover.md (MANDATORY)
  □ If work completed: Add to "Changelog"
  □ If work ongoing: Update "Current Work in Progress"
  □ If issues found: Add to "Known Issues"
  □ Note any blockers/questions
  □ ⚠️ CANNOT mark complete without this update

□ CHECK FOR UNCOMMITTED CHANGES (Preserve Working Code)
  □ Run git status to check file states
  □ If uncommitted changes exist:
    □ Document in llm_handover.md
    □ Suggest committing to user
    □ Warn user code could be lost if not committed

□ Commit work if requested by user
  □ Write descriptive commit message
  □ Reference llm_handover.md changelog entry
  □ NEVER use destructive git commands without user approval

□ Suggest next steps to user
  □ Based on Roadmap in llm_handover.md
  □ Based on Known Issues that need fixing
  □ Be honest about blockers/limitations

□ DO NOT leave:
  □ Uncommitted temporary files
  □ Unfinished analysis documents in root
  □ Investigation notes in root
  □ Unverified claims of success
  □ Outdated llm_handover.md
```

---

## 📈 Benefits of This Workflow

By following this workflow, you ensure:

✅ **No document sprawl** - Only 6-7 core documents  
✅ **Single source of truth** - llm_handover.md is authoritative  
✅ **Easy information finding** - Know exactly where to look  
✅ **Clear responsibilities** - Each document has specific purpose  
✅ **Consistent practice** - Same workflow every time  
✅ **Efficient onboarding** - New agents read 2-3 files, not 21  
✅ **Better collaboration** - All agents follow same process  
✅ **Reduced confusion** - No conflicting information  
✅ **Easier maintenance** - Update 1 place, not 5  

---

## 🆘 Quick Reference Card

**Most Common Actions:**

| I want to... | Do this... |
|--------------|------------|
| Start session | Read llm_handover.md |
| Plan work | Update llm_handover.md "Work in Progress" |
| Code feature | Follow CLAUDE.md conventions |
| Complete work | Update llm_handover.md "Changelog" |
| Fix bug | Update llm_handover.md "Known Issues" + "Changelog" |
| Test | Read TESTING.md, document results in llm_handover.md |
| Deploy | Read DEPLOYMENT.md, document in llm_handover.md |
| Troubleshoot | Read DEPLOYMENT.md "Troubleshooting" |
| Analyze alert | Read prompt_read_the_flow.md, create in docs/analysis/ |
| Unsure | Update llm_handover.md (default) |

---

**Remember:** When in doubt, update `llm_handover.md`. It's the single source of truth.

---

## 📖 Mandatory Rules Reference

### Anti-Hallucination Protocol (14 Rules)

**Source:** `.claude/rules/anti-hallucination-rules.md`

#### Core Verification Rules

**RULE 1: VERIFY BEFORE CLAIMING**

- NEVER report change without reading file afterward
- ALWAYS use `read_file` IMMEDIATELY after edit
- ONLY report success after verification

**RULE 2: NO ASSUMPTIONS AS FACTS**

- NEVER say "I have implemented" - say "I attempted, let me verify"
- ALWAYS distinguish "I tried" vs "I successfully completed"

**RULE 3: MANDATORY VERIFICATION WORKFLOW**

```
1. Execute change (search_replace, write, etc.)
2. IMMEDIATELY run read_file to check result
3. Compare actual vs intended
4. ONLY THEN report what actually happened
5. If failed, try alternative and repeat
```

**RULE 4: HONEST REPORTING**

- NEVER say "All files updated" without reading each
- NEVER report percentages without actual verification
- When caught in inaccuracy, ACKNOWLEDGE immediately

**RULE 5: COST CONSCIOUSNESS**

- User pays for accurate work, not hallucinations
- Wasted iterations cost real money
- Accuracy > speed

**RULE 6: NO CONFIDENCE WITHOUT VERIFICATION**

- Use tentative language until verified
- Read files before claiming contents

**RULE 7: ANTI-HALLUCINATION MANDATE**

- Choose ACCURACY over CONVENIENCE
- Admit uncertainty instead of plausible guesses

**RULE 8: NO "YESMAN" BEHAVIOR**

- Answer honestly, not "plausibly"
- Truth over politeness

**RULE 9: TRUTH AS HIGHEST VALUE**

- Honest uncertainty > confident incorrectness

**RULE 10: FILE READING STATUS PROTOCOL**

- Present simple ✅ READ or ❌ NOT READ status
- DO NOT offer workarounds without user direction

**RULE 11: DATA INTERPRETATION - NO EMBELLISHMENT**

- Report values EXACTLY as they appear
- DO NOT interpret or "fix" based on assumptions
- If ambiguous, report verbatim and flag uncertainty

**RULE 12: LITERAL VALUE COMPLIANCE**

- Use EXACT values specified by user
- "16px" means 16px, not "something close"
- DO NOT substitute your judgment

**RULE 13: NO INTERPRETATION SUBSTITUTION**

- If user says X, do X - not what you think they meant
- Specific beats general

**RULE 14: ANTI-OVERCONFIDENCE PROTOCOL**

- DO NOT skim instructions
- Parse word by word when specific values present
- Speed is worthless if output is wrong

---

### Preserve Working Code Rules

**Source:** `.claude/rules/preserve-working-code.md`

#### Before ANY Git Operation

**Check for uncommitted changes:**

```bash
git status <file>
```

**If file is modified (M) or untracked (??):**

1. DO NOT run git checkout on it
2. ASK USER: "File has uncommitted changes. Backup first?"
3. Create backup: `cp <file> <file>.backup`

**Destructive Git Commands:**

- `git checkout <file>` - DESTROYS local changes
- `git reset --hard` - DESTROYS all uncommitted
- `git clean -fd` - DESTROYS untracked files
- `git stash` without pop - Can lose work

**Protocol:**

1. List what will be affected
2. Confirm with user
3. Backup if necessary

**After successful development:**

1. Document in llm_handover.md
2. Suggest committing to user
3. Warn if user declines

---

### LLM Handover Maintenance Rules

**Source:** `.claude/rules/llm-handover-maintenance.md`

#### When to Update llm_handover.md

**MUST update in these situations:**

1. **After Verified Milestones**
   - Feature completed and tested
   - Bug fixed and verified
   - Deployment successful
   - Major refactoring complete

2. **After Significant Changes**
   - New dependencies added
   - Database schema changes
   - API endpoint changes
   - Configuration changes
   - Architecture changes

3. **Project State Updates**
   - Git status changes
   - Environment changes
   - Known issues discovered/resolved
   - Testing results
   - Deployment status

4. **Documentation Updates**
   - New .md files created
   - README updates
   - API docs changes

#### What to Update

Required sections:

1. Header (date, status, version)
2. Current Project State
3. Recent Milestones
4. Known Issues
5. Architecture Overview
6. API Endpoints
7. Environment Configuration
8. Git & Version Control Status
9. Common Issues & Solutions
10. Next Steps & Roadmap
11. **Changelog** (ALWAYS)

#### Update Format

```markdown
### YYYY-MM-DD (DESCRIPTION)

**What Changed:**
- Created/Added/Fixed: Specific description
- Files Modified: List with paths
- Verification: Test results

**Impact:**
- Breaking changes (if any)
- Migration steps (if any)
```

#### Verification Checklist

Before marking complete:

- [ ] All code changes tested
- [ ] llm_handover.md updated
- [ ] Changelog entry added
- [ ] Git status documented
- [ ] Known issues section current

**NON-NEGOTIABLE:** Cannot mark task complete without updating llm_handover.md.

---

### Quantitative Alert Analysis Rules

**Source:** `.claude/rules/quantitative-alert-analysis.md`

**Applies to:** Analyzing Skywind 4C alerts with measurable data (financial amounts, counts, percentages)

#### Template Adherence (CRITICAL)

**Before EVERY analysis report:**

1. READ `docs/th-context/analysis-rules/templates/quantitative-alert.yaml`
2. FOLLOW structure EXACTLY as defined
3. DO NOT rename sections
4. DO NOT omit subsections
5. DO NOT add creative variations

**VIOLATION = REJECTED REPORT**

#### Mandatory Document Structure

Reports MUST follow this exact order:

1. **KEY FINDINGS** (Must be First)
   - Metrics Table (4-row format)
   - Critical Discovery (bold heading, 3 bullets)
   - Concentration Pattern (one table + note)

2. **BUSINESS CONTEXT** (After Key Findings)
   - Business Purpose (blockquote from Explanation file)
   - What This Alert Monitors
   - Why It Matters (table)
   - Interpreting the Findings (table)

3. **EXECUTIVE SUMMARY**
   - Alert Identity
   - Execution Context
   - Alert Parameters (ALL, even empty ones)
   - The Bottom Line
   - What Happened
   - Top 3 Findings
   - Immediate Actions

4. **KEY METRICS**
5. **CONCENTRATION ANALYSIS**
6. **RISK ASSESSMENT**
7. **RECOMMENDED ACTIONS**
8. **TECHNICAL DETAILS** (Last)

#### Critical Rules

**Parameters:**

- Include ALL parameters from Metadata
- Show empty as "(none)"
- BACKDAYS is filter, NOT divisor

**Source System:**

- Always identify (PS4, ECC, etc.)
- Critical for multi-instance clients

**Manual Override Check:**

- Check for manual flags (MPROK='A')
- Manual + large loss = RED FLAG

**Fraud Indicator:**

- MUST explicitly state: YES, NO, or INVESTIGATE
- Never leave ambiguous

**Concentration:**
>
- >50% in single entity = FLAG IT
- Bold the entity

**Multi-Currency:**

- Group by currency first
- Convert all to USD for totals
- Show both local AND USD
- Document exchange rates used

#### Formatting Standards

**Numbers:**

- Currency: `$14,152,997`
- Large in text: `$14.15M`
- Percentages: `81%` or `81.2%`
- Counts: `2,044`

**Tables:**

- Markdown tables
- Bold key figures
- Right-align numbers

**Emphasis:**

- **Bold** for critical findings
- **UPPERCASE** for warnings
- Start actions with verbs

#### Quality Checklist

Before finalizing:

- [ ] Key Findings is FIRST?
- [ ] All 3 subsections in Key Findings?
- [ ] Business Context is SECOND?
- [ ] Business Purpose from Explanation file?
- [ ] Executive Summary has ALL 7 sections?
- [ ] ALL parameters included (even empty)?
- [ ] Source system identified?
- [ ] Concentrations >50% highlighted?
- [ ] Manual override checked?
- [ ] Fraud indicator explicit?
- [ ] Actions specific and actionable?
- [ ] JSON output included?
- [ ] Multi-currency grouped and converted?

---

## 🔄 Integrated Workflow with Rules

### Phase-Specific Rule Application

Each development phase integrates these rules:

**Planning Phase:**

- Apply: Handover Maintenance (document plan)
- Apply: Anti-Hallucination (verify assumptions)

**Development Phase:**

- Apply: Anti-Hallucination (verify all changes)
- Apply: Handover Maintenance (real-time updates)
- Apply: Preserve Working Code (before git ops)

**Debugging Phase:**

- Apply: Anti-Hallucination (verify findings)
- Apply: Handover Maintenance (document bugs)

**Testing Phase:**

- Apply: Anti-Hallucination (verify test results)
- Apply: Handover Maintenance (document results)

**Deployment Phase:**

- Apply: Preserve Working Code (git safety)
- Apply: Handover Maintenance (deployment notes)

**Alert Analysis Phase:**

- Apply: Quantitative Alert Analysis (template adherence)
- Apply: Data Interpretation (no embellishment)
- Apply: Handover Maintenance (document findings)

---

*This workflow ensures consistent, organized, and efficient development on the THA project while maintaining the highest standards of accuracy and safety.*
