# Material Standard Price Change (>20%) - Analysis

> **Alert ID:** 200005_000009 | **Module:** MM | **Analysis Date:** November 2025

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 45,078 price changes |
| Period | 30 days (BACKDAYS parameter) |
| Total Value Impact | ~$110.1 million USD |
| Severity | CRITICAL |

## Critical Discovery

**DA01 (ALAF Tanzania) - $116.8M from 94 Records:**
• Material AZC-P-A3 prices jumped from ~1,500 TZS to ~1,350,000 TZS (1000x increase)
• This is NOT a price change - it's data corruption (likely PEINH price unit error)
• 31.7% of all records hit 999.99% cap = systemic configuration error

## Concentration Pattern

| Valuation Area | Records | USD Impact |
|----------------|---------|------------|
| DA01 (ALAF Tanzania) | 94 | **$116.8M** |
| MR98 (Mabati Kenya) | 2 | -$4.4M |
| DA02 (ALAF Tanzania) | 15,482 | $27K |

PEINH price unit configuration error causing 1000x price jumps - halt MR21 transactions until fixed.

---

## Business Context

> **Business Purpose:** This alert identifies materials where the standard price has changed by more than 20%. Standard price changes directly impact inventory valuation and cost of goods sold (COGS). Unexpected or unauthorized changes can distort financial statements, enable inventory manipulation, and signal configuration or data quality problems in the standard cost roll process.

### What This Alert Monitors

Tracks standard price changes via transaction MR21 (Price Change) where:
- Price control indicator is "S" (standard price)
- Business transaction is RMPR (change in material price)
- Standard price percentage change exceeds 20%

The alert compares `STPRS_OLD` vs `STPRS_NEW` and calculates the absolute value difference percentage.

### SAP Price Control: Standard (S) vs Moving Average (V)

SAP offers two price control methods for material valuation:

| Price Control | Code | How It Works | When Used |
|---------------|------|--------------|-----------|
| **Standard Price** | S | Fixed price set manually or via cost roll; remains constant until explicitly changed | Manufactured goods, finished products |
| **Moving Average Price** | V | Automatically recalculated with each goods receipt based on weighted average | Raw materials, traded goods |

**Key Differences:**

| Aspect | Standard Price (S) | Moving Average Price (V) |
|--------|-------------------|--------------------------|
| **Update Trigger** | Manual (MR21) or planned cost roll | Automatic on every GR |
| **Variance Handling** | Posts to price difference account | Absorbed into inventory value |
| **Audit Trail** | Clear - each change is a deliberate action | Continuous - harder to trace single impact |
| **Risk** | Outdated prices if not updated | Volatile if purchase prices fluctuate |

**This alert monitors Standard Price (S) changes only** - because each change is a deliberate action that should be reviewed. Moving Average prices are tracked by a separate alert (SW_10_02_MAT_PRC_CHG with VPRSV=V).

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Financial Statement Distortion** | Large price changes immediately revalue inventory, affecting balance sheet and P&L |
| **Standard Cost Roll Issues** | Prices jumping 1000x indicate configuration errors in cost estimates |
| **Data Integrity Problems** | Prices going from near-zero to millions suggest master data corruption |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| 20-50% change | Annual cost roll, commodity price updates | Same material changed multiple times same day |
| 50-100% change | Major supplier change, currency devaluation | Price unit mismatch (1 vs 1000) |
| 999.99% (cap) | New material initial pricing | Prices going from $0.01 to $1000+ indicates corruption |

---

## 2. Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| **Alert Name** | Material Standard Price Change (>20%) |
| **Alert ID** | 200005_000009 |
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

### Alert Parameters

| Parameter | Description | Value |
|-----------|-------------|-------|
| BACKDAYS | Lookback period | 30 days |
| GLVOR | Business Transaction | RMPR (price change) |
| PEINH_DIFF_PRCT | Price unit diff % | 0 |
| **STPRS_DIFF_PERCT** | **Standard price diff %** | **>20** |
| TCODE | Transaction Code | MR21 |
| VPRSV_OLD | Price control | S (Standard) |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Total Value Impact** | **USD $110.1 Million** |
| **Total Records** | **45,078** |
| **Severity** | **CRITICAL** |
| **Primary Concern** | **DATA QUALITY / CONFIGURATION ERROR** |

