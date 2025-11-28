# Comparison of Monthly Purchase Volume by Vendor - Alert Analysis

> **TEMPLATE: Quantitative Alert Analysis**

---

## BUSINESS CONTEXT

> **Business Purpose:** This alert monitors vendor spending patterns to identify unusual changes in purchase volumes compared to the same period last year. It helps procurement and finance teams detect potential maverick spending, unauthorized vendor relationships, budget overruns, or fraudulent activity such as fictitious vendors or kickback schemes. Extreme variances often indicate either business opportunities that need proper controls or risks that require immediate investigation.

### What This Alert Monitors

**Vendor Spend Trends** - Compares purchase volume by vendor between current period and same period last year (YoY). Flags vendors with exceptional variance (outside -50% to +200%).

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Maverick Spending** | Purchases bypassing procurement controls |
| **Budget Overruns** | Unexpected spend increases |
| **Fraud Indicators** | Fictitious vendors, kickback schemes |

### Interpreting the Findings

| Variance | Legitimate Cause | Red Flag |
|----------|------------------|----------|
| Large increase (>200%) | New contract, project, bulk buy | Unauthorized purchasing, fictitious vendor |
| Extreme increase (>1000%) | New vendor relationship | **Almost always requires investigation** |
| Large decrease (>50%) | Vendor replaced, contract ended | May indicate unresolved disputes |

---

## EXECUTIVE SUMMARY

### Alert Identity

| | |
|---|---|
| **Alert Name** | Comparison of monthly purchase volume by vendor |
| **Alert ID** | 200025_001373 |
| **Module** | FI (Finance - Accounts Payable) |
| **Category** | Applications |
| **Subcategory** | FI Alerts |

### Execution Context

| | |
|---|---|
| **Source System** | Production S4 (PS4) |
| **Created** | 20.10.2025 at 10:56 by SKYWATCH |
| **Last Executed** | 26.11.2025 at 10:58 |
| **Exception Indicator** | SW_10_07_CM_MN_VL_CV |

### Alert Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| BACKMONTHS | 1 | Compare 1 month back from current |
| COMPMONTHS | 12 | Compare to same month 12 months ago (YoY) |
| DC_IND | C | Creditor (Vendor) - not Customer |
| PERC_VARI | Exclude -50 to 200 | Only show variances outside this range |

### THE BOTTOM LINE

| | |
|---|---|
| **Vendors Flagged** | **233 vendors** with exceptional YoY variance |
| **Variance Range** | -6,583% to +27,465% |
| **Comparison Period** | October 2025 vs October 2024 |
| **Severity** | HIGH |
| **Fraud Indicator** | INVESTIGATE - Significant anomalies detected |

### WHAT HAPPENED

233 vendors showed exceptional year-over-year purchase volume changes (outside -50% to +200%). 138 vendors had significant decreases (>50% drop), 95 had significant increases (>200% growth). Top spike: +27,465% for AON MINET INSURANCE BROKERS.

### TOP 3 FINDINGS

1. **AON MINET INSURANCE BROKERS (KE03)**: +27,465% increase - **INVESTIGATE IMMEDIATELY**
2. **BLUE SKY CARGO MOVERS (RW01)**: +13,599% increase - Major spend spike
3. **AUTO CENTRE GARAGE (KE01)**: -6,583% decrease - Vendor relationship change

### IMMEDIATE ACTIONS REQUIRED

1. **URGENT**: Investigate top 5 vendors with >5,000% variance
2. Review procurement approvals for vendors with >1,000% increase
3. Verify vendor changes for significant decreases

---

## KEY METRICS

### Variance Statistics

| Metric | Value |
|--------|-------|
| Vendors Flagged | 233 |
| Min Variance | -6,583% |
| Max Variance | +27,465% |
| Mean Variance | +489% |
| Median Variance | -61% |

### Volume by Direction

| Direction | Count | % of Total |
|-----------|-------|------------|
| Significant INCREASE (>200%) | 95 | 41% |
| Significant DECREASE (>50%) | 138 | 59% |

---

## CONCENTRATION ANALYSIS

### By Company Code

| Rank | Company | Vendors | Avg Variance |
|------|---------|---------|--------------|
| 1 | **KE01** (Mabati Rolling Mills) | 64 | +379% |
| 2 | **TZ01** (ALAF Limited) | 47 | +585% |
| 3 | **SA01** (Safal Steel) | 44 | +337% |
| 4 | **KE03** (Safal Building Systems) | 31 | +579% |
| 5 | **UG01** (Uganda Baati) | 25 | +223% |
| 6 | **RW01** (Safintra Rwanda) | 12 | **+1,856%** |
| 7 | NA01 | 6 | +110% |
| 8 | SA02 | 4 | +244% |

**Insight**: RW01 has highest average variance (+1,856%) - concentrated anomalies.

### Top 10 Largest INCREASES

