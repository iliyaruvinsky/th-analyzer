# SD Sales Orders with 1M$+ Net Value Analysis

> **Alert ID:** 200025_001435 | **Module:** SD | **Analysis Date:** November 2025

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 20 sales orders |
| Period | Jan - Nov 2025 (365 days) |
| Total Value | ~$28.9 million USD |
| Severity | MEDIUM |

## Critical Discovery

**OTC Retail Sales for Tanzania - $4.45M:**
• 2 orders (7.1B TZS + 4.0B TZS) to generic "OTC Retail Sales" customer
• Both created by same user: RMAGALLAH
• 15% of total value to unidentified customer = fraud risk

## Concentration Pattern

| Customer | Orders | % of Value |
|----------|--------|------------|
| YOUNGMAN SA | 7 | 31% |
| NEWCASTLE STEELWORKS | 5 | 30% |
| OTC Retail Tanzania | 2 | **15%** |
| Others | 6 | 24% |

Single user RMAGALLAH created both high-value orders to unidentified OTC customer.

---

## Business Context

> **Business Purpose:** This alert helps you catch wrong data entry for Sales Orders. All sales documents with Net Value higher than $1M (NETWR_FR > 1,000,000) will be presented, if found. It serves as a data validation control to identify potentially erroneous high-value entries that may indicate keying errors, pricing mistakes, or unusual business transactions requiring management review.

### What This Alert Monitors

Selects sales documents from VBAK where the net value converted to statistics currency (USD) exceeds $1 million. Uses SAP currency conversion function CONVERT_TO_FOREIGN_CURRENCY to translate local currency amounts to USD for consistent comparison across sales organizations.

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Data Entry Errors** | Keying mistakes can create $1M+ orders requiring manual correction |
| **Financial Reporting** | Erroneous high-value orders distort revenue forecasts |
| **Operational Risk** | Incorrect orders may trigger procurement, shipping, and billing issues |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| Large orders to industrial customers | Bulk purchases, project contracts | Same user creating multiple high-value orders to OTC customers |
| High concentration in one sales org | Large regional market | Single user >50% of total value |
| Multiple orders same customer | Long-term contract, blanket orders | Orders to "one-time" or generic customers |

---

## Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| **Alert Instance Name** | Sales Orders with 1M$+ Net Value |
| **Alert Instance ID** | 200025_001435 |
| **Module** | SD (Sales & Distribution) |
| **Category** | Applications |
| **Subcategory** | SD Alerts |

### Execution Context

| Attribute | Value |
|-----------|-------|
| **Source System** | Production S4 (PS4) |
| **Exception Indicator ID** | SW_10_01_ORD_VAL_NEW |
| **Exception Indicator Name** | Exceptional sales documents values – Doc. level |
| **Created On** | 28.10.2025 |
| **Last Updated** | 28.11.2025 |
| **Data Saving** | Cloud |
| **Collection Mode** | Full |
| **Execution Mode** | On event presence |

### Alert Parameters

| Parameter | Description | Value |
|-----------|-------------|-------|
| BACKDAYS | Lookback period | 365 days (1 year) |
| DATE_REF_FLD | Reference date field | ERDAT (Document created) |
| NETWR_FR | Net value threshold in statistics currency | > 1,000,000 |
| VBTYP | SD document category | C (Sales Orders) |
| WAERK_FR | Statistics currency | USD |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Total Sales Orders** | **20** |
| **Total Value (USD)** | **$28,942,346** |
| **Period** | Jan 2025 - Nov 2025 (365 days) |
| **Sales Organizations** | 4 (SA01, TZ01, RW01, UG01) |
| **Severity** | **MEDIUM** |
| **Fraud Indicator** | **INVESTIGATE** |

### What Happened

**20 sales orders** exceeding $1M USD were identified over a 1-year period, totaling **$28.9 million USD**. The majority (16 orders, $22M) are in South Africa (SA01) with legitimate industrial customers. However, **2 orders totaling $4.45M USD** were placed to **"OTC Retail Sales for Tanzania"** - a generic one-time customer - both created by the same user (RMAGALLAH), requiring investigation.

### Top 3 Findings

1. **OTC Customer in Tanzania - $4.45M USD:** Two orders (100380977 and 100396881) totaling **7.1B and 4.0B TZS (~$4.45M USD)** were created for "OTC Retail Sales for Tanzania" by user RMAGALLAH. **High-value orders to unidentified customers are a fraud indicator.**

2. **User Concentration - NNDWANDWE:** Single user created **9 of 20 orders (45%)** totaling **$11.4M USD** - primarily for YOUNGMAN SA. While this may reflect assigned customer responsibility, it represents concentration risk.

