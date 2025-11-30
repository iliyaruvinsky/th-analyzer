# Material Moving Average Price Change (>20%) Analysis

> **Alert ID:** SW_10_02_MAT_PRC_CHG | **Module:** MM | **Analysis Date:** November 2025

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 124 price changes |
| Period | 90 days (BACKDAYS parameter) |
| Total Value Impact | ~$6.2 million USD |
| Severity | HIGH |

## Critical Discovery

**DA01 (ALAF Limited, Tanzania) - 90% of All Changes:**
• 112 of 124 changes by single user LDUPLESSIS
• 73 materials with >20% price variance
• Systemic data quality issue requiring audit

## Concentration Pattern

| Valuation Area | Records | Value Impact |
|----------------|---------|--------------|
| DA01 (ALAF Tanzania) | 112 | $756K |
| MR99 (Mabati Kenya) | 2 | **$5.38M** |
| MA01 (Mabati Kenya) | 8 | $75K |

MR99 has $5.38M impact from just 2 records (HRC 999.99% spike) - requires immediate review.

---

## Business Context

> **Business Purpose:** This alert identifies materials using Moving Average Price (MAP) control where the calculated price changed by more than 20% after goods movements or invoice postings. Significant price fluctuations in MAP-controlled materials directly impact inventory valuation and financial reporting accuracy. This alert detects potential data quality issues, posting errors, or unusual procurement pricing that requires immediate investigation to ensure accurate cost accounting.

### What This Alert Monitors

Compares old moving average price (PVPRS_OLD) against newly calculated price (PVPRS_NEW) from material valuation changes in table CKMLHD. Monitors business transactions RMWA, RMWE, RMPR, RMWI, RMRP for materials with price control type 'V' (moving average). Price changes exceeding 20% trigger the alert.

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Financial Misstatement** | Extreme price changes distort inventory valuation and P&L |
| **Data Quality Issue** | May indicate incorrect PO pricing or GR quantity errors |
| **Costing Inaccuracy** | Product cost and profitability analysis becomes unreliable |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| 20-50% change | Commodity price fluctuation, forex | Single material with multiple extreme changes |
| >100% change | Rare - major market shift | Same material oscillating (up/down/up) |
| 999.99% (capped) | First receipt after zero price | Multiple capped changes by same user |

### Critical Context: Valuation Area Specificity

> **Material prices in SAP are VALUATION AREA specific.**
>
> A price change in valuation area DA01 (Tanzania) does NOT affect the same material's
> price in MA01 (Kenya). Each plant/valuation area manages its own inventory values.
>
> **The plant manager in Singapore doesn't care about price changes in USA** -
> this analysis segments findings by valuation area for actionable insights.

---

## 2. Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| **Alert Name** | Material Moving Average Price Change (>20%) |
| **Alert ID** | SW_10_02_MAT_PRC_CHG |
| **Module** | MM (Materials Management) |
| **Category** | SW - Treasure Hunting |
| **Subcategory** | Business Bottlenecks |

### Execution Context

| Attribute | Value |
|-----------|-------|
| **Source System** | Production S4 (PS4) |
| **Created Date** | 28.11.2025 |
| **Last Updated** | 28.11.2025 |
| **Exception Indicator ID** | SW_10_02_MAT_PRC_CHG |
| **Exception Indicator Name** | MM: Material Price Change |
| **Collection Mode** | Full |
| **Execution Mode** | On event presence |
| **Data Saving** | Cloud |

### Alert Parameters

| Parameter | Description | Value |
|-----------|-------------|-------|
| BACKDAYS | Lookback period | 90 days |
| GLVOR | Business Transactions | RMWA, RMWE, RMPR, RMWI, RMRP |
| PEINH_DIFF_PRCT | Price unit diff % | 0 |
| PVPRS_DIFF_PERCT | **Periodic unit price diff %** | **>20%** |
| VPRSV_OLD | Price control | V (Moving Average) |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Total Records** | **124 price changes** |
| **Valuation Areas** | **4 (DA01, MA01, MR99, NB01)** |
| **Materials Affected** | **75 unique materials** |
| **Severity** | **HIGH** |
| **Fraud Indicator** | **INVESTIGATE** |

### What Happened

**124 material price changes** exceeding 20% were detected across **4 valuation areas**. The bulk of changes (**112 records, 90%**) occurred in **DA01 (ALAF Limited, Tanzania)** by user LDUPLESSIS. Material "HRC" shows anomalies in **two different valuation areas** (MA01 and MR99) with prices oscillating wildly - a clear data quality issue requiring investigation at each affected plant.