### What Happened

**45,078 standard price changes** detected across 8 companies over a 30-day period, with **$110.1M net USD impact**. However, **31.7% of records (14,273) hit the 999.99% cap**, indicating prices jumped from near-zero to thousands/millions - a clear sign of **data corruption or configuration errors**, not legitimate price updates. The DA01 valuation area alone shows $116.8M impact from just 94 records where standard prices went from ~1,400 TZS to ~1,350,000 TZS (1000x increase).

### Top 3 Findings

1. **DA01 Valuation Area - AZC-P-A3 Material:** 8 records generated **$116.8M USD impact** (146 Billion TZS) - prices jumped from ~1,500 TZS to ~1,350,000 TZS on same day. This is **not a price change - it's data corruption**.

2. **MR98 Valuation Area - AZ-S-PF-P Material:** Single record shows **-$4.4M USD** (656 Million KES) loss - price dropped from 91,458 KES to 288 KES (99.7% decrease). Likely a **price unit error** or **reversal entry**.

3. **31.7% of records at 999.99% cap:** 14,273 records hit the maximum percentage tracked, with PPAZ-PF-P material accounting for 82% of these. Indicates **systemic configuration issue** in DA02 valuation area (ALAF Tanzania).

### Immediate Actions

1. **HALT MR21 transactions** for DA01, DA02, MR98 valuation areas until root cause identified
2. **Investigate AZC-P-A3 material** - price unit configuration may be wrong (should be per 1000, not per 1?)
3. **Review PPAZ-PF-P material** in DA02 - 11,764 records at 999.99% cap indicates mass data corruption

---

## 3. Key Metrics

### Financial Impact

| Currency | Records | Local Value | USD Equivalent |
|----------|---------|-------------|----------------|
| TZS | 9,473 | 146.3 Billion | $58.5M |
| USD | 24,330 | 56.5 Million | $56.5M |
| KES | 5,956 | -726.3 Million | -$4.8M |
| UGX | 3,881 | -21.1 Million | -$5.7K |
| NAD | 726 | 53.9K | $3.0K |
| RWF | 466 | -946.4K | -$728 |
| MZN | 240 | 673.4K | $10.5K |
| **TOTAL** | **45,078** | - | **$110.1M** |

### Volume

| Dimension | Count |
|-----------|-------|
| **Total Records** | 45,078 |
| **Unique Materials** | 325 |
| **Unique Valuation Areas** | 47 |
| **Unique Users** | 8 |
| **Unique Entry Dates** | 6 |
| **Unique Companies** | 8 |

### % Change Distribution

| Bucket | Records | Percentage |
|--------|---------|------------|
| 20-25% | 5,462 | 12.1% |
| 25-50% | 22,222 | 49.3% |
| 50-75% | 1,578 | 3.5% |
| 75-100% | 481 | 1.1% |
| 100-150% | 410 | 0.9% |
| 150-200% | 194 | 0.4% |
| 200-500% | 315 | 0.7% |
| **500%+ (at cap)** | **14,416** | **32.0%** |

---

## 4. Concentration Analysis

### By Valuation Area (Top 10 by USD Impact)

| Rank | Valuation Area | Company | Records | USD Impact | Avg/Record |
|------|----------------|---------|---------|------------|------------|
| 1 | **DA01** | ALAF Limited (TZ) | **94** | **$116.8M** | **$1.24M** |
| 2 | DA02 | ALAF Limited (TZ) | 15,482 | $27.2K | $1.76 |
| 3 | **MR98** | Mabati Rolling Mills (KE) | **2** | **-$4.4M** | **-$2.2M** |
| 4 | MA01 | Mabati Rolling Mills (KE) | 2,738 | -$1.7M | -$607 |
| 5 | UB99 | Uganda Baati Ltd. | 28 | -$517K | -$18.5K |
| 6 | NB01 | Mabati Rolling Mills (KE) | 5,327 | -$489K | -$92 |
| 7 | NB05 | Mabati Rolling Mills (KE) | 1,395 | $319K | $229 |
| 8 | AL98 | ALAF Limited (TZ) | 36 | $74.3K | $2.1K |
| 9 | KG01 | Safintra Rwanda Ltd. | 1,659 | -$41.3K | -$25 |
| 10 | KL01 | Uganda Baati Ltd. | 6,875 | -$36.6K | -$5.33 |

