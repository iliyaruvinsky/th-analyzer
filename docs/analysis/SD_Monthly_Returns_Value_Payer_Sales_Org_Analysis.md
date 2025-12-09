# Analysis: Monthly Returns Value by Payer and Sales Organization

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 206 return documents across 7 customers |
| Period | January 2025 - December 2025 (12 months) |
| Total Value | **$1,131,679 USD** (aggregated monthly returns > $100K) |
| Severity | **MEDIUM** |

### Critical Discovery

**OTC Retail Sales Account with Extreme Return Volume:**
* Customer 3999999 "OTC Retail Sales for Kenya" has 153 return documents (74% of all returns)
* Generic one-time customer accounts with high return volumes are a classic fraud indicator
* Requires immediate investigation: Who is processing these returns? What products? Why through OTC account?

### Concentration Pattern

| Customer | Returns | % of Value | Sales Org |
|----------|---------|------------|-----------|
| CHARTWELL ROOFING CAPE PTY LTD | 7 | **21.9%** | SA02 |
| OTC Retail Sales for Kenya | 153 | 15.2% | KE01 |
| SCHELTEMA AND COMPANY PTY LTD | 14 | 14.0% | SA02 |
| GLOBAL ROOFING SOLUTIONS PTY LTD | 7 | 13.5% | SA01 |

Distribution is relatively even across top customers, but OTC account volume is suspicious.

---

## Business Context

> **Business Purpose:** This alert detects payers with Total (aggregated) Net Value of returns exceeding a defined threshold (e.g., more than $100,000 USD) per sales organization. High volume of returns can indicate fraud behavior, product quality issues, or process manipulation.

### What This Alert Monitors

Aggregates SD return documents (VBTYP = H) by customer (KUNNR) and sales organization (VKORG) on a monthly basis, flagging any customer-month combination exceeding $100,000 USD in return value.

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| Fraud | Fictitious returns to extract cash or inventory |
| Revenue Leakage | Unauthorized credits eroding profit margins |
| Process Gap | Returns without proper approval or documentation |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|-----------------|----------|
| High return value | Large customer, seasonal patterns | Concentrated in one customer/user |
| OTC customer returns | Walk-in customer corrections | High volume through generic account |
| Multiple small returns | Normal business | Structured to avoid thresholds |

---

## Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| Alert Name | Monthly returns value by Payer and Sales organization |
| Alert ID | 200025_001455 |
| Module | SD |
| Category | Applications |
| Subcategory | SD Alerts |

### Execution Context

| Attribute | Value |
|-----------|-------|
| Source System | **Production S4 (PS4)** |
| Created On | 02.12.2025 at 13:38 by ILIYAR |
| Last Executed | 02.12.2025 at 20:25 |
| Exception Indicator ID | SW_10_01_ORD_VAL_TOT |

### Alert Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| AGGR_FIELDS | KUNNR, VKORG | Aggregate by Customer + Sales Org |
| AGGR_PERIOD | M | Monthly aggregation |
| BACKDAYS | 365 | Last 365 days of data |
| BP1_FUNCT | SP | Sold-to Party function |
| DATE_REF_FLD | VDATU | Requested delivery date |
| TOT_NETWR_FR | > 100,000 | Flag monthly totals > $100K USD |
| VBTYP | H | Returns documents only |
| WAERK_FR | USD | Convert all to USD |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Total Returns Flagged** | **$1,131,679 USD** |
| **Customers Flagged** | 7 customers with monthly returns > $100K |
| **Severity** | **MEDIUM** |
| **Fraud Indicator** | **INVESTIGATE** - OTC account with 153 returns requires review |

### What Happened

Over the past 12 months, 7 customers across 3 sales organizations (KE01, SA01, SA02) had monthly return values exceeding $100,000 USD. The most concerning finding is customer 3999999 "OTC Retail Sales for Kenya" which processed 153 return documents through a generic one-time customer account - this pattern is a classic indicator of potential return fraud.

### Top 3 Findings

1. **OTC Account Return Volume** - Customer 3999999 has 153 returns (74% of total) through a generic "OTC Retail Sales" account - investigate who is processing these and why
2. **South Africa Concentration** - SA02 has 3 customers totaling $558K (49% of returns) - review return authorization process
3. **CHARTWELL Highest Value** - Single customer with $248K in returns (21.9%) - verify product quality or contract issues

### Immediate Actions