### Top 3 Findings

1. **DA01 dominates:** 112 of 124 changes (90%) in single valuation area - concentrated data quality issue at ALAF Limited
2. **HRC in two plants:** Material HRC shows anomalies in both MA01 (8 changes, oscillating) and MR99 (2 changes, 999.99% spikes)
3. **71% extreme changes:** 88 of 124 records capped at 999.99% - systemic posting errors

### Immediate Actions

1. **DA01 (ALAF Limited):** Audit user LDUPLESSIS - 112 changes need review
2. **MA01 (Mabati):** Investigate HRC price oscillations - 8 changes in 2 days
3. **MR99 (Mabati):** Review HRC 999.99% spikes - likely posting errors

---

## 3. Key Metrics

### Financial Impact by Valuation Area

| Valuation Area | Company | Records | Materials | TZS | KES | USD |
|----------------|---------|---------|-----------|-----|-----|-----|
| **DA01** | ALAF Limited (TZ) | **112** | 73 | 864,216,961 | - | 415,909 |
| **MA01** | Mabati Rolling Mills (KE) | 8 | 1 | - | 4,877,298 | 37,709 |
| **MR99** | Mabati Rolling Mills (KE) | 2 | 1 | - | 349,022,449 | 2,698,488 |
| **NB01** | Mabati Rolling Mills (KE) | 2 | 1 | - | 0 | 0 |

### Consolidated Impact (USD Equivalent)

| Valuation Area | Local Currency Total | USD Equivalent |
|----------------|---------------------|----------------|
| DA01 (Tanzania) | TZS 864,216,961 | ~$340,000 + $415,909 = **$756,000** |
| MA01 (Kenya) | KES 4,877,298 | ~$37,500 + $37,709 = **$75,000** |
| MR99 (Kenya) | KES 349,022,449 | ~$2,685,000 + $2,698,488 = **$5,383,000** |
| NB01 (Kenya) | 0 | **$0** |
| **Total** | | **~$6,214,000** |

*Exchange rates: TZS 2,540/USD, KES 130/USD (Nov 2025 approximate)*

### Volume by Valuation Area

| Valuation Area | Records | % of Total | Unique Materials | User |
|----------------|---------|------------|------------------|------|
| **DA01** | **112** | **90.3%** | 73 | LDUPLESSIS |
| MA01 | 8 | 6.5% | 1 (HRC) | SONGWAE |
| MR99 | 2 | 1.6% | 1 (HRC) | SONGWAE |
| NB01 | 2 | 1.6% | 1 | SONGWAE |

---

## 4. Concentration Analysis

### By Valuation Area (Primary Segmentation)

| Rank | Valuation Area | Company | Records | Financial Impact |
|------|----------------|---------|---------|------------------|
| 1 | **DA01** | ALAF Limited (TZ) | **112 (90%)** | **$756K USD** |
| 2 | MR99 | Mabati Rolling Mills (KE) | 2 | $5.38M USD |
| 3 | MA01 | Mabati Rolling Mills (KE) | 8 | $75K USD |
| 4 | NB01 | Mabati Rolling Mills (KE) | 2 | $0 |

**Note:** MR99 has only 2 records but highest financial impact - requires priority review.

### By User (Within Valuation Area Context)

| User | Valuation Area | Records | % in Area |
|------|----------------|---------|-----------|
| **LDUPLESSIS** | DA01 (ALAF) | **112** | **100%** |
| SONGWAE | MA01/MR99/NB01 (Mabati) | 12 | 100% |

### By Transaction Code

| Transaction | Description | Count | % |
|-------------|-------------|-------|---|
| MR21 | Price Change | 114 | 91.9% |
| MR22 | Price Change (Reversal) | 10 | 8.1% |

---

## 5. Anomaly Deep Dive: Material HRC

### Critical Finding: HRC Exists in TWO Valuation Areas

Material HRC shows anomalies in **two separate valuation areas** - these are independent issues that affect different plants:

### HRC in Valuation Area MA01 (Mabati Rolling Mills - Main Plant)