3. **Rwanda Project Order - $1.41M USD:** Order 100427664 for "CHINA CIVIL ENGINEERING CONSTRUCTION" in RW01 totals **1.69B RWF ($1.41M USD)**. Large infrastructure project - verify contract documentation.

### Immediate Actions

1. **Investigate OTC Tanzania orders** - verify authorization, customer identity, contract documentation for $4.45M (Owner: TZ01 Sales Manager)
2. **Review RMAGALLAH transactions** - same user created both OTC orders - verify authorization level (Owner: Line Manager)
3. **Confirm Rwanda project contract** - verify documentation for $1.41M China Civil Engineering order (Owner: RW01 Controller)

---

## Key Metrics

### Financial Impact

| Metric | Value |
|--------|-------|
| **Total Value (USD)** | $28,942,346 |
| **Largest Single Order** | $2,840,000 (7.1B TZS - OTC Tanzania) |
| **Average per Order** | $1,447,117 |
| **Minimum Order** | $980,306 (17.6M ZAR) |

### Volume

| Metric | Count |
|--------|-------|
| **Total Sales Orders** | 20 |
| **Unique Customers** | 7 |
| **Unique Users (Creators)** | 6 |
| **Sales Organizations** | 4 |

### Patterns

| Currency | Orders | Local Value | USD Equivalent | % of Total |
|----------|--------|-------------|----------------|------------|
| ZAR (South Africa) | 16 | 396,748,323 | $22,041,573 | 76% |
| TZS (Tanzania) | 2 | 11,115,000,000 | $4,446,000 | 15% |
| RWF (Rwanda) | 1 | 1,689,287,280 | $1,407,739 | 5% |
| USD (Uganda) | 1 | 1,047,033 | $1,047,033 | 4% |

---

## Concentration Analysis

### By Sales Organization

| Sales Org | Country | Orders | Local Value | USD | % |
|-----------|---------|--------|-------------|-----|---|
| **SA01** | South Africa | 16 | 396.7M ZAR | $22,041,573 | **76%** |
| TZ01 | Tanzania | 2 | 11.1B TZS | $4,446,000 | 15% |
| RW01 | Rwanda | 1 | 1.69B RWF | $1,407,739 | 5% |
| UG01 | Uganda | 1 | 1.05M USD | $1,047,033 | 4% |

**Note:** SA01 represents 76% of total value with legitimate industrial customers.

### By Entity (Customer)

| Rank | Customer | Sales Org | Orders | USD Value | % |
|------|----------|-----------|--------|-----------|---|
| 1 | YOUNGMAN SA (PTY) LTD | SA01 | 7 | $8,852,579 | 31% |
| 2 | NEWCASTLE STEELWORKS (PTY) LTD | SA01 | 5 | $8,691,056 | 30% |
| 3 | **OTC Retail Sales for Tanzania** | TZ01 | 2 | $4,446,000 | **15%** |
| 4 | PRO ROOF STEEL AND TUBE PTY LTD | SA01 | 2 | $2,529,462 | 9% |
| 5 | ROOFCO STEEL | SA01 | 2 | $1,969,250 | 7% |
| 6 | CHINA CIVIL ENGINEERING CONSTRUCTIO | RW01 | 1 | $1,407,739 | 5% |
| 7 | KAMBERE MULIMIRWA SAMUEL | UG01 | 1 | $1,047,033 | 4% |

**Flag:** "OTC Retail Sales for Tanzania" is a generic customer with **$4.45M (15%)** - requires investigation.

### By User (Document Creator)

| User ID | Orders | USD Value | % | Primary Customer |
|---------|--------|-----------|---|------------------|
| **NNDWANDWE** | 9 | $11,381,268 | 39% | YOUNGMAN SA |
| **LMAJIKIJELA** | 5 | $8,691,056 | 30% | NEWCASTLE STEELWORKS |
| **RMAGALLAH** | 2 | $4,446,000 | 15% | **OTC Tanzania** |
| AKUSELO | 2 | $1,969,250 | 7% | ROOFCO STEEL |
| LSHEMA | 1 | $1,407,739 | 5% | CHINA CIVIL ENG |
| MNAKENDO | 1 | $1,047,033 | 4% | KAMBERE MULIMIRWA |

**Flag:** RMAGALLAH created both OTC Tanzania orders totaling $4.45M to generic customer.

### Largest Transactions

| Order | Customer | Created By | Local Value | Currency | USD | Risk |
|-------|----------|------------|-------------|----------|-----|------|
| 100396881 | **OTC Retail Sales for Tanzania** | RMAGALLAH | 7,100,000,000 | TZS | $2,840,000 | **HIGH** |
| 100429157 | NEWCASTLE STEELWORKS | LMAJIKIJELA | 47,150,000 | ZAR | $2,619,444 | Low |
| 100429164 | NEWCASTLE STEELWORKS | LMAJIKIJELA | 38,100,000 | ZAR | $2,116,667 | Low |
| 100450652 | YOUNGMAN SA | NNDWANDWE | 30,681,675 | ZAR | $1,704,538 | Low |
| 100380977 | **OTC Retail Sales for Tanzania** | RMAGALLAH | 4,015,000,000 | TZS | $1,606,000 | **HIGH** |

