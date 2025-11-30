# Inventory Count - Plant Level Analysis

> **Alert ID:** 200025_001397 | **Module:** MM | **Analysis Date:** November 2025

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 817 inventory count records |
| Period | 7 days (BACKDAYS parameter) |
| Total Value Impact | ~$407K USD |
| Severity | HIGH |

## Critical Discovery

**DA01 (Tanzania) - "Ghost Inventory" Pattern:**
• 9 records with Book Qty = 0 but Physical Count = 17,162 KG
• 108.3M TZS (~$43K USD) of inventory exists that wasn't in the system
• Either unrecorded goods receipts, prior write-off reversal, or consignment stock issue

## Concentration Pattern

| Plant | Records | USD Impact |
|-------|---------|------------|
| DA01 (Tanzania) | 9 | **$43K** |
| WD01 (Namibia) | 24 | $173K |
| CP02 (South Africa) | 784 | $191K |

DA01 "ghost inventory" (book=0, physical=17,162 KG) requires immediate investigation of unrecorded receipts.

---

## Business Context

> **Business Purpose:** Physical inventory count differences are discrepancies between book quantities and actual physical counts captured in inventory documents (IKPF/ISEG tables). They indicate inventory control failures, theft/shrinkage, system errors, poor counting procedures, or data quality issues, leading to inaccurate financial statements, wrong production planning, compliance violations, and inventory valuation errors.

### What This Alert Monitors

Tracks physical inventory count results where the aggregated difference amount at plant level exceeds a threshold. The alert joins IKPF (inventory document header) with ISEG (inventory document items) to identify plants with significant inventory variances.

Key table fields monitored:
- **WERKS** - Plant code
- **DMBTR** - Difference amount in local currency
- **BUCHM** - Book quantity (system)
- **MENGE** - Counted quantity (physical)

### Understanding Inventory Count Variances

| Variance Type | System (BUCHM) | Physical (MENGE) | Meaning |
|---------------|----------------|------------------|---------|
| **Positive** | 0 | 5,000 | Found inventory not in books - unrecorded receipts? |
| **Negative** | 5,000 | 0 | Missing inventory - theft, damage, or unrecorded issues? |
| **Small +/-** | 1,000 | 1,050 | Normal counting variance - within tolerance |

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Financial Misstatement** | Book vs. physical variance directly affects balance sheet accuracy |
| **Operational Risk** | Wrong inventory leads to production delays, stockouts, or overstock |
| **Compliance Violation** | SOX/audit requirements for accurate inventory records |
| **Theft/Shrinkage** | Large unexplained differences may indicate theft or fraud |

---

## 2. Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| **Alert Name** | Inventory Count - Plant Level |
| **Alert ID** | 200025_001397 |
| **Module** | MM (Materials Management) |
| **Category** | Applications |
| **Subcategory** | MM Alerts |

### Execution Context

| Attribute | Value |
|-----------|-------|
| **Source System** | Production S4 (PS4) |
| **Created Date** | 20.10.2025 |
| **Last Updated** | 23.10.2025 |
| **Exception Indicator ID** | SW_10_02_INV_CNT_PLN |
| **Exception Indicator Name** | Inventory count - Plant level (WERKS) |
| **Collection Mode** | Full |
| **Execution Mode** | On event presence |

### Alert Parameters

| Parameter | Description | Value |
|-----------|-------------|-------|
| BACKDAYS | Days backward from today | 7 days |
| **DIFF_AMOUNT** | **Difference threshold** | **>100,000** |
| AGG_LVL | Aggregation level | WERKS (Plant) |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Total USD Impact** | **$407,448** |
| **Total Records** | **817** |
| **Severity** | **HIGH** |
| **Primary Concern** | **INVENTORY CONTROL GAP** |

### What Happened

**817 inventory count items** across **3 plants** and **16 inventory documents** showed differences totaling **$407K USD** over 7 days. **DA01 (Tanzania)** has the most concerning pattern: **AZC material with book qty = 0 but 17,162 KG physically counted** - indicating **108M TZS (~$43K) of inventory exists that wasn't in the system**. WD01 (Namibia) shows potential stock relocation issues. CP02 (South Africa) has typical count variances across multiple materials.

### Top 3 Findings

1. **DA01 Plant - AZC Material "Ghost Inventory":** 9 records show Book Qty = 0, Physical Count = 5,650-5,834 KG per batch. **108M TZS of inventory discovered** that wasn't in the system. Either unrecorded receipts, prior write-off reversals, or consignment stock issue.

