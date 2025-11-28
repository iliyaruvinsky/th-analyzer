# PREQ & PO Value Check - Alert Analysis

> **TEMPLATE: Quantitative Alert Analysis**

---

## BUSINESS CONTEXT

> **Business Purpose:** This alert compares Purchase Requisition values against corresponding Purchase Order values to identify unauthorized price changes during PO creation. It helps detect approval bypasses where PO values exceed approved PR thresholds, potential vendor collusion through deliberate PR understatement, and budget control violations. Significant PR-to-PO value increases without proper documentation may indicate procurement fraud.

### What This Alert Monitors

**PR to PO Value Integrity** - Compares Purchase Requisition values against corresponding Purchase Order values. Flags cases where PO values differ from approved PR values, indicating potential unauthorized price changes during PO creation.

### Why It Matters

| Risk Type | Business Impact |
|-----------|--------------------|
| **Approval Bypass** | PO values exceeding PR thresholds avoid proper authorization |
| **Vendor Collusion** | Deliberate PR understatement followed by inflated PO |
| **Budget Control** | Understated PRs bypass budget controls |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| Small increase (<5%) | Currency fluctuation, quantity adjustment | Pattern of consistent increases |
| Large increase (>100%) | Emergency procurement, scope change | No documented approval |
| PR value = 1 or 0 | Placeholder/dummy value | **Extreme increases without documentation** |

---

## EXECUTIVE SUMMARY

### Alert Identity

| | |
|---|---|
| **Alert Name** | PREQ & PO value check |
| **Alert ID** | 200025_001414 |
| **Module** | PUR (Purchasing / Materials Management) |
| **Category** | Applications |
| **Subcategory** | PUR Alerts |

### Execution Context

| | |
|---|---|
| **Source System** | Production S4 (PS4) |
| **Created** | 22.10.2025 at 11:59 by SKYWATCH |
| **Last Updated** | 27.11.2025 at 14:21 by ILIYAR |
| **Exception Indicator** | SW_10_03_PR_PO_VAL |

### Alert Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| BACKDAYS | 15 | Data from past 15 days |
| PO_PREQ_DIFF | Not equal to 0 | Flag any PR-to-PO value difference |

### THE BOTTOM LINE

| | |
|---|---|
| **Total PR Value (USD)** | **$35,118,406** |
| **Total PO Value (USD)** | **$7,794,955** |
| **Net Difference (USD)** | **-$27,323,451** (PO < PR overall) |
| **Records with PO > PR** | 993 records totaling **$2,115,529** potential overpricing |
| **Records Affected** | 1,307 line items |
| **Severity** | HIGH |
| **Fraud Indicator** | INVESTIGATE - Large value differences detected |

### WHAT HAPPENED

1,307 purchase requisitions show value differences when converted to purchase orders. While overall PO values are lower than PR values (-$27.3M), **993 records (76%) show PO values exceeding PR values** - totaling $2.1M in potential unauthorized price increases. Largest single overpricing: $335K to GLOBETECH ASIA.

### TOP 3 FINDINGS

1. **MR03 Purch Org - $827,638 total overpricing** across only 8 records - **INVESTIGATE IMMEDIATELY**
2. **GLOBETECH ASIA vendor**: $335,444 single transaction increase (PR: 1 ZAR → PO: 5.7M ZAR)
3. **Purchasing Group 1**: -$27.6M difference in 19 records - unusual concentration

### IMMEDIATE ACTIONS REQUIRED

1. **URGENT**: Investigate MR03 purchasing organization - average $103K overpricing per transaction
2. Review GLOBETECH ASIA vendor relationship - single PR of 1 ZAR became 5.7M ZAR PO
3. Audit PR 65977317 - multiple line items with significant value increases

---

## KEY METRICS

### Financial Impact (Converted to USD)

| Metric | Value |
|--------|-------|
| Total PR Value | $35,118,406 |
| Total PO Value | $7,794,955 |
| Net Difference | -$27,323,451 |
| Records with PO > PR | 993 (76%) |
| Total Overpricing | $2,115,529 |
| Max Single Overpricing | $335,444 |

### Volume

| Metric | Value |
|--------|-------|
| Total Records | 1,307 |
| Unique PRs | ~419 |
| Purchasing Orgs | 16 |
| Purchasing Groups | 7 |
| Vendors | ~200 |

### Patterns

| Pattern | Count | % |
|---------|-------|---|
| PO > PR (Overpricing) | 993 | 76% |
| PO < PR (Underpricing) | 314 | 24% |

---

## MULTI-CURRENCY ANALYSIS

### Exchange Rates Used (November 2025)

| Currency | Rate (per 1 USD) | Source |
|----------|------------------|--------|
| USD | 1.00 | Base |
| KES (Kenyan Shilling) | 129.24 | Market rate |
| TZS (Tanzanian Shilling) | 2,429 | Market rate |
| ZAR (South African Rand) | 17.13 | Market rate |
| UGX (Ugandan Shilling) | 3,636 | Market rate |
| RWF (Rwandan Franc) | 1,446 | Market rate |
| NAD (Namibian Dollar) | 17.31 | Market rate |

