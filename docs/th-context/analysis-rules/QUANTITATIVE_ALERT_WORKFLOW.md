# Quantitative Alert Analysis Workflow

> **Version:** 1.2 | **Last Updated:** 28 November 2025

---

## ⛔ MANDATORY RULE - READ BEFORE EVERY ANALYSIS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   BEFORE CREATING ANY ANALYSIS REPORT:                                      │
│                                                                             │
│   1. READ the template: templates/quantitative-alert.yaml                   │
│   2. FOLLOW the structure EXACTLY - no deviations                           │
│   3. VERIFY all required sections are present                               │
│                                                                             │
│   CLIENT REPORTS MUST BE 100% CONSISTENT IN FORMAT                          │
│   NO EXCEPTIONS. NO CREATIVE VARIATIONS.                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Required Report Structure (from template)

| Section | Position | Required |
|---------|----------|----------|
| **Business Context** | FIRST | YES |
| ├─ Business Purpose | blockquote | YES |
| ├─ What This Alert Monitors | paragraph | YES |
| ├─ Why It Matters | table | YES |
| └─ Interpreting Findings | table | Optional |
| **Executive Summary** | SECOND | YES |
| ├─ Alert Identity | table | YES |
| ├─ Execution Context | table | YES |
| ├─ Alert Parameters | table | YES |
| ├─ The Bottom Line | table | YES |
| ├─ What Happened | paragraph | YES |
| ├─ Top Findings | numbered list | YES |
| └─ Immediate Actions | numbered list | YES |
| **Key Metrics** | after summary | YES |
| **Concentration Analysis** | after metrics | YES |
| **Risk Assessment** | after concentration | YES |
| **Recommended Actions** | after risk | YES |
| **Technical Details** | LAST | Optional |

**FAILURE TO FOLLOW THIS STRUCTURE = REJECTED REPORT**

---

## The 4 Input Artifacts

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ALERT FOLDER STRUCTURE                               │
│  docs/skywind-4c-alerts-output/Applications/{MODULE}/{ID} - {AlertName}/    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Code_*.txt           ─── ABAP/SQL detection logic                       │
│  2. Summary_*.xlsx       ─── Actual findings data (the records)             │
│  3. Metadata_*.xlsx      ─── Alert configuration & parameters               │
│  4. Explanation_*.*      ─── Business purpose (PDF, DOCX, or HTML)          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Note on Explanation File Formats:**
- `.pdf` - Read directly with Read tool
- `.docx` - Use Python `python-docx` library via Bash
- `.html` - Read directly with Read tool (parse HTML tags)

## Graphical Processing Flow