---

## Risk Assessment

### Classification

| Factor | Assessment | Reasoning |
|--------|------------|-----------|
| **Focus Area** | BUSINESS_CONTROL | Data validation/entry control |
| **Severity** | MEDIUM | Most orders appear legitimate; 2 OTC orders require investigation |
| **Risk Score** | 50/100 | 15% of value to generic OTC customer |
| **Fraud Indicator** | **INVESTIGATE** | $4.45M to unidentified OTC customer, single user |

### Risk Indicators

| Risk Type | Evidence | Recommended Action |
|-----------|----------|-------------------|
| **High-Value OTC Orders** | $4.45M to "OTC Retail Sales for Tanzania" | Verify customer identity, contract documentation |
| **User Concentration** | RMAGALLAH: 100% of OTC orders | Review user authorization for high-value orders |
| **Generic Customer** | No specific customer master data | Convert to named customer or reject order |
| **Single Point of Failure** | NNDWANDWE: 39% of total value | Ensure proper authorization levels |

---

## Recommended Actions

### Immediate (24-48 hours)

1. **Investigate OTC Tanzania orders (CRITICAL)**
   - Order 100396881: 7.1B TZS - verify customer identity and contract
   - Order 100380977: 4.0B TZS - verify authorization and supporting documentation
   - Interview user RMAGALLAH - understand transaction rationale

2. **Verify Rwanda project documentation**
   - Order 100427664: 1.69B RWF for China Civil Engineering
   - Confirm project contract and payment terms
   - Verify customer creditworthiness

3. **Review high-value order authorization**
   - Confirm all orders >$1M have proper approval documentation
   - Verify user authorization levels for high-value transactions

### Short-term (1-2 weeks)

1. **Implement OTC controls for high-value orders**
   - Add approval workflow for orders >$500K to OTC/generic customers
   - Require named customer master data for orders >$1M

2. **Review user authorization levels**
   - Verify RMAGALLAH, NNDWANDWE, LMAJIKIJELA have appropriate limits
   - Document authorization matrix for high-value orders

3. **Customer master data cleanup**
   - Convert OTC customers with repeat high-value orders to named customers
   - Ensure proper credit limits and payment terms

### Process Improvements

1. **Order Value Threshold:** Add hard stop requiring manager approval for orders >$1M
2. **OTC Customer Controls:** Prohibit OTC customers for orders >$500K without exception approval
3. **Dual Authorization:** Require two approvers for orders >$2M

---

## Technical Details

### Source Tables

| Table | Description |
|-------|-------------|
| VBAK | Sales Document Header |
| VBPA | Sales Document Partners |

### Key Fields

| Field | Description | Usage |
|-------|-------------|-------|
| NETWR | Net value (local currency) | Original order value |
| NETWR_FR | Net value (statistics currency) | USD converted value for threshold |
| WAERK | Document currency | Local currency code |
| WAERK_FR | Statistics currency | USD for comparison |
| KUNNR | Sold-to party | Customer identification |
| VKORG | Sales organization | Regional segmentation |

### Detection Logic

```abap
SELECT * FROM VBAK
  WHERE VBELN IN R_VBELN
    AND VKORG IN R_VKORG
    AND VBTYP IN R_VBTYP        -- C = Sales Orders
    AND ERDAT IN R_ERDAT        -- Created date filter
DELETE T_DATA WHERE NETWR NOT IN R_NETWR
-- Currency conversion
CALL FUNCTION 'CONVERT_TO_FOREIGN_CURRENCY'
DELETE T_DATA WHERE NETWR_FR NOT IN R_NETWR_FR  -- > 1,000,000 USD
```

### Artifacts Analyzed

| File | Purpose |
|------|---------|
| Explanation_*.html | Business context - data validation purpose |
| Metadata_*.xlsx | Alert configuration - 365 day lookback, >$1M USD |
| Summary_*.xlsx | Transaction data (20 orders) |
| Code_*.txt | ABAP detection logic with currency conversion |

### Exchange Rates Used

| Currency | Rate (per 1 USD) | Date |
|----------|------------------|------|
| ZAR | 18 | November 2025 |
| TZS | 2,500 | November 2025 |
| RWF | 1,200 | November 2025 |
| USD | 1 | Base currency |

---

*Analysis generated following QUANTITATIVE_ALERT_WORKFLOW.md v1.2 and templates/quantitative-alert.yaml*
