# Alert Classification Principles

> **Version:** 1.0 | **Last Updated:** November 2025

## Core Principle: Severity is Context-Dependent

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   QUANTITATIVE ≠ MORE IMPORTANT                                            │
│   QUALITATIVE  ≠ LESS IMPORTANT                                            │
│                                                                             │
│   Severity is determined by CONTEXT and CONTENT, not by alert TYPE         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quantitative vs Qualitative Alerts

### Quantitative Alerts

| Characteristic | Description |
|----------------|-------------|
| **Output Type** | Measurable numbers: amounts, counts, percentages, variances |
| **Why Processed First** | Easier to interpret, clear metrics, straightforward analysis |
| **Analysis Approach** | Statistical, aggregation, concentration analysis, trends |
| **Examples** | Financial losses, purchase volume changes, inventory counts |

### Qualitative Alerts

| Characteristic | Description |
|----------------|-------------|
| **Output Type** | Events, patterns, status changes, access logs, configurations |
| **Why Different** | Requires contextual interpretation, pattern recognition |
| **Analysis Approach** | Event correlation, timeline analysis, anomaly detection |
| **Examples** | Fraud indicators, cyber events, SoD violations, access patterns |

---

## Severity Determination

### The Rule

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   Alert criticality is determined by:                                       │
│                                                                             │
│   1. WHAT happened (the event/finding itself)                              │
│   2. WHO is involved (user, vendor, customer)                              │
│   3. HOW MUCH is at stake (financial, reputational, operational)           │
│   4. WHEN it occurred (timing, frequency, pattern)                         │
│   5. WHERE in the process (controls, approvals, payments)                  │
│                                                                             │
│   NOT by whether it produces numbers or events                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Severity Scale (Applies to BOTH Types)

| Severity | Criteria | Examples |
|----------|----------|----------|
| **CRITICAL** | Immediate business impact, active fraud/breach, regulatory violation | Cyber breach detected, payment redirected to fraudulent account |
| **HIGH** | Significant risk, requires urgent action, potential for major loss | Vendor bank changes by single user, large unauthorized transactions |
| **MEDIUM** | Notable finding, requires review within days, control weakness | Unusual volume patterns, minor SoD conflicts |
| **LOW** | Informational, process improvement opportunity, minor anomaly | Data quality issues, configuration recommendations |

---

## Examples: Same Severity, Different Types

### CRITICAL Severity

| Alert Type | Example |
|------------|---------|
| **Quantitative** | $5M payment to vendor with recently changed bank account |
| **Qualitative** | Privileged user accessed production system at 3 AM from foreign IP |

### HIGH Severity

| Alert Type | Example |
|------------|---------|
| **Quantitative** | 66% of vendor bank changes made by single user |
| **Qualitative** | Same user created vendor AND processed payment (SoD violation) |

### MEDIUM Severity

| Alert Type | Example |
|------------|---------|
| **Quantitative** | 15% variance in monthly purchase volume |
| **Qualitative** | User password unchanged for 180+ days |

---

## LLM Decision-Making Guidance

When selecting which alert to analyze:

1. **Quantitative alerts first** - Not because more important, but because easier to interpret and validate analysis approach

2. **Module coverage** - Ensure analysis spans different modules (SD, FI, MM, MD, PUR, etc.)

3. **Risk indicators in name** - Prioritize alerts with fraud/security-related terminology:
   - "Modified" + sensitive data = high priority
   - "Unauthorized" = high priority
   - "Bank Account" = high priority
   - "Access" + unusual pattern = high priority

4. **Context always wins** - A low-volume qualitative alert about a cyber breach is more critical than a high-volume quantitative alert about minor variances

---

## Data Quality vs Fraud Distinction

Not all CRITICAL findings indicate fraud. Some indicate **data quality or configuration issues** that are equally urgent but require different responses.

### Decision Matrix

| Indicator | Data Quality Issue | Fraud Indicator |
|-----------|-------------------|-----------------|
| **Pattern** | Systematic across many records | Concentrated on specific entities |
| **User behavior** | Automated/batch operations | Manual, after-hours, rapid changes |
| **Values** | 1000x jumps (price unit error) | Gradual changes to avoid detection |
| **Timing** | During cost roll/period-end | Random or clustered outside business hours |
| **Reversibility** | Can be corrected with adjustment | May require legal/forensic action |

### Example: Standard Price Change Alert

| Metric | Finding | Classification |
|--------|---------|----------------|
| 45K records | 31.7% hit 999.99% cap | **Data Quality** - systemic issue |
| $116.8M impact | 94 records from DA01 | **Configuration Error** - not fraud |
| Prices 1000x higher | PEINH mismatch | **Technical Root Cause** identified |

**Severity:** CRITICAL (because financial statements are misstated)
**Primary Concern:** DATA QUALITY / CONFIGURATION ERROR (not fraud)

### Response Differences

| Issue Type | Immediate Response | Long-term Fix |
|------------|-------------------|---------------|
| **Data Quality** | Halt posting, identify scope, correct data | Fix configuration, add validation |
| **Fraud** | Freeze accounts, preserve evidence, involve legal | Prosecute, improve controls |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `QUANTITATIVE_ALERT_WORKFLOW.md` | Processing workflow for measurable alerts |
| `quantitative-alert.yaml` | Template for quantitative analysis reports |
| `quantitative-alert-analysis.md` | Enforcement rules for quantitative analysis |
| *(Future)* `QUALITATIVE_ALERT_WORKFLOW.md` | Processing workflow for event-based alerts |

---

*This document establishes foundational principles for alert classification and severity determination.*