```
                              ┌──────────────────────┐
                              │   START ANALYSIS     │
                              └──────────┬───────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
        ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
        │  1. EXPLANATION   │ │   2. METADATA     │ │    3. CODE        │
        │     (.pdf)        │ │    (.xlsx)        │ │    (.txt)         │
        └─────────┬─────────┘ └─────────┬─────────┘ └─────────┬─────────┘
                  │                     │                     │
                  ▼                     ▼                     ▼
        ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
        │ Extract Business  │ │ Extract:          │ │ Understand:       │
        │ Purpose (why it   │ │ • Alert Identity  │ │ • Detection logic │
        │ matters)          │ │ • Source System   │ │ • Field names     │
        │                   │ │ • Parameters      │ │ • Thresholds      │
        │ Output: Blockquote│ │ • Execution date  │ │ • Manual flags    │
        └─────────┬─────────┘ └─────────┬─────────┘ └─────────┬─────────┘
                  │                     │                     │
                  └──────────┬──────────┴──────────┬──────────┘
                             │                     │
                             ▼                     │
                  ┌───────────────────────┐        │
                  │   BUILD CONTEXT       │        │
                  │   (Understanding)     │◄───────┘
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │   4. SUMMARY DATA     │
                  │      (.xlsx)          │
                  └───────────┬───────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────────────┐
        │              QUANTITATIVE ANALYSIS                   │
        ├─────────────────────────────────────────────────────┤
        │                                                      │
        │  Step A: Currency Detection & Grouping               │
        │          └─► Identify all currencies                 │
        │          └─► Group records by currency               │
        │          └─► Get exchange rates (web search)         │
        │                                                      │
        │  Step B: Financial Impact Calculation                │
        │          └─► Sum by currency                         │
        │          └─► Convert to USD                          │
        │          └─► Calculate: total, avg, max              │
        │                                                      │
        │  Step C: Concentration Analysis                      │
        │          └─► Group by: Org, Entity, Customer         │
        │          └─► Flag >50% concentrations                │
        │          └─► Identify top 5 largest transactions     │
        │                                                      │
        │  Step D: Pattern Detection                           │
        │          └─► Manual vs System entries                │
        │          └─► Zero-price patterns                     │
        │          └─► Anomaly identification                  │
        │                                                      │
        │  Step E: Risk Classification                         │
        │          └─► Focus Area (6 options)                  │
        │          └─► Severity (CRITICAL/HIGH/MEDIUM/LOW)     │
        │          └─► Risk Score (0-100)                      │
        │          └─► Fraud Indicator (YES/NO/INVESTIGATE)    │
        │                                                      │
        └─────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────────────┐
        │              REPORT GENERATION                       │
        │         (Following Template Structure)               │
        ├─────────────────────────────────────────────────────┤
        │                                                      │
        │  SECTION 1: BUSINESS CONTEXT ◄─── From Explanation   │
        │             (First - before any data)                │
        │             • Business Purpose (blockquote)          │
        │             • What It Monitors                       │
        │             • Why It Matters (table)                 │
        │             • Interpreting Findings (table)          │
        │                                                      │
        │  SECTION 2: EXECUTIVE SUMMARY ◄─── Synthesis         │
        │             • Alert Identity (from Metadata)         │
        │             • Execution Context                      │
        │             • ALL Parameters                         │
        │             • Bottom Line (4 key numbers)            │
        │             • What Happened (1-2 sentences)          │
        │             • Top 3 Findings                         │
        │             • Immediate Actions                      │
        │                                                      │
        │  SECTION 3: KEY METRICS ◄──────── From Analysis      │
        │             • Financial Impact                       │
        │             • Volume Counts                          │
        │             • Pattern Breakdown                      │
        │                                                      │
        │  SECTION 4: CONCENTRATION ◄─────── From Analysis     │
        │             • By Organization                        │
        │             • By Entity                              │
        │             • Largest Transactions                   │
        │                                                      │
        │  SECTION 5: RISK ASSESSMENT ◄───── Classification    │
        │             • Focus Area + Reasoning                 │
        │             • Severity + Reasoning                   │
        │             • Risk Score Breakdown                   │
        │             • Fraud Indicator (explicit)             │
        │                                                      │
        │  SECTION 6: RECOMMENDED ACTIONS ◄─ Synthesis         │
        │             • Immediate (24-48h)                     │
        │             • Short-term (1-2 weeks)                 │
        │             • Process Improvements                   │
        │                                                      │
        │  SECTION 7: TECHNICAL DETAILS ◄─── Reference         │
        │             • Detection Logic                        │
        │             • Artifacts Analyzed                     │
        │             • JSON Output                            │
        │                                                      │
        └─────────────────────────────────────────────────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  OUTPUT: Analysis.md  │
                  │  docs/analysis/       │
                  └───────────────────────┘
```

---

## Step-by-Step Process

### Step 1: Read Explanation File

| Attribute | Value |
|-----------|-------|
| **Input** | `Explanation_*.pdf` |
| **Output** | Business Purpose blockquote |
| **Why** | Context before data - reader needs to understand what they're looking at |

### Step 2: Read Metadata File

| Attribute | Value |
|-----------|-------|
| **Input** | `Metadata_*.xlsx` (3 sheets: Basic, General, Parameters) |
| **Output** | Alert Identity, Execution Context, ALL Parameters |
| **Why** | Critical for understanding scope, filters, and source system |

### Step 3: Read Code File

| Attribute | Value |
|-----------|-------|
| **Input** | `Code_*.txt` (ABAP/SQL) |
| **Output** | Detection logic understanding, field mappings, manual flags |
| **Why** | Needed to interpret what the data means and identify red flags |

### Step 4: Analyze Summary Data

| Attribute | Value |
|-----------|-------|
| **Input** | `Summary_*.xlsx` (the actual findings) |
| **Output** | Currency-grouped totals, USD conversion, Financial impact (total, avg, max), Concentration analysis, Pattern breakdown, Top 5 largest transactions |
| **Why** | This is the actual quantitative analysis |

### Step 5: Classify Risk

| Attribute | Value |
|-----------|-------|
| **Inputs** | All previous analysis |
| **Output** | Focus Area, Severity, Risk Score (0-100), Fraud Indicator |
| **Why** | Classification drives recommended actions |

### Step 6: Generate Report

