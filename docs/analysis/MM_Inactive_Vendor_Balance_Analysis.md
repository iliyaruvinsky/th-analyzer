# Inactive Vendor with Balance >$10K Analysis

> **Alert ID:** 200025_001452 | **Module:** MM | **Analysis Date:** November 2025

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 13 inactive vendors |
| Period | 720 days inactivity (BACKDAYS) |
| Total Balance | ~$1.86 million USD |
| Severity | HIGH |

## Critical Discovery

**ICE MAKE REFRIGERATION LIMITED - $932K Across Multiple Orgs:**
• Single vendor appearing in 4 purchasing orgs with $231K-$234K balance each
• No financial activity for 720+ days despite significant outstanding balance
• Represents 50% of total inactive vendor exposure

## Concentration Pattern

| Company Code | Vendors | Balance |
|--------------|---------|---------|
| TZ01 (ALAF Limited) | 20 | **$1.30M** |
| KE01 (Mabati Kenya) | 3 | $495K |
| KE03 (Mabati Kenya) | 1 | $65K |

TZ01 accounts for 70% of total inactive vendor balance - AP team review required.

---

## Business Context

> **Business Purpose:** Inactive vendors with high balances (>$10K) are vendor master records showing no financial activity but carrying significant unpaid amounts in accounts payable. This creates cash flow mismanagement risk, potential duplicate payments on reactivation, prevents accurate cash forecasting, indicates unresolved disputes or forgotten debts, and exposes the company to legal claims or statute of limitations issues on aged payables.

### What This Alert Monitors

Identifies vendors where:
- No financial activity for BACKDAYS period (720 days = ~2 years)
- Outstanding balance exceeds threshold ($10K USD)
- Vendor not blocked (LFA1_SPERM, LFB1_SPERR, LFM1_SPERM all empty)
- Uses LFC1 (vendor totals) and LFC3 (special G/L balances) tables

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Cash Flow Misstatement** | Aged payables distort working capital metrics |
| **Duplicate Payment Risk** | Reactivating vendor may trigger duplicate payments |
| **Legal Exposure** | Statute of limitations on aged payables may expire |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| High balance, no activity | Dispute under resolution | Balance aging >2 years without review |
| Same vendor multiple orgs | Multi-org relationship | Inconsistent balances across orgs |
| ZNRP account group | Standard vendor type | No recent master data updates |

---

## Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| **Alert Instance Name** | Inactive Vendor with Balance >$10K |
| **Alert Instance ID** | 200025_001452 |
| **Module** | MM (Materials Management) |
| **Category** | Applications |
| **Subcategory** | MM Alerts |

### Execution Context

| Attribute | Value |
|-----------|-------|
| **Source System** | Production S4 (PS4) |
| **Exception Indicator ID** | SW_10_06_INACT_VEND |
| **Created On** | 05.11.2025 |
| **Collection Mode** | Full |
| **Execution Mode** | On event presence |

### Alert Parameters

| Parameter | Description | Value |
|-----------|-------------|-------|
| BACKDAYS | Days of inactivity | 720 |
| BALANCE_TOTAL_FR | Balance threshold | >10,000 USD |
| COUNTER | Number of active periods | 0 |
| LFM1_SPERM | Purchasing block | (none) |
| WAERS_FR | Currency for balance | USD |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Total Inactive Vendors** | **13** |
| **Total Balance** | **$1,858,004 USD** |
| **Largest Single Vendor** | $470,757 USD |
| **Severity** | **HIGH** |
| **Fraud Indicator** | **INVESTIGATE** |

### What Happened

**13 inactive vendors** with no financial activity for 720+ days are carrying **$1.86 million** in outstanding balances. Two vendors (VAG POLYTECH and ICE MAKE REFRIGERATION) account for 75% of the total exposure. All vendors are in the ZNRP account group and span 3 company codes (TZ01, KE01, KE03).

### Top 3 Findings

1. **ICE MAKE REFRIGERATION LIMITED (TZ01):** $932K balance across 4 purchasing organizations - same vendor, different org assignments, needs consolidation review.

2. **VAG POLYTECH PRIVATE LIMITED (KE01):** Single largest balance at $471K in MR03 purchasing org - 2+ years inactive with significant outstanding amount.

