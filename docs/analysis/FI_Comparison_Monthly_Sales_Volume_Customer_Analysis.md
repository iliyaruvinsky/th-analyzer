# Key Findings Analysis: Comparison of Monthly Sales Volume by Customer

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 211 unique customers flagged |
| Period | October 2025 vs October 2024 (YoY comparison) |
| Total Value | ~$4.7 million USD (prior year sales for flagged customers) |
| Severity | **MEDIUM** |

### Critical Discovery

**Tanzania (TZ01) Concentration with Major Declines:**

* 91.8% of total sales value concentrated in TZ01 company code ($4.3M USD)
* Top 8 of 10 largest customers show DECLINES between -58% and -98%
* Largest customer dropped 89% (from $634K to $69K) - requires immediate investigation

### Concentration Pattern

| Company Code | Customers | % of Value | Avg Variance |
|--------------|-----------|------------|--------------|
| TZ01 (Tanzania) | 55 (26%) | **91.8%** | +152% |
| KE01 (Kenya) | 88 (42%) | 7.0% | -406% |
| UG01 (Uganda) | 35 (17%) | 0.5% | +193% |
| SA01 (South Africa) | 14 (7%) | 0.6% | +42% |

Despite TZ01 showing +152% average variance, top individual customers are declining significantly.

---

## Business Context

> **Business Purpose:** This alert tracks year-over-year changes in customer sales revenue by comparing current fiscal period to prior year same period. It detects unusual sales patterns, pricing anomalies, major customer growth/loss, revenue leakage, duplicate customer accounts, or fraudulent sales schemes requiring sales management review and revenue analysis.

### What This Alert Monitors

Compares customer transaction figures (KNC1 table) between fiscal periods, calculating percentage variance between current period sales (UMXXU_TGT) and prior year same period sales (UMXXU_CMP).

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| Revenue Loss | Major customer declines = lost market share |
| Concentration Risk | 92% in one region = business vulnerability |
| Pricing Anomaly | Extreme variances may indicate pricing errors or fraud |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|-----------------|----------|
| High growth (>200%) | New contracts, market expansion | Duplicate accounts, revenue manipulation |
| Severe decline (<-50%) | Customer churn, market conditions | Lost contracts without explanation |
| Extreme variance (>1000%) | New customer, data issue | Data quality problem or fraud |

---

## Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| Alert Name | Comparison of monthly sales volume by customer |
| Alert ID | 200025_001374 |
| Module | FI |
| Category | Applications |
| Subcategory | FI Alerts |

### Execution Context

| Attribute | Value |
|-----------|-------|
| Source System | **Production S4 (PS4)** |
| Created On | 20.10.2025 at 10:57 by SKYWATCH |
| Last Executed | 18.11.2025 - 23.11.2025 (8 executions) |
| Exception Indicator ID | SW_10_07_CM_MN_VL_CV |

### Alert Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| BACKMONTHS | 1 | Months backwards (start from October 2025) |
| COMPMONTHS | 12 | Compare with October 2024 (12 months prior) |
| DC_IND | D | Debtor (Customer) indicator |
| PERC_VARI | Exclude -50 to 200 | Flag variances outside normal range |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Total Prior Year Sales** | **~$4.7M USD** (11.4B TZS + 863M KES + 79M ZAR + 56M UGX) |
| **Customers Flagged** | 211 unique customers |
| **Severity** | **MEDIUM** |
| **Fraud Indicator** | **INVESTIGATE** - Extreme variances require validation |

### What Happened

211 customers across 7 company codes showed sales volume variances outside the normal -50% to +200% range when comparing October 2025 to October 2024. Tanzania (TZ01) dominates with 91.8% of value, but its top customers are experiencing severe declines (up to -98%), while some smaller customers show extreme growth (up to +3,394%).

### Top 3 Findings

1. **TZ01 largest customer declined 89%** - From TZS 1.54B ($634K) to ~TZS 168M ($69K) - represents potential loss of major customer relationship
2. **Rwanda (RW01) extreme variance +11,897%** - 5 customers with 11,897% increase from minimal prior year base - likely data quality issue or new customers
3. **Kenya (KE01) extreme decline -35,889%** - Customer with -35,889% variance indicates potential data issue (negative prior year value)

### Immediate Actions

1. **Review top 10 TZ01 declining customers** - Verify if these are genuine customer losses or data issues
2. **Validate RW01 extreme growth** - Check if these are new customers or data entry errors
3. **Investigate KE01 negative variance** - The -35,889% variance suggests data quality problem requiring correction