```
VALUATION AREA: MA01 | 8 CHANGES | USER: SONGWAE

DATE       │ PRICE BEFORE  │ PRICE AFTER   │ % CHANGE │ CURRENCY
───────────┼───────────────┼───────────────┼──────────┼──────────
2025/10/02 │    243,602.53 │     73,823.00 │   69.70% │ KES
2025/10/02 │      1,884.61 │        571.95 │   69.65% │ USD
2025/10/03 │     73,839.29 │    243,602.53 │  229.91% │ KES      ← UP
2025/10/03 │    243,602.53 │     73,839.29 │   69.69% │ KES      ← DOWN
2025/10/03 │    243,602.53 │     73,839.29 │   69.69% │ KES      ← DOWN
2025/10/03 │        572.08 │      1,884.61 │  229.43% │ USD      ← UP
2025/10/03 │      1,884.61 │        572.08 │   69.64% │ USD      ← DOWN
2025/10/03 │      1,884.61 │        572.08 │   69.64% │ USD      ← DOWN

PATTERN: Classic oscillation - prices swing between ~73K and ~244K (KES)
VALUE IMPACT: KES 4,877,298 (~$37,500 USD)
ROOT CAUSE LIKELY: Posting errors, possibly quantity/price confusion
```

### HRC in Valuation Area MR99 (Mabati Rolling Mills - Alternate)

```
VALUATION AREA: MR99 | 2 CHANGES | USER: SONGWAE

DATE       │ PRICE BEFORE  │ PRICE AFTER   │ % CHANGE │ CURRENCY
───────────┼───────────────┼───────────────┼──────────┼──────────
2025/10/03 │        574.81 │     72,379.34 │  999.99% │ KES      ← EXTREME
2025/10/03 │          4.44 │        559.60 │  999.99% │ USD      ← EXTREME

PATTERN: Extreme spike from near-zero - 999.99% capped
VALUE IMPACT: KES 349,022,449 (~$2.68M USD) + USD $2,698,488 = ~$5.38M
ROOT CAUSE LIKELY: First receipt pricing error OR initial price was wrong
```

### Analysis

The HRC anomalies are **separate issues in separate plants**:

1. **MA01 (8 changes, oscillating):** Characteristic of posting errors being "corrected" incorrectly
   - Should use MR22 reversal, not repeated MR21 changes
   - Quantity/price field confusion possible

2. **MR99 (2 changes, 999.99%):** Characteristic of:
   - First receipt after zero/minimal initial price
   - OR: Massive pricing error on goods receipt
   - **Highest financial impact: $5.38M**

**Action owners differ by plant** - MA01 and MR99 managers need separate notifications.

---

## 6. Risk Assessment

### Classification

| Dimension | Value | Reasoning |
|-----------|-------|-----------|
| **Focus Area** | BUSINESS_CONTROL | Inventory valuation accuracy and costing integrity |
| **Severity** | **HIGH** | 74% extreme changes + oscillating patterns + multi-plant impact |
| **Risk Score** | **72/100** | Data quality issues with significant financial impact |
| **Fraud Indicator** | **INVESTIGATE** | User concentration + oscillating prices warrant review |

### Risk Score Breakdown

| Component | Points | Reasoning |
|-----------|--------|-----------|
| Extreme Changes (74% capped) | 25 | Systemic data quality issue |
| User Concentration (90% one user in DA01) | 20 | Single user dominates |
| Oscillating Prices (HRC in MA01) | 15 | Abnormal pattern |
| Financial Impact (~$6.2M across plants) | 12 | Material inventory impact |
| **Total** | **72** | |

### Risk by Valuation Area

| Valuation Area | Risk Level | Key Issue | Owner Action |
|----------------|------------|-----------|--------------|
| **DA01** | HIGH | 112 changes by one user | Audit LDUPLESSIS transactions |
| **MR99** | CRITICAL | $5.38M from 2 records | Verify HRC pricing immediately |
| **MA01** | MEDIUM | Oscillating pattern | Review posting procedures |
| **NB01** | LOW | No value impact | Monitor only |

---

## 7. Recommended Actions

### By Valuation Area (Actionable by Plant Manager)

#### DA01 - ALAF Limited (Tanzania)
**Owner:** DA01 Plant Controller

1. **Audit user LDUPLESSIS**
   - Review all 112 transactions
   - Identify common error patterns
   - Determine if training needed

2. **Review 999.99% changes**
   - 73 materials affected
   - Validate initial prices were correct
   - Reverse erroneous postings

#### MR99 - Mabati Rolling Mills (Kenya)
**Owner:** MR99 Plant Controller