| Rank | Vendor | Company | Variance |
|------|--------|---------|----------|
| 1 | **AON MINET INSURANCE BROKERS** | KE03 | **+27,465%** |
| 2 | BLUE SKY CARGO MOVERS | RW01 | +13,599% |
| 3 | LYNNTECH CHEMICALS | KE01 | +11,733% |
| 4 | MASANGULA GARAGE | TZ01 | +10,000% |
| 5 | AIR PRODUCTS SA | SA01 | +9,276% |
| 6 | KANSAI PLASCON | TZ01 | +6,871% |
| 7 | EOH MTHOMBO | TZ01 | +4,945% |
| 8 | ROBOTICS NETWORKS | UG01 | +4,485% |
| 9 | TONY MEDIA & PR | KE01 | +3,900% |
| 10 | BUREAU VERITAS KENYA | KE01 | +3,538% |

**Critical**: Top vendors show 3,500% to 27,000%+ variance.

### Top 10 Largest DECREASES

| Rank | Vendor | Company | Variance |
|------|--------|---------|----------|
| 1 | AUTO CENTRE GARAGE | KE01 | **-6,583%** |
| 2 | REAL AUTO SPARES | KE03 | -6,320% |
| 3 | Wilfred Makori Gwaka | KE01 | -5,009% |
| 4 | SEVEN SUNDAY MANUFACTURING | KE03 | -4,302% |
| 5 | RSM CONSULTING | TZ01 | -2,192% |
| 6 | RWEGO TECH | TZ01 | -2,154% |
| 7 | WS RISK PROTECTIVE | TZ01 | -887% |
| 8 | Rose Odhiambo | KE01 | -507% |
| 9 | BATTAMA INVESTMENTS | UG01 | -413% |
| 10 | Santosh Panda | KE03 | -142% |

---

## RISK ASSESSMENT

### Classification

| Attribute | Value | Reasoning |
|-----------|-------|-----------|
| Focus Area | BUSINESS_CONTROL | Procurement spend monitoring |
| Severity | HIGH | Significant variance patterns |
| Risk Score | 75/100 | High variance, requires investigation |
| Fraud Indicator | INVESTIGATE | Extreme spikes could indicate fictitious vendors |

### Risk Indicators

| Risk | Evidence | Action |
|------|----------|--------|
| **Maverick Spending** | 95 vendors with >200% increase | Review procurement approvals |
| **Vendor Issues** | 138 vendors with >50% decrease | Verify intentional changes |
| **Potential Fraud** | 5 vendors with >5,000% variance | Investigate transactions |
| **Budget Risk** | KE01 has 64 vendors flagged | Review department budgets |

---

## RECOMMENDED ACTIONS

### Immediate (24-48 hours)

1. **Investigate top 5 extreme increases** (>5,000% variance)
   - AON MINET INSURANCE BROKERS
   - BLUE SKY CARGO MOVERS
   - LYNNTECH CHEMICALS

2. **Review RW01 (Rwanda)** - highest average variance (+1,856%)

3. **Verify goods receipt** for top 10 increased vendors

### Short-term (1-2 weeks)

4. **Audit procurement approvals** for all >1,000% increases

5. **Review vendor master changes** - check for duplicates

6. **Budget variance analysis** by cost center

### Process Improvements

7. **Implement spend alerts** at lower thresholds
8. **Require additional approval** for first-time large payments
9. **Monthly procurement review** for top variances

---

## DETECTION LOGIC

**What the alert detects**: YoY variance in vendor purchase volume

```
PERC_VARI = (Current Period / Prior Year Same Period) × 100 - 100
Filter: PERC_VARI < -50% OR PERC_VARI > 200%
```

**Data Sources**:
- LFA1/LFB1: Vendor Master
- LFC1: Vendor Transaction Figures

---

## ARTIFACTS ANALYZED

| Artifact | File |
|----------|------|
| Code | `Code_Comparison of monthly purchase volume by vendor_200025_001373.txt` |
| Summary | `Summary_Comparison of monthly purchase volume by vendor_200025_001373.csv` |
| Explanation | `Explanation_Comparison of monthly purchase volume by vendor_200025_001373.docx` |
| Metadata | `Metadata _Comparison of monthly purchase volume by vendor_200025_001373.xlsx` |

**Location**: `docs/skywind-4c-alerts-output/Applications/FI/200025_001373 - Comparison of monthly purchase volume by vendor/`

---

## CONTENT ANALYZER OUTPUT

```json
{
  "alert_id": "200025_001373",
  "alert_name": "Comparison of monthly purchase volume by vendor",
  "module": "FI",
  "classification": {
    "focus_area": "BUSINESS_CONTROL",
    "severity": "HIGH",
    "risk_score": 75,
    "fraud_indicator": "INVESTIGATE"
  },
  "metrics": {
    "vendors_flagged": 233,
    "variance_min": -6583,
    "variance_max": 27465,
    "variance_mean": 489,
    "increases_count": 95,
    "decreases_count": 138
  },
  "concentration": {
    "top_company": {"code": "KE01", "vendors": 64},
    "highest_avg_variance": {"code": "RW01", "avg_variance": 1856}
  },
  "key_finding": "233 vendors with exceptional YoY variance. Top spike: AON MINET at +27,465%. Requires procurement investigation.",
  "recommended_actions": [
    "Investigate 5 vendors with >5,000% variance",
    "Review RW01 procurement - highest avg variance",
    "Verify goods receipt for top increased vendors"
  ]
}
```

---

*Analysis Date: 2025-11-27 | Template Version: 1.0*