---

## Key Metrics

### Financial Impact (Prior Year Sales by Currency)

| Currency | Company Codes | Local Amount | USD Equivalent | Exchange Rate |
|----------|---------------|--------------|----------------|---------------|
| TZS | TZ01 | 11,382,330,000 | $4,686,000 | 2,429/USD |
| KES | KE01, KE03 | 884,293,600 | $6,843,000 | 129.24/USD |
| ZAR | SA01 | 79,039,020 | $4,391,000 | 18/USD |
| UGX | UG01 | 55,841,010 | $15,400 | 3,636/USD |
| NAD | NA01 | 217,440 | $12,100 | 18/USD |
| RWF | RW01 | -4,594,875 | -$3,200 | 1,446/USD |
| **Total** | | | **~$15.9M USD** | |

*Note: Exchange rates as of November 2025*

### Volume

| Metric | Count |
|--------|-------|
| Unique Customers Flagged | 211 |
| Company Codes | 7 |
| Execution Records | 1,688 (duplicate from multiple alert runs) |

### Variance Patterns

| Pattern | Count | % of Flagged |
|---------|-------|--------------|
| Severe decline (<-50%) | 151 | 72% |
| High growth (>200%) | 60 | 28% |
| Extreme (>1000% or <-1000%) | 18 | 9% |

---

## Concentration Analysis

### By Company Code

| Rank | Company Code | Country | Customers | Total Sales (USD) | % of Total | Avg Variance |
|------|--------------|---------|-----------|-------------------|------------|--------------|
| 1 | TZ01 | Tanzania | 55 | $4,686,000 | **91.8%** | +152% |
| 2 | KE01 | Kenya | 88 | $6,843,000 | 7.0% | -406% |
| 3 | SA01 | South Africa | 14 | $4,391,000 | 0.6% | +42% |
| 4 | UG01 | Uganda | 35 | $15,400 | 0.5% | +193% |
| 5 | KE03 | Kenya | 7 | $162,000 | 0.2% | -427% |
| 6 | NA01 | Namibia | 7 | $12,100 | 0.0% | +293% |
| 7 | RW01 | Rwanda | 5 | -$3,200 | 0.0% | +2,473% |

**Observation:** TZ01 at 91.8% represents extreme concentration risk.

### Top 5 Customers by Prior Year Sales (TZ01)

| Rank | Prior Year Sales (TZS) | USD Equivalent | Variance | Pattern |
|------|------------------------|----------------|----------|---------|
| 1 | 1,540,677,000 | $634,000 | **-89%** | Major decline |
| 2 | 1,228,483,000 | $506,000 | **-58%** | Major decline |
| 3 | 1,114,863,000 | $459,000 | **-58%** | Major decline |
| 4 | 780,118,500 | $321,000 | **-75%** | Major decline |
| 5 | 757,802,200 | $312,000 | **-85%** | Major decline |

**Critical Pattern:** All top 5 TZ01 customers are experiencing major declines between -58% and -89%.

### Extreme Variance Analysis

| Company Code | Variance | Prior Year Sales | Interpretation |
|--------------|----------|------------------|----------------|
| RW01 | +11,897% | 292,500 RWF (~$200) | New customer or data issue |
| UG01 | +6,920% | 22,254 UGX (~$6) | New customer or data issue |
| KE01 | -35,889% | -10,695 KES | **Data quality issue** - negative prior year |
| UG01 | -11,137% | -10,510 UGX | **Data quality issue** - negative prior year |

---

## Risk Assessment

### Focus Area Classification

| Classification | Value | Reasoning |
|----------------|-------|-----------|
| **Focus Area** | BUSINESS_CONTROL | Monitors business performance metrics (sales volume) |
| **Severity** | MEDIUM | Significant variances requiring review but no direct fraud indicators |
| **Risk Score** | 65/100 | High concentration + major customer declines |
| **Fraud Indicator** | **INVESTIGATE** | Extreme variances need validation before ruling out fraud |

### Risk Score Breakdown

| Factor | Score | Reasoning |
|--------|-------|-----------|
| Base (Medium alert) | 60 | Business control monitoring |
| Concentration >50% | +10 | TZ01 at 91.8% |
| Data quality issues | -5 | Negative prior year values indicate data problems |
| **Total** | **65** | |

### Risk Indicators

| Risk Type | Evidence | Recommended Action |
|-----------|----------|-------------------|
| Revenue Loss | Top 5 customers declining 58-89% | Review customer relationships |
| Concentration Risk | 91.8% in single company code | Diversification strategy needed |
| Data Quality | Negative prior year sales values | Data cleansing required |
| Extreme Variance | 11,897% growth likely anomaly | Validate data integrity |

