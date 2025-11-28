# Skywind 4C Knowledge Base

> **Purpose:** Consolidated reference document for AI agents working with Skywind 4C alerts in the Treasure Hunt Analyzer. Read this once at session start to understand the domain.

---

## 1. Skywind Platform Overview

**SkyAPS (Skywind Analytical Platform for SAP)** is a cloud-based SaaS platform that provides:
- **4C** - Real-time alerting and monitoring for SAP systems
- **SoDA** - Segregation of Duties Analysis
- **JAM** - Job and Application Monitoring

**4C Key Capabilities:**
- Fraud Detection (Procurement, Finance, Sales, Controlling)
- Business Process Monitoring (SD/MM/HCM/FI/CO/PM/QM)
- Infrastructure Monitoring (BASIS/DB/Communications)
- Application Monitoring (BW/Security/User Management)

**Delivery:** Alerts sent via email or SMS based on scheduling.

---

## 2. Core Terminology

### Exception Indicator (EI)
An **ABAP Function Module** built to trace and catch specific events in SAP systems. Each EI has:
- A **structure** with fields that can be output and/or used as parameters
- **Built-in restrictions** that cannot be changed by users

Think of it as: **The detection logic/code**

### Alert Instance (AI)
A **parameterized Exception Indicator** configured with:
- Specific parameter values (restrictions)
- Recipients (email/SMS)
- Output fields
- Scheduling plan

Think of it as: **A configured alert ready to run**

### Alert Template
A **pre-configured Alert Instance** (out-of-the-box). Part of Skywind's Business Content. Can be copied and customized by users.

Think of it as: **A starter template**

### Alert Notification
The **message generated** when an alert runs and finds matching events. Sent to recipients via email or SMS.

### Relationship:
```
Exception Indicator (EI) → parameterized → Alert Instance (AI)
                                              ↓
                                      Alert Notification
```

**Key Point:** Multiple Alert Instances can be built from a single Exception Indicator.

---

## 3. Alert Parameters

### Date and Time Parameters

These are **external parameters** (not from SAP tables) used to define time windows for monitoring.

#### BACKDAYS
**Definition:** How far back in time the alert looks to fetch data.

| Value | Meaning |
|-------|---------|
| BACKDAYS = 0 | Today only |
| BACKDAYS = 1 | Today + yesterday |
| BACKDAYS = 7 | Today + previous 7 days |
| BACKDAYS = 365 | Today + previous 365 days |

**CRITICAL:** BACKDAYS is just a filter parameter. It is NOT:
- A divisor for normalizing counts
- An indicator of "frequency" or "rate"
- Something to divide by when calculating risk

It simply defines the **time window** for the data query.

#### FORWDAYS
Similar to BACKDAYS but for **future events** (e.g., employee retirement dates, upcoming deadlines).

#### DATE_REF_FLD
The **date field** used by BACKDAYS for filtering. Examples:
- AUDAT (Document Date)
- ERDAT (Creation Date)
- Custom Z* fields

#### DURATION
Used to monitor **time intervals** (e.g., processing time, job runtime).
- Works with DURATION_UNIT
- Answers: "How much time has passed since event X?"

#### DURATION_UNIT
| Value | Meaning |
|-------|---------|
| D | Days |
| H | Hours |
| M | Minutes |
| F | Full Days (specific day in past, not range) |

### Example Parameter Combinations

**Fetch records for last 24 hours:**
```
BACKDAYS = 1 (today + yesterday)
DURATION <= 24
DURATION_UNIT = H
```

**Fetch records for same day last week only:**
```
BACKDAYS = 7
DURATION = 7
DURATION_UNIT = F (Full Days - specific day, not range)
```

**Fetch long-running jobs (>3 hours today):**
```
BACKDAYS = 0
DURATION > 3
DURATION_UNIT = H
```

---

## 4. Alert Artifact Structure

Each 4C alert typically produces 4 artifact files:

| Artifact | Prefix | Content | Purpose |
|----------|--------|---------|---------|
| **Code** | `Code_` | ABAP Function Module source | Understanding detection logic |
| **Explanation** | `Explanation_` | Business context (.docx) | WHY this alert matters |
| **Metadata** | `Metadata_` | Alert parameters (.xlsx) | Configuration: BACKDAYS, filters, etc. |
| **Summary** | `Summary_` | Output data (.csv/.xlsx) | THE ACTUAL DATA TO ANALYZE |

