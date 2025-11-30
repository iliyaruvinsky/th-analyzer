# Exceptional Posting by GL Account - Alert Analysis

> **Alert ID:** 200025_001359 | **Module:** FI | **Analysis Date:** November 2025

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 521 line items |
| Period | 3 days (BACKDAYS parameter) |
| Total Amount | ~$736.9 million USD |
| Severity | HIGH |

## Critical Discovery

**JKOCK - $11.5M Average Per Posting:**
• 12 postings totaling $138.6M (19% of total)
• $11.55M average vs ~$1M average for other users
• Single user with 10x higher transaction values = control bypass risk

## Concentration Pattern

| User | Records | Avg/Record |
|------|---------|------------|
| WCHIGWADA | 82 | $1.81M |
| JKOCK | 12 | **$11.55M** |
| ASAM | 70 | $1.17M |

$82.5M posted to GRIR Clearing account (170002100) requires GR/IR reconciliation review.

---

## Business Context

> **Business Purpose:** This alert monitors high-value financial postings to General Ledger accounts to identify transactions that may require additional scrutiny. It helps finance controllers and auditors detect potential accounting errors, unauthorized transactions, or control bypasses where users may be posting amounts that exceed their authorization limits. Large GL postings can significantly impact financial statements and require proper approval chains.

### What This Alert Monitors

**High-Value GL Postings** - Detects postings to General Ledger accounts that exceed predefined amount thresholds (LC2 > $500K), flagging unusual transaction activity that may indicate errors, fraud, or process issues.

### Why It Matters

| Risk Type | Business Impact |
|-----------|--------------------|
| **Accounting Errors** | Large mispostings affect financial statements |
| **Fraud Risk** | Unauthorized high-value transactions |
| **Control Bypass** | Transactions exceeding approval limits |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| High-value bank transfers | Month-end settlements, treasury operations | Unexpected timing, unknown counterparty |
| GRIR clearing postings | Normal procurement cycle | Long-outstanding items, concentration |
| Single user high volume | Authorized batch processor | Manual postings without approval chain |

---

## EXECUTIVE SUMMARY

### Alert Identity

| | |
|---|---|
| **Alert Name** | Exceptional posting by GL account |
| **Alert ID** | 200025_001359 |
| **Module** | FI (Finance - General Ledger) |
| **Category** | Applications |
| **Subcategory** | FI Alerts |

### Execution Context

| | |
|---|---|
| **Source System** | Production S4 (PS4) |
| **Created** | 18.06.2025 at 13:40 by SKYWATCH |
| **Last Updated** | 23.10.2025 at 11:08 by SKYWATCH |
| **Exception Indicator** | SW_10_07_FI_EXC_POST |

### Alert Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| BACKDAYS | 3 | Data from past 3 days |
| DMBE2 | > 500,000 | LC2 Amount (USD) exceeding $500K threshold |

### THE BOTTOM LINE

| | |
|---|---|
| **Total Amount (USD)** | **$736,880,005** |
| **Records Affected** | 521 line items across 97 documents |
| **Severity** | HIGH |
| **Fraud Indicator** | INVESTIGATE - Concentration patterns detected |

### WHAT HAPPENED

521 GL postings exceeding $500K threshold totaling $736.9M in 3 days. Single user (JKOCK) posted $138.6M across only 12 records ($11.5M average per posting). GRIR clearing account (170002100) shows $82.5M requiring goods receipt reconciliation.

### TOP 3 FINDINGS

1. **JKOCK - $138.6M in 12 postings** - $11.5M average per transaction - **REVIEW IMMEDIATELY**
2. **GRIR Clearing (170002100)**: $82.5M across 82 records - requires GR/IR reconciliation
3. **SA01 concentration**: 40% of total amount ($295.8M) in one company code

### IMMEDIATE ACTIONS REQUIRED

1. **URGENT**: Review JKOCK's 12 high-value postings (avg $11.5M each)
2. Investigate GRIR clearing account reconciliation status
3. Verify authorization levels for users posting >$10M transactions

---

## KEY METRICS

### Financial Impact

| Metric | Value |
|--------|-------|
| Total Amount (LC2/USD) | $736,880,005 |
| Maximum Single Posting | $11,546,744 |
| Average Per Posting | $1,414,357 |
| Currency | USD (LC2) |

