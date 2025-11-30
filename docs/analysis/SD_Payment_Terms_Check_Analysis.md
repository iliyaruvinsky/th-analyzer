# SD Sales Document Payment Terms Check Analysis

> **Alert ID:** 200025_001443 | **Module:** SD | **Analysis Date:** November 2025

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 6 unique documents |
| Period | Nov 19-26, 2025 (1 week) |
| Total Value | ~$35,400 USD (637,071 ZAR) |
| Severity | HIGH |

## Critical Discovery

**ROOFCO STEEL - Cash to Credit Override:**
• 2 orders totaling 600,748 ZAR ($33K USD)
• Payment terms changed from C100 (Cash) to SD07 (7-day credit)
• Cash to credit conversion bypasses credit approval process

## Concentration Pattern

| Customer | Documents | Override Type |
|----------|-----------|---------------|
| ROOFCO STEEL | 2 | **C100→SD07** |
| SPAR locations | 3 | SD07→SD05 |

User PMOKGOKO created 50% of all payment term overrides in this period.

---

## Business Context

> **Business Purpose:** Sales document payment terms check identifies sales orders where payment terms entered on the sales document (VBKD-ZTERM) differ from customer sales area master data (KNVV-ZTERM), detected by joining VBAK with VBKD, VBPA (payer PARVW='RG'), and KNVV then comparing ZTERM fields, indicating unauthorized payment term overrides during order entry.

### What This Alert Monitors

Compares the payment terms on sales documents (VBKD-ZTERM) against the customer's established payment terms in master data (KNVV-ZTERM). Triggers when these values do not match, indicating a user manually overrode the default terms during order entry.

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Cash Flow** | Extended payment terms delay cash collection |
| **Credit Risk** | Unauthorized credit extension increases bad debt exposure |
| **Policy Violation** | Bypasses credit management approval process |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| Single mismatch | Master data outdated, negotiated exception | Multiple users overriding same customer |
| Credit tier change (SD07→SD05) | Approved promotion, volume discount | Cash to credit conversion (C100→SD07) |
| User with multiple overrides | Sales manager with approval authority | Junior user without credit authority |

---

## Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| **Alert Instance Name** | Sales Document Payment Terms check |
| **Alert Instance ID** | 200025_001443 |
| **Module** | SD (Sales & Distribution) |
| **Category** | Applications |
| **Subcategory** | SD Alerts |

### Execution Context

| Attribute | Value |
|-----------|-------|
| **Source System** | Production S4 (PS4) |
| **Exception Indicator ID** | SW_10_01_SD_PT_CHK |
| **Created On** | 28.10.2025 |
| **Data Saving** | Cloud |
| **Collection Mode** | Full |
| **Execution Mode** | On event presence |

### Alert Parameters

| Parameter | Description | Value |
|-----------|-------------|-------|
| BACKDAYS | Lookback period | 3 days |
| PARVW | Partner Function | RG (Payer) |
| DATE_REF_FLD | Reference date field | ERDAT (Created on) |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Unique Sales Documents** | **6** |
| **Total Value** | **637,071 ZAR (~$35,400 USD)** |
| **Period** | Nov 19-26, 2025 (1 week) |
| **Sales Organization** | **SA01 (South Africa) - 100%** |
| **Severity** | **HIGH** |
| **Fraud Indicator** | **INVESTIGATE** |

### What Happened

**6 sales documents** were created where the payment terms used in the order **differ from the customer's established payment terms** in master data. This represents a control bypass - users are overriding pre-approved credit terms without documented authorization. The largest concentration is with **ROOFCO STEEL** (2 orders, 600,748 ZAR) where payment terms were changed from **C100 (Cash) to SD07 (7-day credit)**.

### Top 3 Findings

1. **ROOFCO STEEL - Cash to Credit Override:** Documents 600030553 and 600030608 both show payment terms changed from C100 to SD07, totaling **600,748 ZAR ($33K USD)**. Created by different users (VNJAPHA and PMOKGOKO) - indicates either outdated master data or repeated unauthorized extension.

2. **THE SPAR GROUP LTD - Three Locations Affected:** Three different SPAR distribution centers (South Rand DC, KZN DC) have orders where payment terms were changed from SD07 to SD05, totaling **35,177 ZAR**. Pattern suggests possible customer-wide negotiation not reflected in master data.

3. **User Concentration - PMOKGOKO:** Portia Mokgoko created **4 of 6 documents** with payment term mismatches, representing **319,429 ZAR (50%)**. Requires investigation - training issue or intentional override?

