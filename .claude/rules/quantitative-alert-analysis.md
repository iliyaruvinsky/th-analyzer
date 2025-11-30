# Quantitative Alert Analysis Rules

> **Mandatory rules for analyzing Skywind 4C alerts with measurable data**

---

## ⛔ CRITICAL - NO DEVIATION FROM TEMPLATE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   BEFORE EVERY ANALYSIS REPORT:                                             │
│                                                                             │
│   1. READ templates/quantitative-alert.yaml FIRST                           │
│   2. FOLLOW the structure EXACTLY as defined                                │
│   3. DO NOT rename sections (e.g., "Alert Purpose" instead of "Business     │
│      Context" is FORBIDDEN)                                                 │
│   4. DO NOT omit required subsections                                       │
│   5. DO NOT add creative variations to the format                           │
│                                                                             │
│   CLIENT REPORTS MUST BE 100% CONSISTENT                                    │
│   EVERY REPORT MUST LOOK IDENTICAL IN STRUCTURE                             │
│                                                                             │
│   VIOLATION = REJECTED REPORT                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**This rule exists because:** The client cannot receive reports in different formats. Consistency is mandatory for professional delivery and automated processing.

---

## When This Applies

Use these rules when analyzing alerts that produce:
- Financial amounts (losses, gains, exposures)
- Counts (records, transactions, users, vendors)
- Percentages and ratios
- Variance data (YoY, MoM comparisons)

## Template Reference

**Always follow:** `docs/th-context/analysis-rules/templates/quantitative-alert.yaml`

## Mandatory Document Structure

### 0. KEY FINDINGS (Must Be First)

**Principle:** Key findings upfront - scannable at a glance.

Three subsections in order:

1. **Metrics Table** - 4-row table with clean format:
   - Records (with context, e.g., "1,274 billing documents")
   - Period (dates and duration)
   - Total Value (with currency)
   - Severity (CRITICAL/HIGH/MEDIUM/LOW)

2. **Critical Discovery** - The single most important finding:
   - Bold heading with entity name + amount
   - Use bullet points (•) not dashes
   - 3 bullets explaining why it matters

3. **Concentration Pattern** - Single table with closing note:
   - One table showing main concentration
   - No Risk column - keep it clean
   - Bold only the critical percentage
   - Add closing observation as plain text after table

**Format:** Clean, minimal bold, scannable. Half page max.

### 1. BUSINESS CONTEXT (After Key Findings)

**Principle:** Reader needs detailed context AFTER seeing the key findings.

Four subsections:
1. **Business Purpose** (blockquote) - 2-3 sentences explaining what business risk this alert detects. Source: Explanation_* file
2. **What This Alert Monitors** - 1-2 sentences describing the monitoring logic
3. **Why It Matters** - Table with Risk Type | Business Impact (max 3 rows)
4. **Interpreting the Findings** - Table with Pattern | Legitimate Cause | Red Flag (max 3 rows)

**Keep Short:** Half page max.

### 2. EXECUTIVE SUMMARY (After Business Context)

The Executive Summary MUST contain ALL of the following in this order:

| Section | Content | Source |
|---------|---------|--------|
| **Alert Identity** | Name, ID, Module, Category, Subcategory | Metadata Basic sheet |
| **Execution Context** | Source System, Created Date, Last Executed, EI ID | Metadata General sheet |
| **Alert Parameters** | ALL parameters (including empty ones shown as "none") | Alert Parameters sheet |
| **The Bottom Line** | Total impact, Records affected, Severity, Fraud indicator | Calculated from Summary |
| **What Happened** | 1-2 sentence plain language summary | Synthesis |
| **Top 3 Findings** | Largest transaction, Highest concentration, Pattern anomaly | Summary data |
| **Immediate Actions** | 3 specific actions for next 24-48 hours | Analysis |

**Principle:** Reader must understand everything critical WITHOUT scrolling past Executive Summary.

### 3. KEY METRICS

- Financial Impact (total, average, maximum, currency)
- Volume (counts by dimension)
- Patterns (breakdown with percentages)

### 4. CONCENTRATION ANALYSIS

- By Organization (company code, sales org, plant)
- By Entity (customer, vendor, user)
- Largest Single Transactions (top 5)

**Rule:** Flag any entity with >50% concentration.

### 5. RISK ASSESSMENT

Required classifications:
- **Focus Area:** BUSINESS_CONTROL | BUSINESS_PROTECTION | ACCESS_GOVERNANCE | TECHNICAL_CONTROL | JOBS_CONTROL | S4HANA_EXCELLENCE
- **Severity:** CRITICAL | HIGH | MEDIUM | LOW
- **Risk Score:** 0-100
- **Fraud Indicator:** YES | NO | INVESTIGATE (MUST be explicit)

### 6. RECOMMENDED ACTIONS

Three tiers:
- **Immediate (24-48 hours)** - Max 3 items with substeps
- **Short-term (1-2 weeks)** - Max 3 items with substeps
- **Process Improvements** - Max 3 items, brief

### 7. TECHNICAL DETAILS (Last)

- Detection Logic (ABAP/SQL explanation)
- Artifacts Analyzed (file list)
- Content Analyzer Output (JSON for programmatic use)

---

## Critical Rules - DO NOT VIOLATE

### Parameters
- **Include ALL parameters** from Metadata file
- Show empty parameters as "(none)" - do not omit them
- BACKDAYS is a filter, NOT a divisor for normalization

### Source System
- **Always identify the source system** (PS4, ECC, etc.)
- Critical for clients with multiple SAP instances

### Manual Override Check
- **Always check for manual override flags** (MPROK='A' or equivalent)
- Manual override + large loss = RED FLAG
- Note in concentration tables whether entries are manual

### Fraud Indicator
- **Must explicitly state** YES, NO, or INVESTIGATE
- Never leave ambiguous

### Concentration Threshold
- **>50% in single entity = flag it**
- Bold the entity, add insight note

### Multi-Currency Handling
- **Group data by currency first** - analyze each currency separately
- **Convert ALL non-USD values to USD** for consolidated totals
- **Use current exchange rates** - search for rates if not provided
- **Show BOTH local currency AND USD** in tables where applicable
- **Document exchange rates used** - include in Technical Details section

**Currency Conversion Process:**
1. Identify all unique currencies in the Summary data
2. Look up current exchange rates (per 1 USD)
3. Calculate: `USD_Value = Local_Value / Exchange_Rate`
4. Present: Local totals by currency + Grand total in USD

**Required Exchange Rate Sources:**
- Web search for current rates if not in source data
- Document rate date (e.g., "November 2025 rates")
- Include rate table in analysis document

---

## Formatting Standards

### Numbers
- Currency: `$14,152,997` (comma separators, $ prefix)
- Large amounts in text: `$14.15M` (K/M suffix)
- Percentages: `81%` or `81.2%`
- Counts: `2,044` (comma separators)

### Tables
- Use markdown tables
- Bold key figures
- Right-align numbers

### Emphasis
- **Bold** for critical findings
- **UPPERCASE** for warnings
- Start actions with verbs (Investigate, Review, Audit)

---

## Quality Checklist

Before finalizing any quantitative alert analysis:

- [ ] Key Findings is FIRST (right after template header)?
- [ ] Key Findings has all 3 subsections (Metrics, Critical Discovery, Concentration Pattern)?
- [ ] Key Findings is clean and scannable (half page max)?
- [ ] Business Context is SECOND (after Key Findings)?
- [ ] Business Purpose blockquote derived from Explanation_* file?
- [ ] Executive Summary contains ALL 7 required sections?
- [ ] ALL parameters from Metadata included (even empty ones)?
- [ ] Source system clearly identified?
- [ ] Business Context section is concise (half page max)?
- [ ] Concentrations >50% are highlighted?
- [ ] Manual override flag checked for all top losses?
- [ ] Fraud indicator explicitly stated (YES/NO/INVESTIGATE)?
- [ ] Actions are specific and actionable (start with verb)?
- [ ] JSON output included for programmatic use?
- [ ] Multi-currency data grouped by currency?
- [ ] Exchange rates documented and conversion to USD shown?

---

## File References

- **Template:** `docs/th-context/analysis-rules/templates/quantitative-alert.yaml`
- **Skywind Knowledge:** `docs/th-context/skywind-4c-knowledge.md`
- **Field Mappings:** `docs/th-context/analysis-rules/field-mappings/`
- **Example Analyses:** `docs/analysis/`

---

*Version: 1.0 | Created: 2025-11-27*