### Volume

| Metric | Value |
|--------|-------|
| Line Items | 521 |
| Documents | 97 |
| Unique Users | 18 |
| Company Codes | 7 |
| GL Accounts | 34 |

### Patterns

| Pattern | Count | % |
|---------|-------|---|
| Debit Postings (SHKZG=S) | ~260 | 50% |
| Credit Postings (SHKZG=H) | ~261 | 50% |
| Bank Interim Accounts | 96 | 18% |
| GRIR/Clearing Accounts | 82 | 16% |

---

## CONCENTRATION ANALYSIS

### By Company Code

| Rank | Company | Amount (USD) | Records | % of Total |
|------|---------|--------------|---------|------------|
| 1 | **SA01** (Safal Steel) | **$295,768,300** | 131 | **40%** |
| 2 | TZ01 (ALAF Limited) | $161,967,300 | 170 | 22% |
| 3 | SA04 | $113,621,100 | 52 | 15% |
| 4 | KE01 (Mabati Rolling Mills) | $108,469,400 | 114 | 15% |
| 5 | SA02 | $34,862,710 | 30 | 5% |
| 6 | UG01 (Uganda Baati) | $18,449,940 | 18 | 2% |
| 7 | ZM01 (Zambia) | $3,741,398 | 6 | <1% |

**Insight**: SA01 has 40% concentration - elevated but within normal range for large entity.

### By User (Top 10)

| Rank | User | Name | Amount (USD) | Records | Avg/Record |
|------|------|------|--------------|---------|------------|
| 1 | **WCHIGWADA** | Vimbai Chigwada | **$148,483,800** | 82 | $1.81M |
| 2 | **JKOCK** | Jennifer Kock | **$138,560,900** | 12 | **$11.55M** |
| 3 | ASAM | Allen Sam | $81,698,520 | 70 | $1.17M |
| 4 | JOBUSER | (System) | $57,684,630 | 52 | $1.11M |
| 5 | JGOVENDER | J. Govender | $52,886,520 | 25 | $2.12M |
| 6 | GVUMU | G. Vumu | $39,639,660 | 48 | $0.83M |
| 7 | LMLEMBE | L. Mlembe | $39,368,380 | 42 | $0.94M |
| 8 | PAMUDAVI | P. Amudavi | $24,525,590 | 24 | $1.02M |
| 9 | JWAHOME | J. Wahome | $22,823,260 | 21 | $1.09M |
| 10 | DNJAU | D. Njau | $17,929,190 | 18 | $1.00M |

**Critical**: JKOCK has **$11.55M average per posting** - significantly higher than other users (~$1M average).

### By GL Account (Top 10)

| Rank | GL Account | Description | Amount (USD) | Records |
|------|------------|-------------|--------------|---------|
| 1 | **170002100** | GRIR Clearing | **$82,455,047** | 82 |
| 2 | 330000100 | Debtors - Domestic | $71,774,728 | 10 |
| 3 | 600001000 | (Cost Account) | $69,280,463 | 6 |
| 4 | 371041001 | Standard Chartered Bank Interim SA01 | $51,454,029 | 37 |
| 5 | 180000200 | Creditors - Import | $43,261,559 | 18 |
| 6 | 371041002 | Standard Chartered Bank Interim | $30,244,491 | 30 |
| 7 | 433000300 | (Expense Account) | $28,740,331 | 9 |
| 8 | 320001600 | (Liability Account) | $23,809,197 | 25 |
| 9 | 180000100 | Creditors - Import Raw Materials | $21,773,470 | 11 |
| 10 | 370941015 | Bank Account | $20,690,319 | 14 |

**Insight**: GRIR Clearing (170002100) dominates with $82.5M - requires reconciliation review.

### Largest Single Transactions

| Amount (USD) | User | GL Account | Description | Company |
|--------------|------|------------|-------------|---------|
| **$11,546,744** | JKOCK | 330000100 | Debtors - Domestic | SA01 |
| $3,867,403 | WCHIGWADA | 340000100 | Debtors - Related Party | SA04 |
| $2,595,384 | ASAM | 371041001 | Bank Interim | SA01 |
| $2,209,945 | WCHIGWADA | 340000100 | Debtors - Related Party | SA04 |
| $1,340,609 | ASAM | 371041001 | Bank Interim | SA01 |

