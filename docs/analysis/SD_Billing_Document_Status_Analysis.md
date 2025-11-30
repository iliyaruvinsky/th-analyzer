# SD Billing Document Status (General) Analysis

> **Alert ID:** 200025_001421 | **Module:** SD | **Analysis Date:** November 2025

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 1,274 billing documents |
| Period | Nov 19-27, 2025 (9 days) |
| Total Value | ~$7.9 million USD |
| Severity | MEDIUM |

## Critical Discovery

**Credit Memo to One-Time Customer:**
• 167.8 million TZS (~$67K USD) credit memo issued to "One time customer for Tanzania"
• Credit memos to unidentified one-time customers are a classic fraud indicator
• Requires immediate investigation: authorization, supporting docs, original invoice

## Concentration Pattern

| Sales Org | Records | % of Value |
|-----------|---------|------------|
| TZ01 (Tanzania) | 336 (26%) | **92%** |
| KE01 (Kenya) | 411 (32%) | 3% |
| SA01 (South Africa) | 314 (25%) | 4% |

All top 10 customers by value are from Tanzania.

---

## Business Context

> **Business Purpose:** SD billing document status (general) monitors billing documents (VBRK) with various status conditions by joining with document status table (VBUK) and filtering on multiple status fields including accounting status (BUCHK), billing block (RFBSK), document category (VBTYP), and other billing attributes, providing visibility into billing document processing states and potential issues.

### What This Alert Monitors

Tracks billing documents from table VBRK joined with VBUK status table, filtering by billing date (FKDAT), and capturing document category, sales organization, payer information, and net value to identify documents requiring status attention.

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Revenue Recognition** | Billing delays affect when revenue can be recognized |
| **Cash Flow** | Unbilled/blocked documents delay collections |
| **Customer Disputes** | Status issues can indicate billing errors or disputes |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| High volume in single org | Large market, seasonal peak | Unusual concentration without explanation |
| Credit memos to named customers | Returns, pricing corrections | Credit memo to one-time/OTC customer |
| Zero-value documents | Internal transfers, sample orders | Large quantities at zero value |

---

## Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| **Alert Instance Name** | SD Billing Document Status (General) |
| **Alert Instance ID** | 200025_001421 |
| **Module** | SD (Sales & Distribution) |
| **Category** | Applications |
| **Subcategory** | SD Alerts |

### Execution Context

| Attribute | Value |
|-----------|-------|
| **Source System** | Production S4 (PS4) |
| **Exception Indicator ID** | SW_10_01_BILL_STAT |
| **Created On** | 26.10.2025 |
| **Collection Mode** | Full |
| **Execution Mode** | On event presence |

### Alert Parameters

| Parameter | Description | Value |
|-----------|-------------|-------|
| BACKDAYS | Lookback period | 1 day |
| DATE_REF_FLD | Reference date field | FKDAT (Billing date) |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Total Documents** | **1,274** |
| **Total Value (Local)** | **5.85 billion** (mixed currencies) |
| **Estimated USD** | **~$7.9 million** |
| **Period** | Nov 19-27, 2025 (9 days) |
| **Severity** | **MEDIUM** |
| **Fraud Indicator** | **INVESTIGATE** |

### What Happened

**1,274 billing documents** were captured across 9 sales organizations over a 9-day period. While this is primarily a general status monitoring alert, analysis revealed a **concentration risk pattern** in Tanzania (TZ01) and a **suspicious credit memo** issued to a one-time customer for **167.8 million TZS (~$67K USD)**.

### Top 3 Findings

1. **One-Time Customer Credit Memo (TZ01):** A single credit memo (ZC02) for **167,779,363 TZS (~$67K USD)** was issued to "One time customer for Tanzania" on Nov 26, 2025. **Credit memos to unidentified one-time customers are a classic fraud indicator.**

2. **Tanzania (TZ01) Concentration:** 26% of documents but **92% of total value**. All top 10 customers by value are from Tanzania. While this may reflect market size, it represents concentration risk.

3. **Credit Memo Volume:** 64 credit memos totaling **227 million TZS (~$91K USD)** in TZ01 alone. 25% of credit memo value went to one-time/OTC customers.

### Immediate Actions

1. **Investigate 167.8M TZS credit memo** - verify authorization, supporting docs, original invoice (Owner: TZ01 Controller)
2. **Review all credit memos to OTC/one-time customers** - validate legitimacy (Owner: Regional Finance)
3. **Verify customer master data for large transactions** - ensure proper customer identification (Owner: Master Data Team)

---

## Key Metrics

### Financial Impact

| Metric | Value |
|--------|-------|
| **Total Value (Local Currencies)** | 5,848,003,316 |
| **Estimated USD Equivalent** | ~$7,937,059 |
| **Largest Single Document** | 167,779,363 TZS ($67K USD) |
| **Average per Document** | ~$6,230 USD |

### Volume

| Metric | Count |
|--------|-------|
| **Total Documents** | 1,274 |
| **Unique Payers** | ~200 |
| **Sales Organizations** | 9 |
| **Credit Memos** | 64 (5%) |

### Patterns

| Pattern | Count | % |
|---------|-------|---|
| Invoices (VBTYP=M) | 1,176 | 92% |
| Credit Memos (VBTYP=O) | 64 | 5% |
| Billing Doc Requests (VBTYP=5) | 27 | 2% |
| Pro Forma (VBTYP=U) | 6 | <1% |
| Other | 1 | <1% |

---

## Concentration Analysis

### By Sales Organization

