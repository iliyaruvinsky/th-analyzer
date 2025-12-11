# JUNK Folder - Deprecated Documentation

**Date Archived:** 2025-12-11  
**Reason:** Document consolidation to reduce overlap and improve AI agent focus

---

## Why These Files Were Moved Here

The project had **21+ markdown files** at root level with significant overlap. This caused:
- AI agents reading outdated/conflicting instructions
- Maintenance burden (updating same info in 5+ places)
- User confusion about which document is authoritative

## Consolidation Results

**From 21 documents → To 6 core documents**

### New Structure (KEEP - In Root)

1. **README.md** - User entry point
2. **CLAUDE.md** - AI assistant guide (authoritative tech reference)
3. **llm_handover.md** - Current state, changelog (THE source of truth)
4. **prompt_read_the_flow.md** - AI reading sequence
5. **TESTING.md** - Consolidated testing guide
6. **DEPLOYMENT.md** - Deployment + Docker troubleshooting
7. **CONTRIBUTING.md** - Contribution guidelines (if accepting PRs)

### Files in This Folder (DEPRECATED - Merged)

| File | Content Merged To |
|------|-------------------|
| `FEATURES.md` | → `llm_handover.md` (Feature Inventory section) |
| `NEXT_STEPS.md` | → `llm_handover.md` (Roadmap section) |
| `QUICK_START.md` | → `README.md` (Quick Start section) |
| `QUICK_TEST.md` | → `TESTING.md` |
| `TESTING_GUIDE.md` | → `TESTING.md` |
| `TESTING_CHECKLIST.md` | → `TESTING.md` |
| `TESTING_WITHOUT_DOCKER.md` | → `TESTING.md` |
| `DOCKER_SETUP_GUIDE.md` | → `DEPLOYMENT.md` |
| `DOCKER_TROUBLESHOOTING.md` | → `DEPLOYMENT.md` |
| `REBUILD_FRONTEND.md` | → `DEPLOYMENT.md` |
| `llm_prompt.md` | → Deleted (redundant with llm_handover.md) |
| `SETUP_NEW_COMPUTER.md` | → Deleted (covered in README.md) |
| `SKYWIND-PLUGIN-MARKETPLACE-STRUCTURE.md` | → Should be in `plugins/README.md` |

---

## Can These Files Be Deleted?

**Yes, safely.** All content has been merged into the core 6 documents.

However, they're kept here temporarily for:
1. Recovery if something was missed
2. Reference during transition period
3. User comfort (can review before permanent deletion)

**Recommended:** After 1-2 weeks, if no issues found, these can be permanently deleted.

---

## Related Changes

- **Created:** `TESTING.md` (consolidates 4 testing docs)
- **Updated:** `README.md` (added Quick Start)
- **Updated:** `DEPLOYMENT.md` (added Docker setup & troubleshooting)
- **Updated:** `llm_handover.md` (added Feature Inventory & Roadmap)
- **Moved:** `AUDIT_REPORT_2025-12-10.md` → `docs/reports/`

---

## Document Structure Analysis

For full details on the consolidation, see:
- `DOCUMENT_STRUCTURE_ANALYSIS.md` (in root)

---

*Archived during document consolidation - 2025-12-11*

