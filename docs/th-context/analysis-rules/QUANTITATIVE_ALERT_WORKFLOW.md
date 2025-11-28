# Quantitative Alert Analysis Workflow

> **Version:** 1.0 | **Last Updated:** November 2025

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
│  4. Explanation_*.pdf    ─── Business purpose documentation                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

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

5. RISK ASSESSMENT
   ├── Focus Area            (with reasoning)
   ├── Severity              (with reasoning)
   ├── Risk Score            (0-100 with breakdown)
   ├── Fraud Indicator       (YES/NO/INVESTIGATE - explicit!)
   └── Risk Indicators Table

6. RECOMMENDED ACTIONS
   ├── Immediate (24-48h)    (max 3 with substeps)
   ├── Short-term (1-2 wks)  (max 3 with substeps)
   └── Process Improvements  (max 3, brief)

7. TECHNICAL DETAILS         (at bottom for deep-dive readers)
   ├── Detection Logic
   ├── Artifacts Analyzed
   └── Content Analyzer JSON Output
```

---

## Related Files

| File | Purpose |
|------|---------|
| `docs/th-context/analysis-rules/templates/quantitative-alert.yaml` | Template definition |
| `.claude/rules/quantitative-alert-analysis.md` | Enforcement rules |
| `docs/th-context/skywind-4c-knowledge.md` | Skywind 4C knowledge base |
| `docs/analysis/` | Example analysis documents |

---

*This workflow document defines how Claude processes Skywind 4C alert artifacts to produce quantitative analysis reports.*