**CRITICAL:** DA01 and MR98 together account for $121.2M impact from just 96 records. This is not normal pricing - it's data anomaly.

### By Company

| Rank | Company | Country | Records | % of Total |
|------|---------|---------|---------|------------|
| 1 | **ALAF Limited** | Tanzania | **18,901** | **41.9%** |
| 2 | Mabati Rolling Mills Ltd. | Kenya | 13,938 | 30.9% |
| 3 | Uganda Baati Ltd. | Uganda | 7,418 | 16.5% |
| 4 | Safintra Namibia Ltd. | Namibia | 2,548 | 5.7% |
| 5 | Safintra Rwanda Ltd. | Rwanda | 1,659 | 3.7% |
| 6 | Safintra Mozambique Ida | Mozambique | 480 | 1.1% |
| 7 | Safal Building Systems | Kenya | 115 | 0.3% |
| 8 | Safintra Zambia Ltd. | Zambia | 19 | 0.04% |

### By User

| Rank | User | Records | % of Total | Primary Company |
|------|------|---------|------------|-----------------|
| 1 | **FIRONDO** | **18,901** | **41.9%** | ALAF Limited (TZ) |
| 2 | SMURABACHA | 13,938 | 30.9% | Mabati Rolling Mills (KE) |
| 3 | ISEWAAYA | 7,418 | 16.5% | Uganda Baati (UG) |
| 4 | ABOCKING | 2,548 | 5.7% | Safintra Namibia |
| 5 | FSEZIKEYE | 1,659 | 3.7% | Safintra Rwanda |
| 6 | BCEIA | 480 | 1.1% | Safintra Mozambique |
| 7 | EOKENYE | 115 | 0.3% | Safal Building Systems |
| 8 | SONGWAE | 19 | 0.04% | Safintra Zambia |

---

## 5. Anomaly Deep Dive: DA01 Data Corruption

### The AZC-P-A3 Material Anomaly

Material **AZC-P-A3** in valuation area **DA01** (ALAF Tanzania) shows the most extreme data issue:

```
┌────┬────────────┬──────────────────────────────────┬──────────────────────────────────┬─────────────────────────────────┐
│ #  │ Date       │ Standard Price BEFORE            │ Standard Price AFTER             │ Value Change                    │
├────┼────────────┼──────────────────────────────────┼──────────────────────────────────┼─────────────────────────────────┤
│ 1  │ 2025/11/12 │ TZS 2,126,897.72                 │ TZS 1,446,521.17                 │ TZS 0.00 (normal)               │
│ 2  │ 2025/11/12 │ TZS 2,048.11                     │ TZS 1,346,175.52 (1000x!)        │ TZS 17.5 Billion                │
│ 3  │ 2025/11/12 │ TZS 1,408.50                     │ TZS 1,385,967.15 (1000x!)        │ TZS 34.3 Billion                │
│ 4  │ 2025/11/12 │ TZS 1,478.89                     │ TZS 1,358,741.92 (1000x!)        │ TZS 94.3 Billion                │
│ 5  │ 2025/11/12 │ USD 835.39                       │ USD 579.38                       │ USD 0.00 (normal)               │
│ 6  │ 2025/11/12 │ USD 0.57                         │ USD 555.13 (1000x!)              │ USD 13.7 Million                │
│ 7  │ 2025/11/12 │ USD 0.59                         │ USD 544.22 (1000x!)              │ USD 37.8 Million                │
│ 8  │ 2025/11/12 │ USD 0.80                         │ USD 539.19 (1000x!)              │ USD 7.0 Million                 │
└────┴────────────┴──────────────────────────────────┴──────────────────────────────────┴─────────────────────────────────┘
```