### By Currency (Local Values)

| Currency | Records | Total PR Value | Total PO Value | Difference |
|----------|---------|----------------|----------------|------------|
| KES | 534 | 1,255,620,977 | 817,047,309 | -438,573,668 |
| TZS | 381 | 431,624,312 | 1,200,354,615 | +768,730,303 |
| ZAR | 218 | 13,010,955 | 9,685,029 | -3,325,926 |
| UGX | 156 | 1,456,237 | 67,914,870 | +66,458,633 |
| NAD | 9 | 157,834 | 95,015 | -62,820 |
| RWF | 7 | 7,564,600 | 4,739,864 | -2,824,736 |
| USD | 2 | 24,451,000 | 386,012 | -24,064,988 |

### By Currency (Converted to USD)

| Currency | Records | PR Value (USD) | PO Value (USD) | Diff (USD) |
|----------|---------|----------------|----------------|------------|
| KES | 534 | $9,715,418 | $6,322,617 | -$3,392,801 |
| TZS | 381 | $177,696 | $494,177 | +$316,481 |
| ZAR | 218 | $759,542 | $565,456 | -$194,086 |
| UGX | 156 | $401 | $18,678 | +$18,278 |
| NAD | 9 | $9,118 | $5,489 | -$3,629 |
| RWF | 7 | $5,231 | $3,278 | -$1,954 |
| USD | 2 | $24,451,000 | $386,012 | -$24,064,988 |
| **TOTAL** | **1,307** | **$35,118,406** | **$7,795,706** | **-$27,322,700** |

---

## CONCENTRATION ANALYSIS

### By Purchasing Organization

| Rank | Org | Records | Diff (USD) | Avg Diff |
|------|-----|---------|------------|----------|
| 1 | **MR03** | 8 | **+$827,638** | **$103,455** |
| 2 | SS02 | 1 | +$335,444 | $335,444 |
| 3 | SS01 | 42 | +$191,338 | $4,556 |
| 4 | AL01 | 222 | +$179,003 | $806 |
| 5 | AL02 | 158 | +$132,508 | $839 |
| 6 | MR01 | 349 | +$59,476 | $170 |
| 7 | SB01 | 42 | +$27,577 | $657 |
| 8 | UB01 | 156 | +$18,278 | $117 |

**Critical**: MR03 has only 8 records but **$827K overpricing** - avg $103K per transaction.

### By Purchasing Group

| Group | Records | Diff (USD) | Note |
|-------|---------|------------|------|
| 5 (Service) | 790 | +$1,137,496 | Largest positive diff |
| 4 (Consumables) | 277 | -$127,048 | |
| 8 | 204 | -$777,967 | |
| **1** | **19** | **-$27,555,935** | **Unusual - 19 records, -$27.5M** |

**Insight**: Group 1 has only 19 records but -$27.5M difference - requires investigation.

### By User (Created By)

| Rank | User | Records | Diff (USD) |
|------|------|---------|------------|
| 1 | FYUSUFALI | 130 | +$111,085 |
| 2 | FGONDWE | 101 | +$57,402 |
| 3 | DMARARO | 67 | +$51,458 |
| 4 | MMBUGUA | 31 | +$27,427 |
| 5 | BKISIWA | 48 | +$26,328 |

### Top 10 Overpriced Transactions (USD)

| PR Number | Org | Currency | PR Value | PO Value | Diff | Diff (USD) |
|-----------|-----|----------|----------|----------|------|------------|
| 65773942 | SS02 | ZAR | 1 | 5,746,149 | +5,746,148 | **$335,444** |
| 65977317 | MR03 | KES | 600,000 | 39,776,260 | +39,176,260 | $303,128 |
| 65872781 | AL02 | TZS | 2,000,000 | 466,120,000 | +464,120,000 | $191,075 |
| 65977317 | MR03 | KES | 350,000 | 24,562,360 | +24,212,360 | $187,344 |
| 65977317 | MR03 | KES | 300,000 | 20,082,350 | +19,782,350 | $153,067 |

**Critical**: PR 65773942 - PR value of **1 ZAR** became PO of **5.7M ZAR** - extreme red flag.

### Top Vendors by Overpricing (USD)

| Vendor | Name | Records | Diff (USD) |
|--------|------|---------|------------|
| 2001106 | **GLOBETECH ASIA** | 1 | **+$335,444** |
| 2005314 | M.M.INTEGRATED STEEL MILLS | 1 | +$191,075 |
| 2010152 | TRIDENT REFRACTORY | 1 | +$80,535 |
| 2000929 | NAIVAS LTD | 16 | +$76,425 |
| 2012073 | UEC ENGINEERING | 1 | +$53,612 |

---

## RISK ASSESSMENT

### Classification

| Attribute | Value | Reasoning |
|-----------|-------|-----------|
| Focus Area | BUSINESS_CONTROL | Procurement approval controls |
| Severity | HIGH | $2.1M potential unauthorized increases |
| Risk Score | 75/100 | Significant value differences, concentration patterns |
| Fraud Indicator | INVESTIGATE | Extreme PR→PO increases (1 ZAR → 5.7M ZAR) |