1. **URGENT: Investigate HRC pricing** (HIGHEST PRIORITY)
   - $5.38M value impact from 2 records
   - Verify goods receipt quantities and prices
   - Determine if initial price of 574.81 KES was correct

#### MA01 - Mabati Rolling Mills (Kenya)
**Owner:** MA01 Plant Controller

1. **Review HRC oscillations**
   - 8 changes in 2 days is abnormal
   - Contact user SONGWAE for explanation
   - Implement MR22 reversal process training

### Process Improvements (All Plants)

1. **Implement price change tolerance validation** before posting
2. **Require supervisor approval** for changes >100%
3. **Add automated detection** for oscillating price patterns
4. **Mandate MR22 for corrections** instead of repeated MR21

---

## 8. Technical Details

### Detection Logic

The ABAP function `/SKN/F_SW_10_02_MAT_PR_CNG_UN` calculates price change percentage:

```abap
' Calculate new moving average price
LV_PVPRS_NEW = LS_DATA-PEINH * (LS_DATA-SALK3_OLD + LS_DATA-SALK3)
               / (LS_DATA-LBKUM_OLD + LS_DATA-LBKUM)

' Calculate percentage difference
LS_DATA-PVPRS_DIFF = ABS(LS_DATA-PVPRS_NEW - LS_DATA-PVPRS_OLD)
LV_PER = (LS_DATA-PVPRS_DIFF / LS_DATA-PVPRS_OLD) * 100

' Cap at 999.99%
IF LV_PER > '999.99'.
  LV_PER = '999.99'.
ENDIF.
```

### Valuation Area (BWKEY) Significance

| Field | Description | Importance |
|-------|-------------|------------|
| BWKEY | Valuation Area | **Primary segmentation key** - prices are plant-specific |
| BUKRS | Company Code | Legal entity for financial reporting |
| MATNR | Material Number | Same material can have different prices per BWKEY |

### Artifacts Analyzed

| File | Description |
|------|-------------|
| `Explanation_Material Moving Average Price Change ( _20_)_SW_10_02_MAT_PRC_CHG.docx` | Business purpose |
| `Metadata _Material Moving Average Price Change ( _20_)_SW_10_02_MAT_PRC_CHG.xlsx` | Alert configuration |
| `Code_Material Moving Average Price Change ( _20_)_SW_10_02_MAT_PRC_CHG.txt` | ABAP detection logic |
| `Summary_Material Moving Average Price Change ( _20_)_SW_10_02_MAT_PRC_CHG.xlsx` | 124 price change records |

### Content Analyzer Output

```json
{
  "alert_id": "SW_10_02_MAT_PRC_CHG",
  "alert_name": "Material Moving Average Price Change (>20%)",
  "module": "MM",
  "source_system": "PS4",
  "analysis_date": "2025-11-28",
  "segmentation": {
    "primary_key": "BWKEY (Valuation Area)",
    "reason": "Material prices are plant-specific"
  },
  "by_valuation_area": {
    "DA01": {
      "company": "ALAF Limited (TZ)",
      "records": 112,
      "materials": 73,
      "user": "LDUPLESSIS",
      "value_TZS": 864216961,
      "value_USD": 415909
    },
    "MA01": {
      "company": "Mabati Rolling Mills (KE)",
      "records": 8,
      "materials": 1,
      "user": "SONGWAE",
      "value_KES": 4877298,
      "value_USD": 37709,
      "anomaly": "HRC oscillating prices"
    },
    "MR99": {
      "company": "Mabati Rolling Mills (KE)",
      "records": 2,
      "materials": 1,
      "user": "SONGWAE",
      "value_KES": 349022449,
      "value_USD": 2698488,
      "anomaly": "HRC 999.99% spike"
    },
    "NB01": {
      "company": "Mabati Rolling Mills (KE)",
      "records": 2,
      "materials": 1,
      "user": "SONGWAE",
      "value_impact": 0
    }
  },
  "totals": {
    "records": 124,
    "materials": 75,
    "valuation_areas": 4,
    "total_usd_equivalent": 6214000
  },
  "classification": {
    "focus_area": "BUSINESS_CONTROL",
    "severity": "HIGH",
    "risk_score": 72,
    "fraud_indicator": "INVESTIGATE"
  }
}
```

---

*Analysis generated following the Quantitative Alert Analysis Template v1.0*
*Key insight: Material prices are VALUATION AREA specific - analysis segmented by BWKEY*