2. **WD01 Plant - PPAZC-P "Mirror Variances":** 24 records show equal positive and negative variances - inventory counted as 0 in some locations but found elsewhere. Indicates **stock movement not reflected in system** or incorrect storage location assignments.

3. **CP02 Plant - 96% of Records:** 784 records but only $191K USD impact. Normal inventory count variance pattern across 46 materials - operational counting differences within acceptable range.

### Immediate Actions

1. **Investigate DA01 AZC inventory source** - How did 17,162 KG appear that wasn't in books?
2. **Audit WD01 storage locations** - Verify if PPAZC-P material was physically moved
3. **Review CP02 count procedures** - 784 items with variance suggests process improvement opportunity

---

## 3. Key Metrics

### Financial Impact

| Currency | Records | Local Value | USD Equivalent |
|----------|---------|-------------|----------------|
| ZAR (South Africa) | 784 | 3,441,248 | $191,180 |
| NAD (Namibia) | 24 | 3,113,107 | $172,950 |
| TZS (Tanzania) | 9 | 108,293,300 | $43,317 |
| **TOTAL** | **817** | - | **$407,448** |

### Volume

| Dimension | Count |
|-----------|-------|
| **Total Records** | 817 |
| **Unique Plants** | 3 |
| **Unique Materials** | 46 |
| **Inventory Documents** | 16 |
| **Unique Users** | 3 |

### Variance Pattern

| Pattern | Records | % of Total |
|---------|---------|------------|
| Positive (Found more than book) | 378 | 46.3% |
| Negative (Found less than book) | 439 | 53.7% |
| Exact match | 0 | 0% |

---

## 4. Concentration Analysis

### By Plant (The Plant Manager View)

| Rank | Plant | Country | Records | Local Value | USD Impact | Avg/Record |
|------|-------|---------|---------|-------------|------------|------------|
| 1 | **DA01** | Tanzania | **9** | **108.3M TZS** | **$43,317** | **$4,813** |
| 2 | WD01 | Namibia | 24 | 3.1M NAD | $172,950 | $7,206 |
| 3 | CP02 | South Africa | 784 | 3.4M ZAR | $191,180 | $244 |

**Insight:** DA01 has only 9 records but the highest per-record impact. WD01 has a high average indicating concentrated variance. CP02 has many small variances.

### By Material (Top 10)

| Rank | Material | Plant | Records | Total Diff (Local) | USD Est. |
|------|----------|-------|---------|-------------------|----------|
| 1 | **AZC** | DA01 | **9** | **108.3M TZS** | **$43,317** |
| 2 | PPAZC-P | WD01 | 24 | 3.1M NAD | $172,950 |
| 3 | PPAL-S-FS-FL | CP02 | 21 | 911K ZAR | $50,611 |
| 4 | PPAZC | CP02 | 105 | 745K ZAR | $41,365 |
| 5 | PPAZ-S-FS-FL | CP02 | 133 | 716K ZAR | $39,785 |
| 6 | PPAZC-P | CP02 | 28 | 253K ZAR | $14,052 |
| 7 | 7001831 | CP02 | 7 | 219K ZAR | $12,181 |
| 8 | PPAZ-PF-P | CP02 | 105 | 175K ZAR | $9,702 |
| 9 | PPAZC-S | CP02 | 7 | 150K ZAR | $8,338 |
| 10 | 7200011 | CP02 | 7 | 117K ZAR | $6,527 |

### By User

| Rank | User | Plant | Records | % of Total | Total Diff |
|------|------|-------|---------|------------|------------|
| 1 | **MVISSER** | CP02 | **784** | **95.96%** | 3.4M ZAR |
| 2 | ABOCKING | WD01 | 24 | 2.94% | 3.1M NAD |
| 3 | SMWAISAKILA | DA01 | 9 | 1.10% | 108.3M TZS |

**Note:** Each user manages a single plant. MVISSER handles all South Africa counts.

### By Inventory Document

| Doc Number | Plant | Records | Total Diff | Currency | Posting Date |
|------------|-------|---------|------------|----------|--------------|
| **100040653** | **DA01** | **9** | **108.3M** | **TZS** | **2025/11/20** |
| 100040633 | WD01 | 24 | 3.1M | NAD | 2025/11/17 |
| 100040625 | CP02 | 161 | 1.6M | ZAR | 2025/11/16 |
| 100040608 | CP02 | 147 | 1.1M | ZAR | 2025/11/16 |
| 100040617 | CP02 | 98 | 267K | ZAR | 2025/11/16 |
| 100040619 | CP02 | 84 | 119K | ZAR | 2025/11/16 |
| ... | ... | ... | ... | ... | ... |

---