| Attribute | Value |
|-----------|-------|
| **Output** | `docs/analysis/{Module}_{AlertName}_Analysis.md` |
| **Format** | Follows `quantitative-alert.yaml` template exactly |

---

## Critical Rules Applied

| Rule | Why It Matters |
|------|----------------|
| **Business Context FIRST** | Reader needs orientation before numbers |
| **ALL parameters included** | Missing param = missing context |
| **Source system identified** | Multi-SAP clients need this |
| **Manual flag checked** | Manual + large loss = RED FLAG |
| **>50% concentration flagged** | High risk indicator |
| **Fraud indicator explicit** | Never leave ambiguous |
| **Multi-currency → USD** | Enables comparison across regions |

---

## Artifact-to-Section Mapping

```
┌─────────────────────┬────────────────────────────────────────────────────┐
│     ARTIFACT        │              FEEDS INTO SECTIONS                    │
├─────────────────────┼────────────────────────────────────────────────────┤
│                     │                                                     │
│  Explanation_*.pdf  │  ──►  Business Context                             │
│                     │       • Business Purpose (blockquote)               │
│                     │       • Why It Matters                              │
│                     │                                                     │
├─────────────────────┼────────────────────────────────────────────────────┤
│                     │                                                     │
│  Metadata_*.xlsx    │  ──►  Executive Summary                            │
│                     │       • Alert Identity                              │
│                     │       • Execution Context                           │
│                     │       • Alert Parameters (ALL of them)              │
│                     │                                                     │
├─────────────────────┼────────────────────────────────────────────────────┤
│                     │                                                     │
│  Code_*.txt         │  ──►  Business Context                             │
│                     │       • What It Monitors                            │
│                     │       • Interpreting Findings                       │
│                     │  ──►  Technical Details                            │
│                     │       • Detection Logic                             │
│                     │                                                     │
├─────────────────────┼────────────────────────────────────────────────────┤
│                     │                                                     │
│  Summary_*.xlsx     │  ──►  Executive Summary                            │
│                     │       • Bottom Line                                 │
│                     │       • What Happened                               │
│                     │       • Top 3 Findings                              │
│                     │  ──►  Key Metrics                                  │
│                     │       • Financial Impact                            │
│                     │       • Volume                                      │
│                     │       • Patterns                                    │
│                     │  ──►  Concentration Analysis                       │
│                     │       • By Organization                             │
│                     │       • By Entity                                   │
│                     │       • Largest Transactions                        │
│                     │                                                     │
├─────────────────────┼────────────────────────────────────────────────────┤
│                     │                                                     │
│  [SYNTHESIS]        │  ──►  Risk Assessment                              │
│  All artifacts      │       • Focus Area                                  │
│  combined           │       • Severity                                    │
│                     │       • Risk Score                                  │
│                     │       • Fraud Indicator                             │
│                     │  ──►  Recommended Actions                          │
│                     │       • Immediate                                   │
│                     │       • Short-term                                  │
│                     │       • Process Improvements                        │
│                     │                                                     │
└─────────────────────┴────────────────────────────────────────────────────┘
```

---

## Output Document Structure

The final analysis document follows this exact order:

```
1. BUSINESS CONTEXT          (half page max)
   ├── Business Purpose      (blockquote - from Explanation)
   ├── What It Monitors      (1-2 sentences - from Code)
   ├── Why It Matters        (table, max 3 rows)
   └── Interpreting Findings (table, max 3 rows)

2. EXECUTIVE SUMMARY         (all critical info visible without scrolling)
   ├── Alert Identity        (from Metadata Basic)
   ├── Execution Context     (from Metadata General)
   ├── Alert Parameters      (ALL - from Metadata Parameters)
   ├── The Bottom Line       (4 numbers: impact, records, severity, fraud)
   ├── What Happened         (1-2 sentences)
   ├── Top 3 Findings        (numbered list)
   └── Immediate Actions     (numbered list, 24-48h)

3. KEY METRICS
   ├── Financial Impact      (total, avg, max, currency)
   ├── Volume                (primary and secondary counts)
   └── Patterns              (breakdown with percentages)

4. CONCENTRATION ANALYSIS
   ├── By Organization       (flag >50%)
   ├── By Entity             (flag >50%)
   └── Largest Transactions  (top 5, check manual flags)

5. ANOMALY DEEP DIVE        (CONDITIONAL - only when significant pattern found)
   ├── Specific Entity Focus (e.g., Material HRC, Vendor 2011720)
   ├── Change Sequence       (temporal ordering with visual table)
   └── Pattern Analysis      (what the sequence reveals)

6. RISK ASSESSMENT
   ├── Focus Area            (with reasoning)
   ├── Severity              (with reasoning)
   ├── Risk Score            (0-100 with breakdown)
   ├── Fraud Indicator       (YES/NO/INVESTIGATE - explicit!)
   └── Risk Indicators Table

7. RECOMMENDED ACTIONS
   ├── Immediate (24-48h)    (max 3 with substeps)
   ├── Short-term (1-2 wks)  (max 3 with substeps)
   └── Process Improvements  (max 3, brief)

8. TECHNICAL DETAILS         (at bottom for deep-dive readers)
   ├── Detection Logic
   ├── Artifacts Analyzed
   └── Content Analyzer JSON Output
```