1. **Audit OTC Retail Sales returns (3999999)** - Review all 153 return documents, identify users, verify supporting documentation
2. **Review SA02 return authorization** - Check if proper approvals exist for the 3 flagged customers
3. **Validate return reasons** - Ensure all returns have valid reason codes and supporting evidence

---

## Key Metrics

### Financial Impact

| Currency | Sales Org | Local Amount | USD Equivalent |
|----------|-----------|--------------|----------------|
| KES | KE01 | 38,566,798 | $297,652 |
| ZAR | SA01 | 4,719,248 | $275,657 |
| ZAR | SA02 | 9,559,289 | $558,370 |
| **Total** | | | **$1,131,679** |

*Exchange rates: KES 129.5/USD, ZAR 17.12/USD (December 2025)*

### Volume

| Metric | Count |
|--------|-------|
| Return Documents | 206 |
| Unique Customers | 7 |
| Sales Organizations | 3 |
| Months Covered | 12 (Jan-Dec 2025) |

### Return Document Types

| Type | Count | % |
|------|-------|---|
| ZR03 | 155 | 75% |
| ZR02 | 38 | 18% |
| ZR01 | 13 | 6% |

---

## Concentration Analysis

### By Sales Organization

| Rank | Sales Org | Country | Customers | Return Docs | Total USD | % of Total |
|------|-----------|---------|-----------|-------------|-----------|------------|
| 1 | SA02 | South Africa | 3 | 23 | $558,370 | **49.3%** |
| 2 | KE01 | Kenya | 2 | 170 | $297,652 | 26.3% |
| 3 | SA01 | South Africa | 2 | 13 | $275,657 | 24.4% |

**Observation:** SA02 has 49.3% of value but only 23 documents - high-value returns. KE01 has 170 documents (83% of volume) but only 26% of value - high-volume, lower-value returns.

### By Customer

| Rank | Customer | Name | Sales Org | USD Value | Return Docs | % of Total |
|------|----------|------|-----------|-----------|-------------|------------|
| 1 | 2008812 | CHARTWELL ROOFING CAPE PTY LTD | SA02 | $248,044 | 7 | **21.9%** |
| 2 | 3999999 | OTC Retail Sales for Kenya | KE01 | $172,031 | **153** | 15.2% |
| 3 | 2009390 | SCHELTEMA AND COMPANY PTY LTD | SA02 | $158,991 | 14 | 14.0% |
| 4 | 2009866 | GLOBAL ROOFING SOLUTIONS PTY LTD | SA01 | $152,564 | 7 | 13.5% |
| 5 | 2009493 | PREMIER ROOFING AND CLADDING | SA02 | $151,334 | 2 | 13.4% |
| 6 | 2011059 | ALIASGER ENTERPRISES | KE01 | $125,621 | 17 | 11.1% |
| 7 | 2001118 | MACSTEEL SERVICES CENTRES SA PTY | SA01 | $123,093 | 6 | 10.9% |

### Anomaly: OTC Retail Sales Account

| Metric | Value | Concern |
|--------|-------|---------|
| Customer Number | 3999999 | Generic OTC customer code |
| Customer Name | OTC Retail Sales for Kenya | One-time customer account |
| Return Documents | 153 | **74% of all return documents** |
| Return Value | $172,031 | 15% of total value |
| Avg Return Value | $1,124 | Low individual amounts |

**Red Flag:** Using a generic OTC account for 153 returns over 12 months is unusual. This could indicate:
- Structuring returns through generic account to avoid customer-specific scrutiny
- Processing fictitious returns
- Lack of proper customer master data management

---

## Risk Assessment

### Focus Area Classification

| Classification | Value | Reasoning |
|----------------|-------|-----------|
| **Focus Area** | BUSINESS_PROTECTION | Returns fraud detection |
| **Severity** | MEDIUM | Significant volume but amounts are moderate |
| **Risk Score** | 68/100 | OTC account pattern + geographic spread |
| **Fraud Indicator** | **INVESTIGATE** | OTC account with 153 returns is suspicious |

### Risk Score Breakdown

| Factor | Score | Reasoning |
|--------|-------|-----------|
| Base (Returns monitoring) | 60 | Business protection alert |
| OTC Account Pattern | +10 | 153 returns through generic account |
| Volume Concentration | +5 | 74% of docs in one account |
| No single customer >50% | -7 | Distribution is relatively even |
| **Total** | **68** | |

### Risk Indicators