### Analysis Order
1. **Metadata** - Understand parameters (BACKDAYS, filters)
2. **Code** - Understand detection logic
3. **Explanation** - Understand business context
4. **Summary** - Analyze the actual findings (PRIMARY DATA SOURCE)

### Metadata Excel Structure
Typically contains sheets:
- **Metadata general** - Source system, status, created/updated dates
- **Metadata basic** - Alert Instance ID, name, category, subcategory
- **Alert Parameters** - BACKDAYS, filters, conditions
- **Excep. Ind. Parameters** - Exception Indicator built-in restrictions

---

## 5. Alert Categories

### By SAP Module

| Module | Description | Common Alert Types |
|--------|-------------|-------------------|
| **SD** | Sales & Distribution | Negative profit deals, pricing anomalies |
| **MM** | Materials Management | Vendor manipulation, procurement fraud |
| **FI** | Finance | GL anomalies, payment irregularities |
| **CO** | Controlling | Cost center issues |
| **HCM** | Human Capital Management | Payroll anomalies |
| **PM** | Plant Maintenance | Work order issues |
| **QM** | Quality Management | Quality failures |
| **BASIS** | System Administration | Technical issues, dumps |
| **BW** | Business Warehouse | Report/data issues |

### By Business Domain (4C Categories)

| Category | Subcategories |
|----------|---------------|
| **Fraud Detection** | Procurement, Finance, Sales, Controlling |
| **Business Processes** | SD, MM, HCM, FI, CO, PM, QM alerts |
| **Infrastructure** | BASIS, DB, Communications |
| **Applications** | BW, Security, User Management |

---

## 6. SoDA (Segregation of Duties Analysis)

SoDA is Skywind's module for analyzing access control and SoD violations.

### Key Concepts

| Term | Definition |
|------|------------|
| **SoD Rule** | A rule defining conflicting transaction combinations |
| **T-Group** | Transaction Group - logical grouping of related transactions |
| **Actual Violation** | User actually executed conflicting transactions |
| **Potential Violation** | User has authorization but hasn't executed |
| **Cross Reference Violation** | Violation between different roles |
| **Internal Violation** | Violation within same role |

### SoDA Reports
- Potential SOD Violations (by SoD Rules)
- Actual SOD Violations (by SoD Rules)
- Potential SOD Violations (by T-Groups)
- Actual SOD Violations (by T-Groups)
- Internal Violations
- Cross Reference Violations
- Excessive Authorizations

---

## 7. Alert Generator (AG)

A **no-code tool** for creating custom Exception Indicators from SAP data sources.

### Supported Sources
- ABAP Repository Tables (KNA1, MARA, Z* tables)
- ABAP Views (including HANA Calculation Views)
- ABAP CDS Views
- ABAP Function Modules (if compliant with 4C API)
- Files (CSV, XLS) - in development
- ALV Reports

### EI Creation Steps
1. Basic Settings (source system, language, source entity)
2. Select output fields
3. Select parameter fields (restrictions)
4. Currency conversion (if needed)
5. Define special parameters (BACKDAYS, etc.)
6. Define key fields for Delta reporting
7. Define conditions (field comparisons)
8. Add documentation

---

## 8. Common SAP Fields Reference

### Sales (SD) - VBAK/VBAP Tables
| Field | Table | Description |
|-------|-------|-------------|
| NETWR | VBAP | Net Value (what customer pays) |
| WAVWR | VBAP | Cost (what it cost to produce/buy) |
| MPROK | VBAP | Manual Price flag (A = manual change) |
| VKORG | VBAK | Sales Organization |
| KUNNR | VBAK | Customer Number |
| AUART | VBAK | Document Type |
| AUDAT | VBAK | Document Date |

### Vendors (LFA1/LFB1 Tables)
| Field | Description |
|-------|-------------|
| LIFNR | Vendor Number |
| NAME1 | Vendor Name |
| KTOKK | Account Group |
| SPERR | Blocked indicator |