### Immediate Actions

1. **Review ROOFCO STEEL orders** - verify authorization for credit extension (Owner: Credit Manager)
2. **Interview PMOKGOKO and VNJAPHA** - understand reason for overrides (Owner: Line Manager)
3. **Update customer master data** - if changes are legitimate, update KNVV-ZTERM (Owner: Master Data Team)

---

## Key Metrics

### Financial Impact

| Metric | Value |
|--------|-------|
| **Total Value** | 637,071 ZAR |
| **USD Equivalent** | ~$35,400 |
| **Largest Single Document** | 300,374 ZAR ($16,700 USD) |
| **Average per Document** | 106,179 ZAR ($5,900 USD) |
| **Currency** | ZAR (South African Rand) |

### Volume

| Metric | Count |
|--------|-------|
| **Unique Sales Documents** | 6 |
| **Alert Executions** | 11 (same docs captured multiple times) |
| **Unique Payers** | 5 |
| **Unique Users (Creators)** | 3 |

### Patterns

| Mismatch Pattern | Documents | Value (ZAR) | % Value | Risk Level |
|------------------|-----------|-------------|---------|------------|
| **C100 → SD07** (Cash to Credit) | 2 | 600,748 | 94% | **CRITICAL** |
| SD07 → SD05 (Credit tier change) | 3 | 35,177 | 6% | MEDIUM |
| I060 → SD10 (Inter-company) | 1 | 1,146 | <1% | LOW |

---

## Concentration Analysis

### By Sales Organization

| Sales Org | Country | Documents | Value (ZAR) | ~USD | % |
|-----------|---------|-----------|-------------|------|---|
| **SA01** | South Africa | 6 | 637,071 | $35,400 | **100%** |

**Note:** All mismatches are concentrated in SA01 (South Africa).

### By Entity (Customer)

| Rank | Customer | Payer ID | Documents | Override Pattern | Value (ZAR) | ~USD |
|------|----------|----------|-----------|------------------|-------------|------|
| 1 | **ROOFCO STEEL** | 2008269 | 2 | C100 → SD07 | 600,748 | $33,375 |
| 2 | SPAR SOUTH RAND DC | 2009534 | 1 | SD07 → SD05 | 19,560 | $1,087 |
| 3 | SPAR KZN DC | 2011290 | 1 | SD07 → SD05 | 12,250 | $681 |
| 4 | SPAR KZN DC | 2009574 | 1 | SD07 → SD05 | 3,367 | $187 |
| 5 | SUPA ROOF PTY LTD | 100121 | 1 | I060 → SD10 | 1,146 | $64 |

**Flag:** ROOFCO STEEL represents **94% of total value** with cash-to-credit conversion.

### By User (Document Creator)

| User ID | Full Name | Documents | Value (ZAR) | % of Total | Risk |
|---------|-----------|-----------|-------------|------------|------|
| **PMOKGOKO** | Portia Mokgoko | 4 | 319,429 | 50% | **HIGH** |
| **VNJAPHA** | Vusumzi Njapha | 1 | 300,374 | 47% | **HIGH** |
| PKHUMBUZA | Percy Khumbuza | 1 | 19,560 | 3% | MEDIUM |

### Largest Transactions

| Document | Customer | Order PT | Master PT | Value (ZAR) | ~USD | Creator | Risk |
|----------|----------|----------|-----------|-------------|------|---------|------|
| 600030553 | ROOFCO STEEL | C100 | SD07 | 300,374 | $16,700 | VNJAPHA | **CRITICAL** |
| 600030608 | ROOFCO STEEL | C100 | SD07 | 300,374 | $16,700 | PMOKGOKO | **CRITICAL** |
| 600030561 | SPAR SOUTH RAND DC | SD07 | SD05 | 19,560 | $1,087 | PKHUMBUZA | MEDIUM |
| 600030613 | SPAR KZN DC | SD07 | SD05 | 12,250 | $681 | PMOKGOKO | MEDIUM |
| 600030612 | SPAR KZN DC | SD07 | SD05 | 3,367 | $187 | PMOKGOKO | MEDIUM |

---

## Risk Assessment

### Classification

| Factor | Assessment | Reasoning |
|--------|------------|-----------|
| **Focus Area** | ACCESS_GOVERNANCE | Unauthorized override of credit controls |
| **Severity** | HIGH | Cash to credit conversion = policy bypass |
| **Risk Score** | 70/100 | Multiple users, high value, control bypass |
| **Fraud Indicator** | **INVESTIGATE** | Cash to credit without authorization |