| Risk Type | Evidence | Recommended Action |
|-----------|----------|-------------------|
| Potential Fraud | 153 returns via OTC account | Audit all OTC returns |
| Process Gap | High return volume per customer | Review authorization workflow |
| Concentration | 49% value in SA02 | Regional process review |

---

## Recommended Actions

### Immediate (24-48 hours)

1. **Audit OTC Retail Sales returns**
   - Pull all 153 return documents for customer 3999999
   - Identify which users processed these returns
   - Verify each return has proper authorization and supporting documentation
   - Check if physical goods were actually returned to inventory

2. **Validate SA02 high-value returns**
   - Review the 7 CHARTWELL returns totaling $248K
   - Confirm product quality issues or contract terms justify returns
   - Verify credit memos were properly approved

3. **User access review**
   - Identify users with authority to process returns
   - Check for SoD conflicts (same user sells and processes returns)

### Short-term (1-2 weeks)

1. **OTC Account Policy Review**
   - Determine if OTC accounts should be used for returns
   - Consider blocking returns to generic customer accounts
   - Implement mandatory customer creation before return processing

2. **Return Reason Analysis**
   - Analyze reason codes for all 206 returns
   - Identify patterns (product defects, pricing errors, customer changes)
   - Compare return rates to industry benchmarks

3. **Geographic Comparison**
   - Compare Kenya vs South Africa return rates
   - Investigate why KE01 has 170 returns (83% of volume)
   - Assess if this reflects legitimate business or process issues

### Process Improvements

1. **Return threshold alerts** - Add real-time alerts for individual returns > $10K
2. **OTC return blocking** - Require named customer for all return transactions
3. **Dual approval** - Require second approver for returns > $25K

---

## Technical Details

### Detection Logic

The ABAP function `/SKN/F_SW_10_01_ORD_VAL_TOT` performs:

1. **Parameter extraction**: AGGR_PERIOD (M), BACKDAYS (365), aggregation fields
2. **Data retrieval**: Calls `/SKN/F_SW_10_01_ORD_VAL_NEW` for detail data
3. **Period calculation**: Groups by month using delivery date (VDATU)
4. **Aggregation**: Sums NETWR by customer + sales org + month
5. **Currency conversion**: Converts to USD using WAERK_FR
6. **Filtering**: Returns only aggregations > 100,000 USD

### Key Fields

| Field | Table | Description |
|-------|-------|-------------|
| VBELN | VBAK | Sales Document (Return Order) |
| KUNNR | VBAK | Sold-to Party |
| VKORG | VBAK | Sales Organization |
| VBTYP | VBAK | Document Category (H = Returns) |
| NETWR | VBAP | Net Value per item |
| TOT_NETWR_FR | Calculated | Aggregated monthly total in USD |

### Artifacts Analyzed

| File | Type | Description |
|------|------|-------------|
| Code_Monthly returns value by Payer...txt | ABAP | Aggregation logic |
| Metadata_Monthly returns value...xlsx | Excel | Alert configuration (4 sheets) |
| Summary_Monthly returns value...xlsx | Excel | 206 return records |
| Explanation_Monthly returns value...docx | Word | Business purpose |

### Content Analyzer Output

```json
{
  "alert_id": "200025_001455",
  "alert_name": "Monthly returns value by Payer and Sales organization",
  "module": "SD",
  "source_system": "PS4",
  "focus_area": "BUSINESS_PROTECTION",
  "severity": "MEDIUM",
  "risk_score": 68,
  "fraud_indicator": "INVESTIGATE",
  "records_affected": 206,
  "unique_customers": 7,
  "financial_impact_usd": 1131679,
  "key_findings": {
    "otc_account_anomaly": {
      "customer": "3999999",
      "name": "OTC Retail Sales for Kenya",
      "return_docs": 153,
      "percentage_of_volume": 74
    },
    "concentration": {
      "top_customer": "CHARTWELL ROOFING CAPE PTY LTD",
      "percentage": 21.9
    }
  },
  "currencies": ["KES", "ZAR"],
  "sales_orgs": ["KE01", "SA01", "SA02"]
}
```

---

## Exchange Rates Used

| Currency | Rate (1 USD =) | Source |
|----------|---------------|--------|
| KES | 129.50 | December 2025 |
| ZAR | 17.12 | December 2025 |

---

*Analysis generated: 2025-12-02*
*Analyst: Claude Code*
*Template version: 1.2*