### Root Cause Analysis

| Observation | Implication |
|-------------|-------------|
| Prices jump exactly ~1000x | **Price Unit Error**: PEINH may have changed from 1000 to 1, or vice versa |
| All changes on same day (2025/11/12) | Batch process or cost roll run caused mass update |
| Some records show $0 value change, others show billions | Mixed data - some records correct, some corrupted |
| Both TZS and USD records affected | Issue is in cost roll configuration, not currency |

### The 999.99% Cap Problem

**14,273 records** hit the system's maximum trackable percentage (999.99%), concentrated in:

| Material | Valuation Area | Records at Cap |
|----------|----------------|----------------|
| PPAZ-PF-P | DA02 | 11,097 |
| GI-S-PF-P | DA02 | 817 |
| PPAZ-PF-P | AR01 | 1,555 |
| PPAZ-PF-P | MW01 | 368 |

**Pattern:** Prices going from ~100-150 TZS to ~10,000+ TZS indicates either:
1. Price unit changed from per-1000 to per-1
2. Standard cost roll picked up wrong base price
3. Material master configuration error

---

## 6. Risk Assessment

### Classification

| Dimension | Value | Reasoning |
|-----------|-------|-----------|
| **Focus Area** | BUSINESS_CONTROL | Standard cost roll configuration issue affecting inventory valuation |
| **Severity** | **CRITICAL** | $116.8M from 94 records indicates data corruption, not price changes |
| **Risk Score** | **85/100** | High impact but likely configuration error, not fraud |
| **Fraud Indicator** | **INVESTIGATE** | No fraud intent likely, but financial statements may be misstated |

### Risk Score Breakdown

| Component | Points | Reasoning |
|-----------|--------|-----------|
| Financial Magnitude | 30 | $110M+ impact is material to any company |
| Data Quality Signal | 25 | 31.7% at 999.99% cap = systemic problem |
| Concentration Risk | 15 | 94 records = $117M (DA01) |
| Process Control Gap | 15 | MR21 transactions not validated before posting |
| **Total** | **85** | |

### Risk Indicators

| Risk Type | Evidence | Recommended Action |
|-----------|----------|-------------------|
| **INVENTORY MISSTATEMENT** | Prices 1000x higher than should be | Reverse corrupted entries |
| **COGS DISTORTION** | Price changes flow to P&L | Month-end adjustments needed |
| **Configuration Error** | PEINH (price unit) mismatch | Review material master settings |
| **Process Gap** | No pre-validation on MR21 | Add approval workflow |

---

## 7. Recommended Actions

### Immediate (24-48 hours)

1. **REVERSE DA01 AZC-P-A3 ENTRIES**
   - 8 records with $116.8M impact are data corruption
   - Document original correct prices
   - Post correction entries

2. **INVESTIGATE MR98 AZ-S-PF-P**
   - Single record with -$4.4M (656M KES loss)
   - Verify if intentional write-off or error
   - Check price unit (PEINH) setting

3. **HALT COST ROLL IN DA02**
   - 11,711 records at 999.99% cap
   - Review standard cost estimates before next run
   - Validate price unit configuration

### Short-term (1-2 weeks)

1. **Price Unit Audit**
   - Review all materials with >500% price change
   - Compare PEINH before and after
   - Document intended price unit per material

2. **Financial Statement Impact Assessment**
   - Calculate inventory valuation impact
   - Identify P&L distortion from cost roll
   - Prepare adjusting entries if needed

3. **User Training**
   - FIRONDO responsible for 41.9% of records
   - Review MR21 transaction controls
   - Implement approval workflow

### Process Improvements

1. **Add validation rule** in MR21 to flag >100% price changes for approval
2. **Price unit change control** - require dual approval for PEINH changes
3. **Cost roll preview report** - review impact before posting