---

## RISK ASSESSMENT

### Classification

| Attribute | Value | Reasoning |
|-----------|-------|-----------|
| Focus Area | BUSINESS_CONTROL | Financial posting controls and authorization |
| Severity | HIGH | Large amounts, user concentration pattern |
| Risk Score | 70/100 | High volume and value, concentration detected |
| Fraud Indicator | INVESTIGATE | JKOCK's unusual posting pattern requires review |

### Risk Indicators

| Risk | Evidence | Action |
|------|----------|--------|
| **User Concentration** | JKOCK: $11.5M avg vs $1M for others | Review authorization matrix |
| **Account Concentration** | GRIR at $82.5M | Verify GR/IR reconciliation |
| **High-Value Postings** | 12 postings by one user = $138.6M | Audit approval workflow |
| **Entity Concentration** | SA01 at 40% | Normal for size, monitor |

---

## RECOMMENDED ACTIONS

### Immediate (24-48 hours)

1. **Review JKOCK's 12 postings**
   - Verify supporting documentation
   - Check approval chain and authorization level
   - Confirm transaction legitimacy

2. **GRIR Clearing Account Review**
   - Check $82.5M for aged items
   - Identify goods receipts without invoices
   - Validate matching status

3. **Authorization Level Audit**
   - Verify users have appropriate posting limits
   - Check if $11M+ postings require dual approval

### Short-term (1-2 weeks)

4. **User Access Review**
   - Review posting authority for high-value GL accounts
   - Implement segregation for critical accounts

5. **Bank Account Reconciliation**
   - $81.7M in bank interim accounts (371041001/002)
   - Verify clearing status

6. **Related Party Transactions**
   - $113.6M to SA04 (related party accounts)
   - Ensure proper disclosure

### Process Improvements

7. **Implement tiered approval** for postings >$5M
8. **Add real-time alerts** for single postings >$10M
9. **Automated GRIR aging report** for items >30 days

---

## DETECTION LOGIC

**What the alert detects**: GL account postings where LC2 amount exceeds threshold

```
BSEG-DMBE2 > 500,000 (configured threshold)
BACKDAYS = 3 (look back 3 days from CPUDT)
```

**Data Sources**:
- BKPF: Document Header
- BSIS: GL Account Line Items (Open)
- BSAS: GL Account Line Items (Cleared)
- SKA1: GL Account Master
- T001: Company Code

---

## ARTIFACTS ANALYZED

| Artifact | File |
|----------|------|
| Code | `Code_Exceptional posting by GL account_200025_001359.txt` |
| Summary | `Summary_Exceptional posting by GL account_200025_001359.xlsx` |
| Explanation | `Explanation_Exceptional posting by GL account_200025_001359.docx` |
| Metadata | `Metadata _Exceptional posting by GL account_200025_001359.xlsx` |

**Location**: `docs/skywind-4c-alerts-output/Applications/FI/200025_001359 - Exceptional posting by GL account/`

---

## CONTENT ANALYZER OUTPUT

```json
{
  "alert_id": "200025_001359",
  "alert_name": "Exceptional posting by GL account",
  "module": "FI",
  "classification": {
    "focus_area": "BUSINESS_CONTROL",
    "severity": "HIGH",
    "risk_score": 70,
    "fraud_indicator": "INVESTIGATE"
  },
  "metrics": {
    "record_count": 521,
    "document_count": 97,
    "total_amount_usd": 736880005,
    "max_single_amount": 11546744,
    "currency": "USD"
  },
  "concentration": {
    "top_company": {"code": "SA01", "amount": 295768300, "pct": 40},
    "top_user": {"name": "WCHIGWADA", "amount": 148483800, "records": 82},
    "highest_avg_user": {"name": "JKOCK", "avg_per_record": 11546743}
  },
  "key_finding": "521 GL postings totaling $736.9M. JKOCK posted $138.6M in only 12 transactions ($11.5M avg) - requires immediate review. GRIR clearing shows $82.5M pending reconciliation.",
  "recommended_actions": [
    "Review JKOCK's 12 high-value postings",
    "Audit GRIR clearing account reconciliation",
    "Verify authorization levels for >$10M postings"
  ]
}
```

---

*Analysis Date: 2025-11-27 | Template Version: 1.0*