---

## Anomaly Deep Dive: When to Include

The **Anomaly Deep Dive** section is CONDITIONAL - include it only when the data reveals a significant pattern that warrants focused analysis.

### Include When:

| Trigger | Example |
|---------|---------|
| **Oscillating values** | Material price going up/down/up within hours |
| **Repetitive changes** | Same vendor bank account changed 4+ times |
| **Suspicious sequence** | Create → Delete → Create within minutes |
| **Single entity dominates** | One material/vendor accounts for majority of anomalies |
| **Pattern tells a story** | Temporal ordering reveals deliberate manipulation |

### Do NOT Include When:

| Scenario | Reason |
|----------|--------|
| All records are similar | No standout entity to focus on |
| Changes are distributed evenly | No concentration to deep dive |
| Simple threshold breach | Alert caught what it was designed to catch, nothing unusual |
| No temporal pattern | Sorting by time doesn't reveal anything new |

### Key Principle:

> **The Anomaly Deep Dive transforms data rows into a NARRATIVE.**
>
> If sorting by time, grouping by entity, or sequencing changes doesn't reveal
> something that wasn't obvious from aggregate statistics - skip the section.
>
> When it DOES reveal something (like HRC's oscillating prices or Vendor 2011720's
> 6-minute fraud probe), it becomes the most valuable part of the report.

---

## Pattern Recognition Catalog

Patterns discovered during analysis that indicate specific issues. When you see these patterns, investigate accordingly.

### Data Quality Patterns

| Pattern | Example | Root Cause | Action |
|---------|---------|------------|--------|
| **999.99% Cap Hit** | 14,273 records at max % | True variance exceeds system limit | Investigate actual % - often 10,000%+ indicates data corruption |
| **1000x Price Jump** | Price: 1,500 → 1,350,000 | Price Unit (PEINH) configuration error | Check if PEINH changed from per-1000 to per-1 |
| **Book Qty = 0, Physical > 0** | "Ghost Inventory" | Unrecorded goods receipts, prior write-offs, or consignment | Trace receipt history, verify consignment agreements |
| **Mirror Variances** | +4,416 and -4,416 same material | Stock moved but not updated in system | Audit storage location transfers |

### Fraud Indicator Patterns

| Pattern | Example | Risk Level | Investigation |
|---------|---------|------------|---------------|
| **Repetitive Changes** | Same vendor bank account changed 4x in 6 minutes | CRITICAL | Immediate freeze, forensic review |
| **Same Account Multiple Vendors** | Account 62349726747 used for 4 different vendors | CRITICAL | Verify account ownership, freeze payments |
| **Create → Delete Same Day** | Bank account created then deleted within hours | HIGH | Recover deleted data, interview users |
| **User Concentration >60%** | PMBURU: 69% of all changes | HIGH | SoD review, audit authorization |
| **Credit Memo to One-Time Customer** | 167M TZS credit to "One time customer" | CRITICAL | Verify authorization, supporting docs, original invoice |

### Process Gap Patterns

| Pattern | Example | Indicates | Improvement |
|---------|---------|-----------|-------------|
| **All Records Same Day** | 82% of vendors changed same day | Batch operation or rapid probing | Add velocity controls |
| **Oscillating Values** | Price up/down/up within hours | Posting errors or deliberate manipulation | Implement approval workflow |
| **Zero-Value Transactions** | Large qty change, $0 value | Pricing issue or cost not yet rolled | Review material pricing |

### Module-Specific Patterns

#### MM (Materials Management)
- **Standard vs Moving Average confusion** - VPRSV indicator mismatch
- **Price Unit errors** - PEINH changing without price adjustment
- **Valuation Area inconsistency** - Same material, different behavior per plant

