# Alert Analysis: Negative Profit Deal (SD Module)

**Alert ID**: 200025_001441
**Module**: SD (Sales & Distribution)
**Date Analyzed**: 2025-11-27
**Status**: AI Interpretation Complete - Awaiting User Comparison

---

## Purpose

This document captures the AI analysis of the "Negative Profit Deal" alert to establish a baseline interpretation. The goal is to compare with the user's interpretation to identify gaps in understanding, then use those insights to improve the Content Analyzer.

---

## Artifacts Analyzed

| Artifact | File | Status |
|----------|------|--------|
| Code | `Code_Negative Profit Deal_200025_001441.txt` | ✅ Analyzed |
| Summary | `Summary_Negative Profit Deal_200025_001441_USD_ONLY.csv` | ✅ Analyzed |
| Explanation | Not yet provided | ⏳ Pending |
| Metadata | Not yet provided | ⏳ Pending |

**Location**: `docs/skywind-4c-alerts-output/Applications/SD/`

---

## Artifact 1: ABAP Code Analysis

### What the Code Does

The ABAP function `/SKN/F_SW_10_01_SALES_REV` detects **sales orders sold below cost**.

**Core Logic** (line 144):
```abap
AND VBAP~NETWR LT VBAP~WAVWR
```

Translation: `Net Value (Revenue) < Cost = Loss`

### Tables Joined
- **VBAK**: Sales Document Header
- **VBAP**: Sales Document Item (contains NETWR/WAVWR)

### Data Enrichment
The code enriches raw data with descriptions:
- Customer name (KNA1)
- Sales organization name (TVKOT)
- Material group description (T023T)
- Plant name (T001W)
- Item category text (TVAPT)

### Key Fields Extracted
| Field | Table | Meaning |
|-------|-------|---------|
| NETWR | VBAP | Net Value (what customer pays) |
| WAVWR | VBAP | Cost (what it cost to produce/buy) |
| MPROK | VBAP | Manual Price flag (A = manual change) |
| VKORG | VBAK | Sales Organization |
| KUNNR | VBAK | Customer Number |
| AUART | VBAK | Document Type |

---

## Artifact 2: Summary CSV Analysis

### Overview Statistics

| Metric | Value |
|--------|-------|
| **Total Line Items** | 2,044 |
| **Total Revenue Recorded** | $11,808,927 |
| **Total Cost** | $25,961,924 |
| **Total Negative Profit (Loss)** | **$14,152,997** |
| **Average Loss Per Item** | $6,923 |

### Pattern Breakdown

| Pattern | Count | Percentage | Description |
|---------|-------|------------|-------------|
| **Zero-Price Items** (NETWR=0) | 1,205 | 59% | Items with $0 revenue but cost recorded |
| **Manual Price Change** | 796 | 39% | Human override of pricing |
| **No Manual Change** | 1,246 | 61% | System-calculated (but still loss) |

### By Sales Organization

| Org Code | Name | Items | Loss Amount | % of Total |
|----------|------|-------|-------------|------------|
| **KE01** | MRM Sales Org. | 428 | **$11,446,868** | 81% |
| UG01 | UBL Sales Org. | 1,085 | $829,884 | 6% |
| TZ01 | Tanzania | 142 | $1,392,422 | 10% |
| KE03 | SBS Sales Org. | 274 | $330,235 | 2% |
| RW01 | Rwanda | 87 | $28,743 | <1% |
| ZM01 | Zambia | 28 | $124,845 | <1% |

**Key Insight**: KE01 (Kenya - MRM) accounts for 81% of total loss despite having only 21% of line items.

### By Document Type

| Document Type | Count | Description |
|---------------|-------|-------------|
| Project WBS Order (Z004) | 1,118 | Project-based sales |
| Building Sol. Sales (Z002) | 826 | Standard sales |
| Project Sales | 87 | Project sales |
| Retail Order | 11 | Retail |
| Coated Steel Sales | 2 | Specialty |

### Top 10 Customers by Loss

| Customer | Loss Amount | Items | Avg Loss/Item |
|----------|-------------|-------|---------------|
| **KAMURU TRADING COMPANY** | **$8,148,934** | 14 | $582,067 |
| EASTERN HOPE LTD | $550,728 | 2 | $275,364 |
| BINA TRADES PVT LTD | $479,024 | 1 | $479,024 |
| ADLER STEEL LTD | $448,189 | 1 | $448,189 |
| DIEUDO TRADING | $392,424 | 20 | $19,621 |
| GABRIEL NYERERE MASAITE | $279,486 | 5 | $55,897 |
| MM INTERGRATED STEEL MILLS | $260,040 | 2 | $130,020 |
| MOHAMED HUSSEIN | $243,222 | 340 | $715 |
| LA TRIBUNE COMMERCIALE | $233,065 | 5 | $46,613 |
| ATLAS STEEL LTD | $168,771 | 17 | $9,928 |

### Top 10 Single Line Item Losses