3. **Concentration in TZ01:** 70% of total exposure ($1.3M) concentrated in ALAF Limited Tanzania - requires dedicated AP review.

### Immediate Actions

1. **Contact ICE MAKE REFRIGERATION** - verify outstanding balance legitimacy and payment status (Owner: TZ01 AP Team)
2. **Review VAG POLYTECH relationship** - determine if vendor should be reactivated or balance written off (Owner: KE01 Procurement)
3. **Initiate TZ01 AP cleanup** - prioritize review of 10 inactive vendors with $1.3M exposure (Owner: Regional Finance)

---

## Key Metrics

### Financial Impact

| Metric | Value |
|--------|-------|
| **Total Balance** | $1,858,004 USD |
| **Average per Vendor** | ~$143K USD |
| **Largest Balance** | $470,757 USD (VAG POLYTECH) |
| **Top 2 Vendors** | 75% of total |

### Volume

| Metric | Count |
|--------|-------|
| **Unique Vendors** | 13 |
| **Vendor-Org Combinations** | 24 |
| **Company Codes** | 3 |
| **Purchasing Orgs** | 8 |

### Patterns

| Account Group | Vendors | % |
|---------------|---------|---|
| ZNRP | 13 | 100% |

---

## Concentration Analysis

### By Company Code

| Company Code | Company Name | Vendors | Balance | % of Total |
|--------------|--------------|---------|---------|------------|
| **TZ01** | ALAF Limited | 20 | **$1,298,188** | **70%** |
| KE01 | Mabati Rolling Mills | 3 | $494,908 | 27% |
| KE03 | Mabati Rolling Mills | 1 | $64,908 | 3% |

**Flag:** TZ01 has 70% of total exposure - requires focused AP review.

### By Vendor (Top 5)

| Rank | Vendor | Company | Balance | % of Total |
|------|--------|---------|---------|------------|
| 1 | **VAG POLYTECH PRIVATE LIMITED** | KE01 | **$470,757** | **25%** |
| 2 | **ICE MAKE REFRIGERATION LIMITED** | TZ01 | **$931,584** | **50%** |
| 3 | METAFLEX DOORS INDIA PVT LTD | KE03 | $64,908 | 3% |
| 4 | SAID SALUM MAJID | TZ01 | $67,819 | 4% |
| 5 | UHURU CONSOLIDATED LIMITED | TZ01 | $64,863 | 3% |

**Note:** ICE MAKE REFRIGERATION appears across multiple purchasing orgs (AL03, SB02, MR02, MR03) with similar balances.

### By Purchasing Organization

| Purch Org | Vendors | Balance | Avg/Vendor |
|-----------|---------|---------|------------|
| **MR03** | 3 | **$715,627** | **$238,542** |
| SB02 | 2 | $299,133 | $149,567 |
| AL03 | 3 | $268,842 | $89,614 |
| MR02 | 1 | $231,567 | $231,567 |
| AL01 | 6 | $149,022 | $24,837 |
| AL02 | 6 | $148,547 | $24,758 |

---

## Risk Assessment

### Classification

| Factor | Assessment | Reasoning |
|--------|------------|-----------|
| **Focus Area** | BUSINESS_CONTROL | Working capital and AP management |
| **Severity** | HIGH | $1.86M in aged payables |
| **Risk Score** | 65/100 | High balance, long inactivity, concentration |
| **Fraud Indicator** | **INVESTIGATE** | Verify balances are legitimate, not fictitious |

### Risk Indicators

| Risk Type | Evidence | Recommended Action |
|-----------|----------|-------------------|
| **Stale Payables** | 720+ days inactivity | Confirm vendor status and balance validity |
| **Concentration Risk** | 2 vendors = 75% of balance | Prioritize top 2 vendors for review |
| **Duplicate Risk** | Same vendor in multiple orgs | Consolidate vendor master data |

---

## Recommended Actions

### Immediate (24-48 hours)

1. **Freeze payments to inactive vendors**
   - Add payment block to all 13 vendors pending review
   - Prevents accidental duplicate payments