---

## 8. Technical Details

### Detection Logic

The ABAP function `/SKN/F_SW_10_02_MAT_PR_CNG_UN` monitors standard price changes:

```abap
' Key filters applied:
' - VGART = 'PC' (Price Change document type)
' - GLVOR = 'RMPR' (Change in material price)
' - VPRSV_OLD = 'S' (Standard price control)
' - STPRS_DIFF_PERCT > threshold (20% in this alert)

' Percentage calculation:
IF LS_DATA-PVPRS_OLD <> 0.
  LV_PER = ( LS_DATA-PVPRS_DIFF / LS_DATA-PVPRS_OLD ) * 100.
  IF LV_PER > '999.99'.
    LV_PER = '999.99'.  ' Cap at maximum
  ENDIF.
ENDIF.
```

**Key Insight:** The 999.99 cap masks the true percentage - many changes are actually 10,000%+ but recorded as 999.99%.

### Data Quality Flags

| Flag | Count | Meaning |
|------|-------|---------|
| At 999.99% cap | 14,273 | True % unknown, likely >10,000% |
| Value Change = 0 | ~5,000 | Price changed but no stock on hand |
| Negative Value Change | ~15,000 | Price decrease (legitimate or write-off) |

### Artifacts Analyzed

| File | Description |
|------|-------------|
| `Explanation_MM_ Material Price Change_SW_10_02_MAT_PRC_CHG_11281206.html` | Business purpose (HTML format) |
| `Metadata _Material Standard Price Change( _20%)_200005_000009.xlsx` | Alert configuration |
| `Code_Material Standard Price Change( _20%)_200005_000009.txt` | ABAP detection logic |
| `Summary_Material Standard Price Change( _20%)_200005_000009.xlsx` | 45,078 price change records |

### Content Analyzer Output

```json
{
  "alert_id": "200005_000009",
  "alert_name": "Material Standard Price Change (>20%)",
  "module": "MM",
  "source_system": "PS4",
  "analysis_date": "2025-11-28",
  "metrics": {
    "total_records": 45078,
    "unique_materials": 325,
    "unique_valuation_areas": 47,
    "unique_users": 8,
    "unique_companies": 8,
    "total_usd_impact": 110143211.32,
    "records_at_cap": 14273,
    "pct_at_cap": 31.67
  },
  "concentration": {
    "by_company": {
      "ALAF Limited": {"records": 18901, "pct": 41.93},
      "Mabati Rolling Mills": {"records": 13938, "pct": 30.92},
      "Uganda Baati Ltd": {"records": 7418, "pct": 16.46}
    },
    "by_user": {
      "FIRONDO": {"records": 18901, "pct": 41.93},
      "SMURABACHA": {"records": 13938, "pct": 30.92},
      "ISEWAAYA": {"records": 7418, "pct": 16.46}
    },
    "by_valuation_area_usd": {
      "DA01": {"records": 94, "usd_impact": 116816704.13},
      "MR98": {"records": 2, "usd_impact": -4376125.92}
    }
  },
  "anomalies": {
    "da01_azc_p_a3": {
      "records": 8,
      "usd_impact": 116816704.13,
      "pattern": "Prices jumped 1000x - likely PEINH error"
    },
    "mr98_az_s_pf_p": {
      "records": 1,
      "usd_impact": -4376125.92,
      "pattern": "Price dropped 99.7% - write-off or error"
    },
    "records_at_999_cap": {
      "total": 14273,
      "top_material": "PPAZ-PF-P",
      "top_valuation_area": "DA02"
    }
  },
  "classification": {
    "focus_area": "BUSINESS_CONTROL",
    "severity": "CRITICAL",
    "risk_score": 85,
    "fraud_indicator": "INVESTIGATE",
    "primary_concern": "DATA_QUALITY_CONFIGURATION_ERROR"
  }
}
```

---

*Analysis generated following the Quantitative Alert Analysis Template v1.0*
*Data segmented by Valuation Area (BWKEY) per Plant Manager Principle*