## 5. Anomaly Deep Dive: DA01 "Ghost Inventory"

### The Pattern

All 9 records in DA01 (Tanzania) show the same unusual pattern:

```
┌────┬────────────┬──────────┬────────────────────┬────────────────────┬──────────────────────┐
│ #  │ Date       │ Material │ Book Qty (System)  │ Physical Count     │ Difference Amount    │
├────┼────────────┼──────────┼────────────────────┼────────────────────┼──────────────────────┤
│ 1  │ 2025/11/20 │ AZC      │ 0.000 KG           │ 5,834.000 KG       │ 12,252,472.87 TZS    │
│ 2  │ 2025/11/20 │ AZC      │ 0.000 KG           │ 5,834.000 KG       │ 12,252,472.87 TZS    │
│ 3  │ 2025/11/20 │ AZC      │ 0.000 KG           │ 5,834.000 KG       │ 12,252,472.87 TZS    │
│ 4  │ 2025/11/20 │ AZC      │ 0.000 KG           │ 5,678.000 KG       │ 11,924,844.18 TZS    │
│ 5  │ 2025/11/20 │ AZC      │ 0.000 KG           │ 5,678.000 KG       │ 11,924,844.18 TZS    │
│ 6  │ 2025/11/20 │ AZC      │ 0.000 KG           │ 5,678.000 KG       │ 11,924,844.18 TZS    │
│ 7  │ 2025/11/20 │ AZC      │ 0.000 KG           │ 5,650.000 KG       │ 11,920,445.65 TZS    │
│ 8  │ 2025/11/20 │ AZC      │ 0.000 KG           │ 5,650.000 KG       │ 11,920,445.65 TZS    │
│ 9  │ 2025/11/20 │ AZC      │ 0.000 KG           │ 5,650.000 KG       │ 11,920,445.65 TZS    │
└────┴────────────┴──────────┴────────────────────┴────────────────────┴──────────────────────┘

TOTAL: Book = 0 KG | Physical = ~17,162 KG | Value = 108.3M TZS (~$43K USD)
```

### Possible Root Causes

| Scenario | Likelihood | Investigation |
|----------|------------|---------------|
| **Unrecorded Goods Receipt** | HIGH | Check for POs/deliveries for AZC that weren't posted |
| **Prior Write-off Reversal** | MEDIUM | Check if AZC was written off but stock remained |
| **Consignment Stock** | MEDIUM | Verify if AZC should be consignment (not in books) |
| **Wrong Material Counted** | LOW | Verify counters identified correct material |
| **System Bug** | LOW | Check if book qty was incorrectly zeroed |

### WD01 Mirror Variance Pattern

WD01 shows an interesting pattern where some batches have:
- Book Qty = 4,416 KG, Physical = 0 KG (MISSING)
- Book Qty = 0 KG, Physical = 4,416 KG (FOUND)

This suggests **stock was physically moved but storage location not updated in SAP**.

---

## 6. Risk Assessment

### Classification

| Dimension | Value | Reasoning |
|-----------|-------|-----------|
| **Focus Area** | BUSINESS_CONTROL | Inventory accuracy directly impacts operations and financials |
| **Severity** | **HIGH** | Large unexplained variance at DA01, potential stock movement issues at WD01 |
| **Risk Score** | **72/100** | Significant control gap but contained to specific plants/materials |
| **Fraud Indicator** | **INVESTIGATE** | DA01 pattern unusual - need root cause before ruling out fraud |

### Risk Score Breakdown

| Component | Points | Reasoning |
|-----------|--------|-----------|
| Financial Impact | 20 | $407K total, concentrated in 2 plants |
| Control Gap | 25 | Book qty = 0 with physical stock = significant control failure |
| Pattern Anomaly | 15 | DA01 all-zero book qty is highly unusual |
| User Concentration | 7 | Each user = one plant, no segregation issue |
| Process Impact | 5 | Inventory accuracy affects production/planning |
| **Total** | **72** | |

### Risk Indicators

| Risk Type | Evidence | Recommended Action |
|-----------|----------|-------------------|
| **UNRECORDED RECEIPTS** | DA01: 17K KG with book qty = 0 | Trace goods receipt history for AZC |
| **STOCK MOVEMENT GAP** | WD01: Mirror +/- variances | Audit storage location transfers |
| **COUNT PROCEDURE** | CP02: 784 items with variance | Review counting methodology |
| **Potential Theft** | Cannot rule out | Investigate DA01 thoroughly |

---

## 7. Recommended Actions

### Immediate (24-48 hours)