### Customers (KNA1 Tables)
| Field | Description |
|-------|-------------|
| KUNNR | Customer Number |
| NAME1 | Customer Name |
| KTOKD | Account Group |

---

## 9. Analysis Guidelines for THA

### When Analyzing a 4C Alert:

1. **Check BACKDAYS first** (in Metadata)
   - Understand the time window
   - Don't normalize/divide by it

2. **Read the Code** to understand detection logic
   - What condition triggers the alert?
   - What fields are being compared?

3. **Read the Explanation** for business context
   - Why does this matter?
   - What are the risks?

4. **Analyze the Summary** (primary data)
   - This is the actual output
   - Extract counts, amounts, patterns
   - Identify concentrations (by org, customer, vendor)

### Key Questions to Answer:
- **What happened?** (qualitative)
- **How much/many?** (quantitative)
- **Where is it concentrated?** (by org, customer, etc.)
- **Are there outliers?** (single large transactions)
- **Is there a pattern?** (manual overrides, specific users)

---

## 10. Quick Reference

### Alert Instance ID Format
`{system_id}_{sequence}` - e.g., `200025_001441`

### Common Alert Name Patterns
- `Negative Profit Deal` - SD: selling below cost
- `Rarely Used Vendors` - MM: inactive vendor monitoring
- `Modified Vendor Bank Account` - FI: vendor master changes
- `Exceptional Posting by GL Account` - FI: GL anomalies
- `SOD GR-IR vs PO` - MM: segregation of duties

### File Naming Convention
```
{Prefix}_{Alert Name}_{Alert ID}.{ext}
```
Examples:
- `Code_Negative Profit Deal_200025_001441.txt`
- `Summary_Negative Profit Deal_200025_001441_USD_ONLY.csv`
- `Metadata_Negative Profit Deal_200025_001441.xlsx`
- `Explanation_Negative Profit Deal_200025_001441.docx`

---

## 11. Analysis Rules (Machine-Readable)

For structured, consistent analysis, refer to the YAML-based rules:

```
docs/th-context/analysis-rules/
├── templates/
│   ├── quantitative-alert.yaml    # Template for quantitative alerts
│   └── qualitative-alert.yaml     # Template for qualitative alerts (TBD)
├── presentation-rules.yaml        # How to present findings
└── field-mappings/
    ├── sd-fields.yaml             # SD module fields
    ├── fi-fields.yaml             # FI module fields (TBD)
    └── mm-fields.yaml             # MM module fields (TBD)
```

**Enforcement Rules:** `.claude/rules/quantitative-alert-analysis.md`

This rule file is automatically loaded by AI agents and enforces:
- Mandatory document structure (Executive Summary first)
- ALL parameters inclusion requirement
- Source system identification
- Manual override checking
- Fraud indicator explicit statement
- Concentration threshold flagging (>50%)

### When to Use Which Template

| Alert Type | Template | Characteristics |
|------------|----------|-----------------|
| **Quantitative** | `quantitative-alert.yaml` | Amounts, counts, percentages, aggregatable data |
| **Qualitative** | `qualitative-alert.yaml` | Descriptive, categorical, non-numeric patterns |

### Key Rules Summary

1. **Executive Summary First** - All critical info before scrolling
2. **Include ALL Parameters** - From Metadata file, even empty ones
3. **Source System Always** - Critical for multi-SAP clients
4. **Concentration = Risk** - Flag >50% in single entity
5. **Manual Override = Red Flag** - Always check MPROK or equivalent
6. **Fraud Indicator Explicit** - Always state YES/NO/INVESTIGATE

---

## Document Information

**Source:** Skywind Knowledge Portal (help.skywind.com)
**Created:** 2025-11-27
**Updated:** 2025-11-27
**Purpose:** AI agent reference for THA development

**Related Documents:**
- [CLAUDE.md](../../CLAUDE.md) - Project guide
- [llm_handover.md](../../llm_handover.md) - Current project state
- [analysis-rules/](analysis-rules/) - Structured analysis templates
- [docs/analysis/](../analysis/) - Completed alert analyses

---

*This document consolidates knowledge from `docs/about_skywind/TXT/` for efficient AI agent onboarding.*