| Sales Org | Country | Records | % Records | Local Value | ~USD | % Value |
|-----------|---------|---------|-----------|-------------|------|---------|
| **TZ01** | Tanzania | 336 | 26% | 5.39B TZS | $2,156,000 | **92%** |
| KE01 | Kenya | 411 | 32% | 234.8M KES | $1,806,000 | 3% |
| SA01 | South Africa | 314 | 25% | 50.6M ZAR | $2,813,000 | 4% |
| UG01 | Uganda | 121 | 9% | 35.9M UGX | ~$10,000 | <1% |
| Other | Various | 92 | 7% | Mixed | ~$1,152,000 | <1% |

**Flag:** TZ01 has **92% of total value** - extreme concentration.

### By Entity (Top 5 Customers)

| Rank | Customer | Sales Org | Documents | Value (Local) | ~USD |
|------|----------|-----------|-----------|---------------|------|
| 1 | 92 HARDWARE LTD | TZ01 | 7 | 327.9M TZS | $131K |
| 2 | SHANANGA GROUP LIMITED | TZ01 | 7 | 256.8M TZS | $103K |
| 3 | MKAAJUNGU TRADERS LIMITED | TZ01 | 7 | 256.2M TZS | $102K |
| 4 | FMJ HARDWARE LIMITED | TZ01 | 3 | 187.1M TZS | $75K |
| 5 | PRISCUS ALEXANDER CO. LTD | TZ01 | 2 | 183.9M TZS | $74K |

**Note:** All top 5 customers are from Tanzania (TZ01).

### Largest Transactions (Credit Memos - Highest Risk)

| Document | Customer | Type | Value (TZS) | ~USD | Risk |
|----------|----------|------|-------------|------|------|
| (ZC02) | **One time customer for Tanzania** | Credit | 167,779,363 | $67,112 | **CRITICAL** |
| (ZC01) | OFA ENTERPRISES LIMITED | Credit | 13,187,419 | $5,275 | Medium |
| (ZC01) | WEZA ROOFING SOLUTION LTD | Credit | 12,229,824 | $4,892 | Medium |
| (ZC02) | ABUNE COMPANY LIMITED | Credit | 11,059,308 | $4,424 | Medium |
| (ZC01) | OTC Retail Sales for Tanzania | Credit | 6,680,494 | $2,672 | High |

---

## Risk Assessment

### Classification

| Factor | Assessment | Reasoning |
|--------|------------|-----------|
| **Focus Area** | BUSINESS_PROTECTION | Credit memo fraud potential |
| **Severity** | MEDIUM | General monitoring alert, but anomaly found |
| **Risk Score** | 55/100 | Concentration + OTC credit memo |
| **Fraud Indicator** | **INVESTIGATE** | Credit memo to unidentified party |

### Risk Indicators

| Risk Type | Evidence | Recommended Action |
|-----------|----------|-------------------|
| **Potential Fraud** | 167.8M TZS credit to "One time customer" | Verify authorization, supporting docs |
| **Concentration Risk** | 92% of value in TZ01 | Review geographic controls |
| **Process Gap** | Credit memos issued to OTC customers | Add control: require named customer for credits >$10K |

---

## Recommended Actions

### Immediate (24-48 hours)

1. **Investigate 167.8M TZS credit memo**
   - Retrieve original invoice this credit relates to
   - Verify authorization chain
   - Obtain supporting documentation (returns, disputes)

2. **Review all OTC credit memos**
   - List all credit memos to one-time/OTC customers
   - Validate each has proper justification
   - Flag any without supporting documentation

3. **Verify customer master data**
   - Ensure large transactions have proper customer records
   - Convert OTC customers to named customers where appropriate

### Short-term (1-2 weeks)

1. **Implement credit memo controls**
   - Add workflow approval for credit memos >$10K
   - Require named customer (not OTC) for credits >$5K

2. **Review TZ01 concentration**
   - Analyze if concentration reflects market reality
   - Assess credit risk of top customers

3. **Update monitoring thresholds**
   - Add alert for credit memos to OTC customers
   - Add alert for single org >80% of value

### Process Improvements

1. **Credit Memo Policy:** Require named customer in master data for credits >$10K
2. **One-Time Customer Controls:** Add approval workflow for OTC transactions >$50K
3. **Concentration Monitoring:** Add alert threshold when single org exceeds 80% of value

---

## Technical Details

### Source Tables

| Table | Description |
|-------|-------------|
| VBRK | Billing Document Header |
| VBUK | Billing Document Status |
| VBPA | Billing Document Partners |

### Key Fields

| Field | Description | Usage |
|-------|-------------|-------|
| FKART | Billing Type | Invoice vs Credit Memo classification |
| VBTYP | SD Document Category | M=Invoice, O=Credit Memo |
| VKORG | Sales Organization | Regional segmentation |
| NETWR | Net Value | Financial impact |
| KUNRG | Payer | Customer identification |

### Detection Logic Summary

```abap
SELECT * FROM VBRK AS A
  INNER JOIN VBUK AS K ON A~VBELN = K~VBELN
  WHERE A~FKDAT IN R_FKDAT    -- Billing date filter
    AND K~BUCHK IN R_BUCHK    -- Accounting status
    AND K~BLOCK IN R_BLOCK    -- Billing block
    AND A~RFBSK IN R_RFBSK    -- Billing status
```

### Artifacts Analyzed

| File | Purpose |
|------|---------|
| Explanation_*.docx | Business context |
| Metadata_*.xlsx | Alert configuration |
| Summary_*.xlsx | Transaction data (1,274 records) |
| Code_*.txt | ABAP detection logic |

### Exchange Rates Used

| Currency | Rate (per 1 USD) | Date |
|----------|------------------|------|
| TZS | 2,500 | November 2025 |
| KES | 130 | November 2025 |
| ZAR | 18 | November 2025 |

---

*Analysis generated following QUANTITATIVE_ALERT_WORKFLOW.md v1.2 and templates/quantitative-alert.yaml*