2. **Contact top 2 vendors**
   - ICE MAKE REFRIGERATION: Verify $932K balance across 4 purchasing orgs
   - VAG POLYTECH: Confirm $471K balance and relationship status

3. **Export full vendor list for AP review**
   - Include balance breakdown by purchasing org
   - Flag vendors with >$100K balance

### Short-term (1-2 weeks)

1. **Vendor master data cleanup**
   - Review multi-org vendor assignments
   - Consolidate ICE MAKE REFRIGERATION entries
   - Update vendor status (reactivate or mark for write-off)

2. **AP reconciliation**
   - Match balances to original invoices
   - Identify any disputed amounts
   - Document resolution for each vendor

3. **Aging analysis**
   - Determine actual aging beyond 720 days
   - Assess statute of limitations exposure
   - Flag balances for potential write-off

### Process Improvements

1. **Periodic inactive vendor review:** Implement quarterly review of vendors with >$10K balance and >180 days inactivity
2. **Automatic payment block:** Block payments to vendors inactive >365 days without manual override
3. **Multi-org vendor monitoring:** Alert when same vendor appears in multiple purchasing orgs with significant balances

---

## Technical Details

### Source Tables

| Table | Description |
|-------|-------------|
| LFA1 | Vendor General Data |
| LFB1 | Vendor Company Code Data |
| LFM1 | Vendor Purchasing Organization Data |
| LFC1 | Vendor Master (Transaction Figures) |
| LFC3 | Vendor Master (Special G/L Transaction Figures) |
| T001 | Company Codes |
| T024E | Purchasing Organizations |

### Key Fields

| Field | Description | Usage |
|-------|-------------|-------|
| LIFNR | Vendor Number | Vendor identification |
| BUKRS | Company Code | Company segmentation |
| EKORG | Purchasing Organization | Procurement segmentation |
| BALANCE_TOTAL_FR | Total Balance (USD) | Financial threshold |
| KTOKK | Account Group | Vendor classification |

### Detection Logic Summary

```abap
SELECT LFB1~LIFNR LFB1~BUKRS...
  FROM LFB1 INNER JOIN LFA1 ON LFB1~LIFNR = LFA1~LIFNR
            INNER JOIN T001 ON LFB1~BUKRS = T001~BUKRS
            LEFT OUTER JOIN LFM1 ON LFA1~LIFNR = LFM1~LIFNR
  WHERE LFB1~SPERR = ''      -- Not posting blocked
    AND LFB1~LOEVM = ''      -- Not deletion flagged
    AND LFA1~SPERM = ''      -- Not purchasing blocked
    AND LFA1~LOEVM = ''      -- Not centrally deleted
-- Then checks LFC1/LFC3 for balance > $10K with no activity in BACKDAYS period
```

### Artifacts Analyzed

| File | Purpose |
|------|---------|
| Explanation_*.docx | Business context |
| Metadata_*.xlsx | Alert configuration |
| Summary_*.xlsx | Transaction data (86 records, 13 unique vendors) |
| Code_*.txt | ABAP detection logic |

---

## Content Analyzer Output

```json
{
  "alert_id": "200025_001452",
  "alert_name": "Inactive Vendor with Balance >$10K",
  "module": "MM",
  "source_system": "PS4",
  "metrics": {
    "total_vendors": 13,
    "total_balance_usd": 1858004,
    "largest_vendor_balance": 470757,
    "company_codes": 3
  },
  "classification": {
    "focus_area": "BUSINESS_CONTROL",
    "severity": "HIGH",
    "risk_score": 65,
    "fraud_indicator": "INVESTIGATE"
  },
  "top_vendors": [
    {"name": "VAG POLYTECH PRIVATE LIMITED", "company": "KE01", "balance": 470757},
    {"name": "ICE MAKE REFRIGERATION LIMITED", "company": "TZ01", "balance": 931584}
  ],
  "immediate_actions": [
    "Freeze payments to inactive vendors",
    "Contact top 2 vendors to verify balances",
    "Export vendor list for AP review"
  ]
}
```

---

*Analysis generated following QUANTITATIVE_ALERT_WORKFLOW.md v1.2 and templates/quantitative-alert.yaml*