### Risk Indicators

| Risk Type | Evidence | Recommended Action |
|-----------|----------|-------------------|
| **Policy Violation** | C100→SD07 (cash to credit) | Verify authorization chain |
| **User Concentration** | PMOKGOKO: 50% of documents | Review user authorization |
| **Repeat Pattern** | Same customer (ROOFCO) overridden by 2 users | Update master data or enforce terms |
| **Process Gap** | No workflow approval for payment term change | Implement approval control |

---

## Recommended Actions

### Immediate (24-48 hours)

1. **Review ROOFCO STEEL authorization**
   - Check if credit extension was approved by credit manager
   - Retrieve supporting documentation (customer request, approval email)
   - If not authorized, flag for recovery action

2. **Interview document creators**
   - PMOKGOKO: 4 documents - understand decision rationale
   - VNJAPHA: 1 high-value document - verify approval
   - Document findings for audit trail

3. **Update customer master data**
   - If SPAR GROUP negotiated new terms, update KNVV-ZTERM
   - If ROOFCO STEEL should be on credit, update master

### Short-term (1-2 weeks)

1. **Implement payment term change approval**
   - Add workflow for changes >$10K
   - Require credit manager sign-off for cash→credit conversion
   - Log all overrides with reason code

2. **Review user authorization**
   - Verify PMOKGOKO has authority to extend credit terms
   - Document authorization levels for payment term changes

3. **Master data cleanup**
   - Review customers with repeated mismatches
   - Update KNVV-ZTERM where legitimate changes occurred

### Process Improvements

1. **System Control:** Add workflow approval for payment term changes >$10K
2. **User Training:** Reinforce policy on payment term overrides
3. **Monitoring:** Add alert threshold for repeat overrides by same user

---

## Technical Details

### Source Tables

| Table | Description |
|-------|-------------|
| VBAK | Sales Document Header |
| VBKD | Sales Document Business Data (Document Payment Terms) |
| VBPA | Sales Document Partners (Payer) |
| KNVV | Customer Sales Area Data (Master Payment Terms) |
| KNA1 | Customer Master General Data |

### Key Fields

| Field | Table | Description |
|-------|-------|-------------|
| ZTERM | VBKD | Payment terms on document |
| ZTERM | KNVV | Payment terms in customer master |
| VKORG | VBAK | Sales organization |
| VTWEG | VBAK | Distribution channel |
| SPART | VBAK | Division |
| KUNNR | VBPA | Customer number (payer) |

### Detection Logic

```abap
SELECT ... FROM VBAK
  INNER JOIN VBPA ON VBAK~VBELN = VBPA~VBELN
  INNER JOIN VBKD ON VBAK~VBELN = VBKD~VBELN
  INNER JOIN KNVV ON VBPA~KUNNR = KNVV~KUNNR
                 AND VBAK~VKORG = KNVV~VKORG
                 AND VBAK~VTWEG = KNVV~VTWEG
                 AND VBAK~SPART = KNVV~SPART
                 AND VBKD~ZTERM NE KNVV~ZTERM  -- KEY FILTER
WHERE VBPA~PARVW = 'RG'  -- Payer partner function
```

**Key Logic:** The alert triggers when `VBKD-ZTERM` (document payment terms) does NOT equal `KNVV-ZTERM` (customer master payment terms).

### Payment Terms Codes Reference

| Code | Typical Meaning | Notes |
|------|-----------------|-------|
| C100 | Cash on Delivery | Strict terms - no credit |
| SD05 | 5 days net | Short credit |
| SD07 | 7 days net | Short credit |
| SD10 | 10 days net | Short credit |
| I060 | Inter-company 60 days | Internal terms |

### Artifacts Analyzed

| File | Purpose |
|------|---------|
| Explanation_*.docx | Business context |
| Metadata_*.xlsx | Alert configuration |
| Summary_*.xlsx | Transaction data (11 records, 6 unique) |
| Code_*.txt | ABAP detection logic |

### Exchange Rates Used

| Currency | Rate (per 1 USD) | Date |
|----------|------------------|------|
| ZAR | 18 | November 2025 |

---

*Analysis generated following QUANTITATIVE_ALERT_WORKFLOW.md v1.2 and templates/quantitative-alert.yaml*
