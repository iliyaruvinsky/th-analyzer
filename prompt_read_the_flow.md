# LLM Context Reading Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   IF YOU ARE NOT IN CONTEXT - READ THIS FILE FIRST:                         │
│   C:\Users\USER\Desktop\tha-new\prompt_read_the_flow.md                     │
│                                                                             │
│   Then follow the reading sequence below.                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

> **Purpose:** This document defines the exact reading order for an LLM to understand the THA (Treasure Hunt Analyzer) project context before performing any work.

---

## Reading Order Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MANDATORY READING SEQUENCE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   PHASE 1: FOUNDATION (Project Structure)                                   │
│   ├── CLAUDE.md                     ← Project overview, tech stack          │
│   └── llm_handover.md               ← Current state, recent changes         │
│                                                                             │
│   PHASE 2: BEHAVIORAL RULES (How to Behave)                                 │
│   ├── .claude/rules/anti-hallucination-rules.md    ← CRITICAL behaviors     │
│   └── .claude/rules/llm-handover-maintenance.md    ← Documentation rules    │
│                                                                             │
│   PHASE 3: DOMAIN KNOWLEDGE (What You're Analyzing)                         │
│   ├── docs/th-context/skywind-4c-knowledge.md      ← Skywind 4C system      │
│   └── docs/th-context/readmore/*.md                ← 6 Focus Areas          │
│                                                                             │
│   PHASE 4: ANALYSIS WORKFLOW (How to Analyze)                               │
│   ├── .claude/rules/quantitative-alert-analysis.md ← Enforcement rules      │
│   ├── docs/th-context/analysis-rules/QUANTITATIVE_ALERT_WORKFLOW.md         │
│   └── docs/th-context/analysis-rules/ALERT_CLASSIFICATION_PRINCIPLES.md     │
│                                                                             │
│   PHASE 5: TEMPLATES & FORMATTING (Output Structure)                        │
│   ├── docs/th-context/analysis-rules/templates/quantitative-alert.yaml      │
│   └── docs/th-context/analysis-rules/presentation-rules.yaml                │
│                                                                             │
│   PHASE 6: SCORING & CLASSIFICATION (How to Score)                          │
│   └── docs/scoring-rules/BUSINESS_PROTECTION.md    ← Severity classification│
│                                                                             │
│   PHASE 7: EXAMPLES (Reference Analyses)                                    │
│   └── docs/analysis/*.md                           ← Completed analyses     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Foundation (READ FIRST)

These documents establish project context and current state.

### 1.1 CLAUDE.md
**Path:** `CLAUDE.md`
**Purpose:** Master project guide for AI assistants
**Contains:**
- Project overview (THA = Treasure Hunt Analyzer)
- Technology stack (FastAPI, React, PostgreSQL)
- Directory structure
- API endpoints
- Development workflows
- Key files reference

**Read time:** ~5 minutes

### 1.2 llm_handover.md
**Path:** `llm_handover.md`
**Purpose:** Current project state and session continuity
**Contains:**
- Recent milestones
- What's working / what's broken
- Current work in progress
- Known issues
- Changelog

**Read time:** ~3 minutes

**CRITICAL:** This document must be updated after each verified milestone.

---

## Phase 2: Behavioral Rules (MANDATORY)

These rules govern LLM behavior. **Violations are unacceptable.**

### 2.1 anti-hallucination-rules.md
**Path:** `.claude/rules/anti-hallucination-rules.md`
**Purpose:** Prevent hallucination, enforce verification
**Contains:**
- Rule 1: Verify before claiming
- Rule 2: No assumptions as facts
- Rule 3: Mandatory verification workflow
- Rule 4: Honest reporting
- Rule 5: Cost consciousness
- Rule 6: No confidence without verification
- Rule 7: Anti-hallucination mandate
- Rule 8: No "yesman" behavior
- Rule 9: Truth as highest value
- Rule 10: File reading status protocol
- Rule 11: Data interpretation - no embellishment

**Read time:** ~3 minutes

**CRITICAL:** These rules override default behavior.

### 2.2 llm-handover-maintenance.md
**Path:** `.claude/rules/llm-handover-maintenance.md`
**Purpose:** Rules for maintaining handover document
**Contains:**
- When to update llm_handover.md
- What sections to update
- Verification requirements

**Read time:** ~2 minutes

---

## Phase 3: Domain Knowledge

Understand what you're analyzing.

### 3.1 skywind-4c-knowledge.md
**Path:** `docs/th-context/skywind-4c-knowledge.md`
**Purpose:** Consolidated Skywind 4C platform knowledge
**Contains:**
- Core terminology (Exception Indicator, Alert Instance, Alert Template)
- 4C artifact structure (Code, Summary, Metadata, Explanation)
- Module codes (FI, MM, SD, MD, PUR)
- Field mappings
- Parameter meanings (BACKDAYS, PERC_VARI, etc.)

**Read time:** ~5 minutes

### 3.2 Focus Area Definitions
**Path:** `docs/th-context/readmore/`
**Purpose:** Detailed explanation of each Focus Area
**Files to read:**
1. `ReadMore_BusinessProtection.md` - Fraud, cybersecurity
2. `ReadMore_BusinessControl.md` - Process anomalies
3. `ReadMore_AccessGovernance.md` - SoD violations
4. `ReadMore_TechnicalControl.md` - Infrastructure issues
5. `ReadMore_JobsControl.md` - Job performance
6. `ReadMore_S4HANAExcellence.md` - Migration safeguards

**Read time:** ~10 minutes total

---

## Phase 4: Analysis Workflow

How to analyze alerts step-by-step.

### 4.1 quantitative-alert-analysis.md (ENFORCEMENT)
**Path:** `.claude/rules/quantitative-alert-analysis.md`
**Purpose:** Mandatory rules for quantitative alert analysis
**Contains:**
- Template adherence requirement
- Mandatory document structure
- Section order (Key Findings → Business Context → Executive Summary → ...)
- Formatting standards
- Quality checklist

**Read time:** ~3 minutes

**CRITICAL:** This is the enforcement document. Non-compliance = rejected report.

### 4.2 QUANTITATIVE_ALERT_WORKFLOW.md
**Path:** `docs/th-context/analysis-rules/QUANTITATIVE_ALERT_WORKFLOW.md`
**Purpose:** Detailed workflow with visual diagrams
**Contains:**
- 4 input artifacts (Code, Summary, Metadata, Explanation)
- Processing flow diagram
- Step-by-step process
- Artifact-to-section mapping
- Output location: `docs/analysis/{Module}_{AlertName}_Analysis.md`
- Pattern recognition catalog
- Data segmentation principle

**Read time:** ~8 minutes

### 4.3 ALERT_CLASSIFICATION_PRINCIPLES.md
**Path:** `docs/th-context/analysis-rules/ALERT_CLASSIFICATION_PRINCIPLES.md`
**Purpose:** Core principle that severity is context-dependent
**Contains:**
- Quantitative vs Qualitative alerts
- Severity determination rules
- Data quality vs fraud distinction
- Decision matrix

**Read time:** ~3 minutes

---

## Phase 5: Templates & Formatting

Exact output structure requirements.

### 5.1 quantitative-alert.yaml (TEMPLATE)
**Path:** `docs/th-context/analysis-rules/templates/quantitative-alert.yaml`
**Purpose:** Defines exact report structure
**Contains:**
- Section definitions
- Required subsections
- Field requirements
- Formatting rules
- Quality checklist

**Read time:** ~5 minutes

**CRITICAL:** Every report must follow this template EXACTLY.

### 5.2 presentation-rules.yaml
**Path:** `docs/th-context/analysis-rules/presentation-rules.yaml`
**Purpose:** How to present findings
**Contains:**
- Core principles (Executive Summary first, Numbers before narrative)
- Table formatting
- Number formatting ($14,152,997 vs $14.15M)
- Risk indicator formatting

**Read time:** ~3 minutes

---

## Phase 6: Scoring & Classification

How to assign severity and risk scores.

### 6.1 BUSINESS_PROTECTION.md
**Path:** `docs/scoring-rules/BUSINESS_PROTECTION.md`
**Purpose:** Severity classification rules
**Contains:**
- Foundational principle: Alerts expose POSSIBILITIES, not confirmations
- CRITICAL severity (base 90): Cybersecurity breach, direct theft
- HIGH severity (base 75): Possible fraud patterns
- MEDIUM severity (base 60): SoD violations, process deviations
- LOW severity (base 50): Tracking, housekeeping
- Scoring factors summary
- Data source principle (Summary_* only for quantities)

**Read time:** ~5 minutes

---

## Phase 7: Examples (Reference)

Learn from completed analyses.

### 7.1 Completed Analysis Examples
**Path:** `docs/analysis/`
**Purpose:** Reference for expected output format

**Recommended reading order:**
1. `SD_Billing_Document_Status_Analysis.md` - Clean SD example
2. `MD_Modified_Vendor_Bank_Account_Analysis.md` - Fraud indicator example
3. `MM_Material_Standard_Price_Change_Analysis.md` - Data quality example
4. `FI_Exceptional_Posting_GL_Account_Analysis.md` - FI module example

**Read time:** ~15 minutes for 4 examples

---

## Quick Reference: File Purposes

| File | Purpose | Priority |
|------|---------|----------|
| `CLAUDE.md` | Project overview | PHASE 1 |
| `llm_handover.md` | Current state | PHASE 1 |
| `anti-hallucination-rules.md` | Behavioral rules | PHASE 2 |
| `llm-handover-maintenance.md` | Documentation rules | PHASE 2 |
| `skywind-4c-knowledge.md` | Domain knowledge | PHASE 3 |
| `readmore/*.md` | Focus Area definitions | PHASE 3 |
| `quantitative-alert-analysis.md` | Enforcement rules | PHASE 4 |
| `QUANTITATIVE_ALERT_WORKFLOW.md` | Workflow details | PHASE 4 |
| `ALERT_CLASSIFICATION_PRINCIPLES.md` | Classification | PHASE 4 |
| `quantitative-alert.yaml` | Report template | PHASE 5 |
| `presentation-rules.yaml` | Formatting rules | PHASE 5 |
| `BUSINESS_PROTECTION.md` | Scoring rules | PHASE 6 |
| `docs/analysis/*.md` | Examples | PHASE 7 |

---

## Minimum Required Reading

If time is limited, read AT LEAST these documents:

```
CRITICAL PATH (15 minutes):
1. CLAUDE.md                                    ← Project context
2. llm_handover.md                              ← Current state
3. .claude/rules/anti-hallucination-rules.md    ← Behavioral rules
4. .claude/rules/quantitative-alert-analysis.md ← Analysis rules
5. docs/th-context/analysis-rules/templates/quantitative-alert.yaml ← Template
```

---

## Document Update Triggers

When to re-read documents:

| Trigger | Documents to Re-read |
|---------|---------------------|
| Starting new session | `llm_handover.md` |
| Before any analysis | `quantitative-alert-analysis.md`, `quantitative-alert.yaml` |
| After completing analysis | Update `llm_handover.md` |
| New Focus Area encountered | Relevant `readmore/*.md` |
| Classification uncertainty | `BUSINESS_PROTECTION.md`, `ALERT_CLASSIFICATION_PRINCIPLES.md` |

---

## Verification Checklist

Before starting any analysis work, verify:

- [ ] Read `CLAUDE.md` for project structure
- [ ] Read `llm_handover.md` for current state
- [ ] Read `anti-hallucination-rules.md` for behavioral rules
- [ ] Read `quantitative-alert-analysis.md` for analysis rules
- [ ] Read `quantitative-alert.yaml` for template structure
- [ ] Know output location: `docs/analysis/{Module}_{AlertName}_Analysis.md`

---

## Additional Reference Documents

These are supporting documents for specific scenarios:

### Product Documentation
- `docs/product-docs/Skywind SAP Protection & Anti-Fraud Documentation.md`
- `docs/product-docs/Skywind SoDA.md`

### Technical Setup
- `DOCKER_SETUP_GUIDE.md`
- `QUICK_START.md`
- `README.md`

### Field Mappings
- `docs/th-context/analysis-rules/field-mappings/sd-fields.yaml`

### Frontend Development
- `.claude/skills/frontend-design/SKILL.md`

---

## Summary

```
Total documents in reading flow: 20+
Minimum critical path: 5 documents (~15 minutes)
Full context read: ~60 minutes

OUTPUT LOCATION: docs/analysis/{Module}_{AlertName}_Analysis.md
TEMPLATE: docs/th-context/analysis-rules/templates/quantitative-alert.yaml
ENFORCEMENT: .claude/rules/quantitative-alert-analysis.md
```

---

*Document created: 2025-11-30*
*Purpose: LLM context initialization for THA project*