1. **DA01 - Investigate AZC Inventory Source**
   - Trace all POs and deliveries for AZC material in past 90 days
   - Check for goods receipts not posted
   - Verify consignment agreements for AZC
   - Interview CBWEMO (counter) and SMWAISAKILA (document creator)

2. **WD01 - Storage Location Audit**
   - Physical inspection of all PPAZC-P storage locations
   - Verify if stock was physically moved without SAP transfer
   - Update storage location if relocation confirmed

3. **Freeze Adjustment Postings**
   - Do not post inventory adjustments until root cause identified
   - Document current state as audit evidence

### Short-term (1-2 weeks)

1. **DA01 Root Cause Analysis**
   - Complete investigation report on AZC variance
   - Determine if goods receipt process has gaps
   - Implement corrective action if receipt process issue

2. **WD01 Process Review**
   - Review stock transfer procedures
   - Implement mandatory SAP transfer before physical move
   - Training for warehouse staff on STO process

3. **CP02 Count Procedure Improvement**
   - Analyze variance patterns by material type
   - Implement cycle counting for high-variance materials
   - Set tolerance thresholds by material group

### Process Improvements

1. **Real-time stock visibility** - Consider RFID/barcode for high-value materials
2. **Mandatory dual-count** for variances >threshold
3. **Automated alerts** for book qty = 0 with physical count >0

---

## 8. Technical Details

### Detection Logic

The ABAP function `/SKN/F_SW_10_02_INVENT_CNT` queries inventory count data from IKPF/ISEG:

```abap
' Key join and filters:
SELECT (fields)
  FROM IKPF AS A
  INNER JOIN ISEG AS B ON A~IBLNR = B~IBLNR AND A~GJAHR = B~GJAHR
  WHERE ...
  GROUP BY B~WERKS B~BUDAT
  HAVING SUM(B~DMBTR) > LV_DIFF_AMOUNT OR SUM(B~DMBTR) < LV_DIFF_AMOUNT_
```

The alert aggregates at plant (WERKS) level and filters for plants where total difference amount exceeds the threshold (100,000 in configured currency).

### Key Fields

| Field | Table | Description |
|-------|-------|-------------|
| IBLNR | IKPF/ISEG | Physical inventory document number |
| WERKS | ISEG | Plant |
| DMBTR | ISEG | Difference amount in document currency |
| BUCHM | ISEG | Book quantity (SAP system) |
| MENGE | ISEG | Counted quantity (physical) |
| USNAM_HD | IKPF | User who created document |
| USNAZ | ISEG | User who counted |

### Artifacts Analyzed

| File | Description |
|------|-------------|
| `Explanation_Inventory count - Plant level_200025_001397.docx` | Business purpose |
| `Metadata _Inventory count - Plant level_200025_001397.xlsx` | Alert configuration |
| `Code_Inventory count - Plant level_200025_001397.txt` | ABAP detection logic (1139 lines) |
| `Summary_Inventory count - Plant level_200025_001397.xlsx` | 817 inventory count records |

### Content Analyzer Output

```json
{
  "alert_id": "200025_001397",
  "alert_name": "Inventory Count - Plant Level",
  "module": "MM",
  "source_system": "PS4",
  "analysis_date": "2025-11-28",
  "metrics": {
    "total_records": 817,
    "unique_plants": 3,
    "unique_materials": 46,
    "inventory_documents": 16,
    "unique_users": 3,
    "total_usd_impact": 407448.15
  },
  "concentration": {
    "by_plant": {
      "DA01": {"records": 9, "local_value": 108293300, "currency": "TZS", "usd": 43317},
      "WD01": {"records": 24, "local_value": 3113107, "currency": "NAD", "usd": 172950},
      "CP02": {"records": 784, "local_value": 3441248, "currency": "ZAR", "usd": 191180}
    },
    "by_user": {
      "MVISSER": {"records": 784, "pct": 95.96},
      "ABOCKING": {"records": 24, "pct": 2.94},
      "SMWAISAKILA": {"records": 9, "pct": 1.10}
    }
  },
  "variance_pattern": {
    "positive_variances": 378,
    "negative_variances": 439,
    "exact_matches": 0
  },
  "anomalies": {
    "da01_ghost_inventory": {
      "material": "AZC",
      "pattern": "Book qty = 0, Physical = 17,162 KG",
      "value_tzs": 108293300,
      "value_usd": 43317,
      "risk": "HIGH - Unrecorded inventory"
    },
    "wd01_mirror_variance": {
      "material": "PPAZC-P",
      "pattern": "Equal positive and negative variances",
      "likely_cause": "Stock movement not reflected in SAP"
    }
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
*Data segmented by Plant (WERKS) per Plant Manager Principle*