---

## Recommended Actions

### Immediate (24-48 hours)

1. **Review TZ01 top 10 declining customers**
   * Contact sales team for Tanzania region
   * Verify if customer relationships are at risk
   * Check for contract renewals, competitor activity

2. **Validate extreme variance records**
   * RW01: 5 customers with +11,897% variance
   * UG01: Customer with +6,920% variance
   * Confirm if these are new customers or data errors

3. **Investigate data quality issues**
   * KE01: Customer with negative prior year sales
   * UG01: Customer with negative prior year sales
   * Coordinate with finance team for corrections

### Short-term (1-2 weeks)

1. **Customer retention analysis for TZ01**
   * Analyze top 20 declining customers
   * Identify root causes (pricing, service, competition)
   * Develop retention strategy

2. **Sales variance investigation**
   * Compare October 2025 invoicing against contracts
   * Check for delayed billing or timing differences
   * Validate revenue recognition

3. **Cross-company code comparison**
   * Why is KE01 showing average -406% while TZ01 shows +152%?
   * Regional market analysis required

### Process Improvements

1. **Add early warning thresholds** - Alert at -30% variance for key accounts
2. **Quarterly customer review** - Proactive monitoring of top 20 customers per region
3. **Data validation rules** - Prevent negative sales values in transaction figures

---

## Technical Details

### Detection Logic

The ABAP function `ZABC4C_F_SW_10_07_CM_MN_VL_CV` performs:

1. **Parameter extraction**: BACKMONTHS (1), COMPMONTHS (12), DC_IND (D for customer)
2. **Customer selection**: Reads KNA1/KNB1 (customer master) filtered by company code
3. **Transaction figures**: Reads KNC1 table for UMXXU (sales) by fiscal period
4. **Variance calculation**: `PERC_VARI = (UMXXU_TGT / UMXXU_CMP * 100) - 100`
5. **Filtering**: Excludes variances between -50% and +200% (normal range)

### Key Fields

| Field | Table | Description |
|-------|-------|-------------|
| KUNNR | KNA1 | Customer number |
| BUKRS | KNB1 | Company code |
| GJAHR_TGT | Calculated | Target fiscal year (2025) |
| GJAHR_CMP | Calculated | Comparison fiscal year (2024) |
| MONAT_TGT | Calculated | Target period (10 = October) |
| UMXXU_TGT | KNC1 | Current period sales |
| UMXXU_CMP | KNC1 | Prior year period sales |
| PERC_VARI | Calculated | Percentage variance |

### Artifacts Analyzed

| File | Type | Description |
|------|------|-------------|
| Code_Comparison of monthly sales volume by customer_200025_001374.txt | ABAP | Detection logic |
| Metadata_Comparison of monthly sales volume by customer_200025_001374.xlsx | Excel | Alert configuration (4 sheets) |
| Summary_Comparison of monthly sales volume by customer_200025_001374.xlsx | Excel | Alert findings (1,688 records) |
| Explanation_Comparison of monthly sales volume by customer_200025_001374.docx | Word | Business purpose |

### Content Analyzer Output

```json
{
  "alert_id": "200025_001374",
  "alert_name": "Comparison of monthly sales volume by customer",
  "module": "FI",
  "source_system": "PS4",
  "focus_area": "BUSINESS_CONTROL",
  "severity": "MEDIUM",
  "risk_score": 65,
  "fraud_indicator": "INVESTIGATE",
  "records_affected": 211,
  "financial_impact_usd": 15900000,
  "key_findings": {
    "concentration": {
      "entity": "TZ01",
      "percentage": 91.8
    },
    "top_variance": {
      "max_positive": 11896.55,
      "max_negative": -35889.15
    },
    "pattern": "Major customer declines in dominant region"
  },
  "data_quality_issues": [
    "Negative prior year sales values in KE01 and UG01"
  ]
}
```

---

## Exchange Rates Used

| Currency | Rate (1 USD =) | Source |
|----------|---------------|--------|
| TZS | 2,429 | November 2025 |
| KES | 129.24 | November 2025 |
| ZAR | 18.00 | November 2025 |
| UGX | 3,636 | November 2025 |
| NAD | 18.00 | Pegged to ZAR |
| RWF | 1,446 | November 2025 |

---

*Analysis generated: 2025-11-30*
*Analyst: Claude Code*
*Template version: 1.2*