#### MD (Master Data)
- **Vendor bank churning** - Multiple changes to same vendor
- **Country hopping** - Bank accounts across different countries for same vendor
- **Timing clusters** - Multiple changes within minutes = red flag

#### FI (Finance)
- **GL account concentration** - >80% of exceptions in single account
- **Period-end spikes** - Unusual activity at month/year end
- **Manual entry flags** - High manual + high value = investigate

#### SD (Sales & Distribution)
- **Credit memo to OTC customer** - Credits to one-time/unnamed customers = fraud risk
- **Sales org concentration** - >80% of value in single org warrants review
- **Document category mismatch** - Credit memo (VBTYP=O) without valid original invoice
- **Payment term override** - Document terms differ from customer master = unauthorized credit extension
- **Cash to credit conversion** - Changing from C100 (cash) to credit terms = CRITICAL fraud risk
- **User concentration on overrides** - Single user >50% of payment term changes = investigation required

---

## Related Files

| File | Purpose |
|------|---------|
| `docs/th-context/analysis-rules/ALERT_CLASSIFICATION_PRINCIPLES.md` | **Core principle: severity is context-dependent, not type-dependent** |
| `docs/th-context/analysis-rules/templates/quantitative-alert.yaml` | Template definition |
| `.claude/rules/quantitative-alert-analysis.md` | Enforcement rules |
| `docs/th-context/skywind-4c-knowledge.md` | Skywind 4C knowledge base |
| `docs/analysis/` | Example analysis documents (9 completed) |

---

## Important Note

> **Quantitative alerts are processed first because they are easier to interpret - NOT because they are more important.**
>
> Severity is determined by **context and content**, not by whether an alert produces numbers or events.
> A qualitative cyber breach alert can be far more critical than a quantitative variance report.
>
> See `ALERT_CLASSIFICATION_PRINCIPLES.md` for full guidance.

---

## Data Segmentation: Context-Specific Keys

### The Plant Manager Principle

> **"The plant manager in Singapore doesn't care about price changes in USA."**
>
> Data must be segmented by the appropriate organizational key so that
> findings are **ACTIONABLE by the responsible person**.

### Why This Matters

A report showing "Material HRC had 10 price changes" is useless if those changes span 3 different plants across 2 countries. The plant manager needs to know:
- How many changes affected **MY plant**?
- What's the financial impact **in MY valuation area**?
- Which changes require **MY action**?

### Common Segmentation Keys by Module

| Module | Primary Key | Field | Why |
|--------|-------------|-------|-----|
| **MM** | Valuation Area | `BWKEY` | Material prices are plant/valuation-area specific |
| **SD** | Sales Organization | `VKORG` | Pricing, customers, and revenue are sales-org specific |
| **FI** | Company Code | `BUKRS` | Financial data is legal entity specific |
| **PUR** | Purchasing Organization | `EKORG` | Procurement is org-specific |
| **MD** | Company Code / Country | `BUKRS` / `BANKS` | Vendor data often needs country-level view |

### When to Apply Segmentation

| Scenario | Action |
|----------|--------|
| Alert spans multiple organizational units | **Segment first**, then analyze each unit separately |
| Single organizational unit | No segmentation needed |
| Cross-unit patterns are the concern | Show both: aggregated AND by unit |

### Example: Right vs Wrong Approach

**WRONG (aggregated only):**
```
Material HRC: 10 price changes, $6.2M impact
```
*Problem: Who is responsible? Which plant? Whose budget?*

**RIGHT (segmented by BWKEY):**
```
Material HRC by Valuation Area:
├── MA01 (Mabati, Kenya): 8 changes, $75K impact, oscillating pattern
├── MR99 (Mabati, Kenya): 2 changes, $5.38M impact, 999% spike
└── DA01 (ALAF, Tanzania): 0 changes for HRC
```
*Now: MA01 plant manager investigates posting errors, MR99 plant manager investigates data corruption*

### Implementation in Analysis

1. **Identify the segmentation key** from Metadata (check `BWKEY`, `BUKRS`, `VKORG`, etc.)
2. **Group data by that key first** before calculating metrics
3. **Report metrics per segment** in Concentration Analysis
4. **Identify anomalies per segment** - same material may be fine in one plant, problematic in another
5. **Recommend actions per responsible party** - "MA01 plant manager should..." not "Someone should..."

---

*This workflow document defines how Claude processes Skywind 4C alert artifacts to produce quantitative analysis reports.*