### Risk Indicators

| Risk | Evidence | Action |
|------|----------|--------|
| **Approval Bypass** | PO values exceeding PR thresholds | Audit approval workflow |
| **Dummy PR Values** | PR=1, PO=5.7M (SS02) | Investigate all PRs with value 1 |
| **Concentration** | MR03: 8 records, $827K overpricing | Review MR03 purchasing authority |
| **Vendor Collusion** | GLOBETECH ASIA: single $335K increase | Verify vendor relationship |

---

## RECOMMENDED ACTIONS

### Immediate (24-48 hours)

1. **Investigate PR 65773942 (SS02)**
   - PR value: 1 ZAR, PO value: 5.7M ZAR
   - Verify if this is data error or approval bypass
   - Check who approved the PO

2. **Review MR03 Purchasing Organization**
   - 8 records with $827K total overpricing
   - Average $103K per transaction
   - Identify who has PO creation authority

3. **Audit GLOBETECH ASIA Vendor**
   - Single transaction with $335K increase
   - Verify goods/services received
   - Check for related-party relationships

### Short-term (1-2 weeks)

4. **Review all PRs with value = 1**
   - Common pattern for placeholder values
   - May indicate intentional understatement

5. **Purchasing Group 1 Investigation**
   - 19 records with -$27.5M difference
   - Understand the business reason

6. **PR 65977317 Full Audit**
   - Multiple line items with significant increases
   - Same PR appearing in multiple high-value transactions

### Process Improvements

7. **Implement PR-to-PO variance threshold** - alert when PO exceeds PR by >20%
8. **Block PRs with nominal values** (1, 0) from PO conversion without approval
9. **Add dual approval** for PO values exceeding PR by significant amounts

---

## DETECTION LOGIC

**What the alert detects**: Difference between PR value and PO value

```
PO_PREQ_DIFF = TOT_PO_VAL - TOT_PREQ_VAL
Where:
  TOT_PREQ_VAL = EBAN.MENGE × EBAN.PREIS / EBAN.PEINH
  TOT_PO_VAL = EKPO.NETWR (converted to PR currency if different)
Filter: PO_PREQ_DIFF ≠ 0
```

**Data Sources**:
- EBAN: Purchase Requisition
- EKPO: Purchase Order Items
- EKKO: Purchase Order Header
- EKET: Scheduling Agreement/PO Schedule Lines

**Currency Conversion**: When PR currency ≠ PO currency, PO value is converted using EKKO.WKURS exchange rate.

---

## ARTIFACTS ANALYZED

| Artifact | File |
|----------|------|
| Code | `Code_PREQ & PO value check_200025_001414.txt` |
| Summary | `Summary_PREQ & PO value check_200025_001414.csv` |
| Explanation | `Explanation_PREQ & PO value check_200025_001414.docx` |
| Metadata | `Metadata _PREQ & PO value check_200025_001414.xlsx` |

**Location**: `docs/skywind-4c-alerts-output/Applications/PUR/200025_001414 - PREQ & PO value check/`

---

## CONTENT ANALYZER OUTPUT

```json
{
  "alert_id": "200025_001414",
  "alert_name": "PREQ & PO value check",
  "module": "PUR",
  "classification": {
    "focus_area": "BUSINESS_CONTROL",
    "severity": "HIGH",
    "risk_score": 75,
    "fraud_indicator": "INVESTIGATE"
  },
  "metrics": {
    "record_count": 1307,
    "total_pr_value_usd": 35118406,
    "total_po_value_usd": 7794955,
    "net_difference_usd": -27323451,
    "overpricing_records": 993,
    "total_overpricing_usd": 2115529,
    "max_single_overpricing_usd": 335444
  },
  "currencies": ["KES", "TZS", "ZAR", "UGX", "RWF", "USD", "NAD"],
  "exchange_rates": {
    "USD": 1.0,
    "KES": 129.24,
    "TZS": 2429,
    "ZAR": 17.13,
    "UGX": 3636,
    "RWF": 1446,
    "NAD": 17.31,
    "rate_date": "November 2025"
  },
  "concentration": {
    "top_org": {"code": "MR03", "diff_usd": 827638, "records": 8},
    "top_vendor": {"name": "GLOBETECH ASIA", "diff_usd": 335444}
  },
  "key_finding": "1,307 PR-to-PO transactions with value differences. 993 records (76%) show PO exceeding PR totaling $2.1M potential unauthorized increases. Single PR of 1 ZAR converted to 5.7M ZAR PO requires immediate investigation.",
  "recommended_actions": [
    "Investigate PR 65773942 - 1 ZAR to 5.7M ZAR increase",
    "Review MR03 purchasing org - $827K overpricing in 8 records",
    "Audit GLOBETECH ASIA vendor relationship"
  ]
}
```

---

*Analysis Date: 2025-11-27 | Template Version: 1.0*

**Exchange Rate Sources:**
- [Wise Currency Converter](https://wise.com/gb/currency-converter/)
- [Exchange-Rates.org](https://www.exchange-rates.org/)
- [Trading Economics](https://tradingeconomics.com/)