| Loss | Customer | Material | Manual Price? |
|------|----------|----------|---------------|
| **$8,105,816** | KAMURU TRADING COMPANY | P-R.H.S 60X40-1.15MM-5.8M | **Yes** |
| $479,024 | BINA TRADES PVT LTD | USED STEEL ROLLS | **Yes** |
| $448,189 | ADLER STEEL LTD | USED STEEL ROLLS | **Yes** |
| $290,991 | EASTERN HOPE LTD | HR SLIT PROFILED PACK | **Yes** |
| $259,738 | EASTERN HOPE LTD | HR SLIT PROFILED PACK | **Yes** |
| $253,938 | MM INTERGRATED STEEL | CR COIL PACK | **Yes** |
| $161,450 | TEMBO MUGISHO | P-AZ-DUMUZAS-NC110 | **Yes** |
| $140,588 | LA TRIBUNE COMMERCIALE | HR SLIT PROFILED PACK | **Yes** |
| $108,802 | GABRIEL NYERERE MASAITE | HR SLIT PROFILED PACK | **Yes** |
| $105,769 | GABRIEL NYERERE MASAITE | HR SLIT PROFILED PACK | **Yes** |

**Critical Observation**: ALL top 10 losses are **Manual Price Changes**.

---

## AI Classification

### Focus Area: **BUSINESS_CONTROL**

**Reasoning**:
- Revenue/margin leakage is a business process control issue
- Pricing process failure (no hard stop on below-cost sales)
- Not fraud by default (would need investigation to confirm)
- Could escalate to BUSINESS_PROTECTION if fraud is confirmed

### Severity: **CRITICAL**

**Reasoning**:
- $14.15M total financial loss
- Single $8.1M transaction (outlier requiring investigation)
- 81% concentration in one sales org
- Manual override pattern suggests process gap or abuse

### Risk Score: **95** (proposed)

**Breakdown**:
- Base (Critical): 90
- Count adjustment (2000+): +15 → capped contribution
- Money adjustment ($14M+): +20 → capped contribution
- Focus multiplier (BUSINESS_CONTROL): 1.0
- Final: ~95 (capped at 100)

---

## Risk Indicators Identified

### 1. FRAUD / BUSINESS PROTECTION CONCERN
- **$8.1M single transaction** to KAMURU TRADING COMPANY
- All top 10 losses are **Manual Price Changes**
- Pattern: Large discounts concentrated on specific customers

**Action Required**: Investigate KAMURU TRADING relationship

### 2. REVENUE LEAKAGE / BUSINESS CONTROL
- 59% of items priced at $0 (Project WBS Orders)
- Cost flows through but no revenue captured
- Missing hard stop on below-cost pricing

**Process Gap**: No pricing validation rule

### 3. CONCENTRATION RISK
- KE01 (Kenya - MRM): **$11.4M loss** (81% of total)
- Top 3 customers: **$9.2M loss** (65% of total)

**Action Required**: Review KE01 sales processes

### 4. MANUAL OVERRIDE ABUSE
- 39% of items have manual price changes
- 100% of top 10 losses are manual overrides
- No apparent approval workflow

**Process Gap**: Unlimited manual pricing authority

---

## What the Content Analyzer Should Output

```json
{
  "alert_id": "200025_001441",
  "alert_name": "Negative Profit Deal",
  "module": "SD",

  "classification": {
    "focus_area": "BUSINESS_CONTROL",
    "severity": "CRITICAL",
    "risk_score": 95,
    "confidence": 0.9
  },

  "quantitative_analysis": {
    "record_count": 2044,
    "total_loss": 14152997,
    "avg_loss_per_item": 6923,
    "max_single_loss": 8105816,
    "currency": "USD"
  },

  "qualitative_analysis": {
    "what_happened": "2,044 sales order line items sold below cost, resulting in $14.15M direct financial loss. 59% are zero-price Project WBS items, 39% are manual price overrides.",
    "business_risk": "Revenue leakage from pricing process failure. Top 10 losses all involve manual price changes, suggesting possible fraud or unauthorized discounting.",
    "process_gap": "No hard stop preventing below-cost sales. Manual price override authority appears unlimited.",
    "fraud_indicator": true,
    "fraud_reasoning": "Single $8.1M manual discount to one customer; all top losses are manual overrides"
  },

  "concentration_analysis": {
    "by_sales_org": {
      "KE01": {"items": 428, "loss": 11446868, "pct": 81}
    },
    "by_customer": {
      "KAMURU TRADING COMPANY": {"items": 14, "loss": 8148934}
    }
  },

  "recommended_actions": [
    "URGENT: Investigate KAMURU TRADING COMPANY $8.1M transaction",
    "Review all manual price changes > $50K",
    "Implement hard stop for pricing below cost threshold",
    "Add approval workflow for discounts > X%",
    "Audit Project WBS Orders missing pricing config"
  ]
}
```

---

## Pending Information

### From Explanation File
- Business justification for this alert
- What constitutes "acceptable" negative profit (if any)
- Industry context

### From Metadata File
- **BACKDAYS parameter** (how many days of data)
- Any filters applied
- Alert thresholds

### User Interpretation
- Does this match the user's understanding?
- What aspects were missed?
- Are the risk indicators correct?

---

## Gap Analysis (To Be Completed After User Review)

| Aspect | AI Interpretation | User Interpretation | Gap |
|--------|-------------------|---------------------|-----|
| Focus Area | BUSINESS_CONTROL | TBD | |
| Severity | CRITICAL | TBD | |
| Primary Risk | Manual override abuse | TBD | |
| Root Cause | Process gap (no pricing validation) | TBD | |
| Fraud Indicator | Yes (investigate) | TBD | |

---

## Next Steps

1. **User provides their interpretation** of this alert
2. **Compare and identify gaps** in AI understanding
3. **Analyze remaining 2 alerts** (user mentioned 3 total)
4. **Implement Content Analyzer improvements** based on findings

---

*Document created: 2025-11-27*
*Last updated: 2025-11-27*
