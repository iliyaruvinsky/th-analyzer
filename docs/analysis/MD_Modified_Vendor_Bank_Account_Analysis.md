# Modified Vendor Bank Account Analysis

> **Alert ID:** 200025_001356 | **Module:** MD | **Analysis Date:** November 2025

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 155 bank account changes |
| Period | 365 days (BACKDAYS parameter) |
| Vendors Affected | 15 vendors across 5 countries |
| Severity | HIGH |

## Critical Discovery

**User PMBURU - 66% of All Bank Changes:**
• 102 of 155 changes made by single user
• 10 vendors affected across 5 countries
• SoD review required - check if user has payment processing access

## Concentration Pattern

| User | Changes | % of Total |
|------|---------|------------|
| PMBURU | 102 | **65.8%** |
| CMBOTI | 53 | 34.2% |

80 bank key (routing) changes and 34 account number changes require vendor confirmation before payments.

---

## Business Context

> **Business Purpose:** This alert monitors changes to vendor bank account details in the SAP system. Vendor bank account modifications represent one of the highest fraud risks in any ERP system, as unauthorized changes can redirect legitimate payments to fraudulent accounts. This alert tracks alterations to the LFBK table (vendor bank master data) through SAP's change document mechanism (CDHDR/CDPOS), capturing modifications to bank keys, account numbers, and reference fields.

### What This Alert Monitors

Tracks changes to vendor banking information stored in table LFBK, including bank key (BANKL), account number (BANKN), bank country (BANKS), bank reference (BKREF), and partner bank type (BVTYP). Changes are captured via SAP change documents using transaction XK02.

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Payment Fraud** | Modified bank details can redirect vendor payments to unauthorized accounts |
| **Embezzlement** | Internal actors may modify details to steal company funds |
| **SoD Violation** | Same user modifying bank details and processing payments = red flag |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| Bank key change | Vendor relocated/changed banks | Multiple changes to same vendor in short period |
| Account number change | Vendor opened new account | Change made without documented vendor request |
| High volume by single user | Dedicated master data team | User also processes payments to same vendors |

---

## 2. Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| **Alert Name** | Modified Vendor Bank Account |
| **Alert ID** | 200025_001356 |
| **Module** | MD (Master Data) |
| **Category** | Applications |
| **Subcategory** | MD Alerts |

### Execution Context

| Attribute | Value |
|-----------|-------|
| **Source System** | Production S4 (PS4) |
| **Created Date** | 18.06.2025 |
| **Last Updated** | 23.10.2025 |
| **Exception Indicator ID** | SW_10_06_VND_BANK_CH |
| **Exception Indicator Name** | MD: Vendor Bank Details Change Log |
| **Collection Mode** | Full |
| **Execution Mode** | On event presence |

### Alert Parameters

| Parameter | Description | Value |
|-----------|-------------|-------|
| BACKDAYS | Lookback period in days | 365 |
| CONVERT_KEY | Decompose key field | X (enabled) |
| FNAME | Field Name filter | BANKN, BANKS, BANKL, BKREF, BVTYP |
| TABNAME | Table Name | LFBK |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Total Records** | **155 changes** |
| **Vendors Affected** | **15 vendors** |
| **Severity** | **HIGH** |
| **Fraud Indicator** | **INVESTIGATE** |

### What Happened

Over the past 365 days, **155 vendor bank account modifications** were made to **15 vendors** by only **2 users** (PMBURU and CMBOTI). The changes span **5 countries** (Kenya, South Africa, China, Tanzania, Rwanda) and include **80 bank key changes** and **34 account number changes**. The high concentration of sensitive modifications by just 2 users requires immediate investigation.

### Top 3 Findings

1. **User Concentration Risk:** User PMBURU made **102 changes (66%)** across 10 vendors - investigate authorization level and SoD conflicts
2. **Bank Key Changes Dominant:** 80 of 155 changes (52%) were to bank keys (BANKL) - validates routing info altered
3. **Geographic Spread:** Changes affect banks in 5 countries including high-risk regions - cross-border payment redirection risk

### Immediate Actions

1. **Verify authorization** for users PMBURU and CMBOTI to modify vendor bank details
2. **Cross-check SoD** - confirm neither user has payment processing access
3. **Contact top 5 vendors** to confirm bank changes were requested by them

---

## 3. Key Metrics

### Financial Impact

| Metric | Value |
|--------|-------|
| **Potential Exposure** | Not directly quantifiable - all vendor payments at risk |
| **Risk Level** | HIGH - Bank changes affect payment routing |
| **Currency** | N/A (master data changes) |

*Note: This alert monitors master data changes, not financial transactions. Financial exposure = total payment volume to the 15 affected vendors.*

### Volume

| Dimension | Count |
|-----------|-------|
| **Total Changes** | 155 |
| **Unique Vendors** | 15 |
| **Unique Users** | 2 |
| **Unique Bank Countries** | 5 |
| **Change Dates** | 15 distinct dates |

### Pattern Breakdown

| Change Type | Count | Percentage |
|-------------|-------|------------|
| Update | 117 | 75.5% |
| Delete (field) | 38 | 24.5% |

| Field Changed | Count | Percentage |
|---------------|-------|------------|
| BANKL (Bank Key) | 80 | **51.6%** |
| BANKN (Account Number) | 34 | 21.9% |
| BKREF (Bank Reference) | 19 | 12.3% |
| BVTYP (Partner Bank Type) | 19 | 12.3% |
| BANKS (Bank Country) | 3 | 1.9% |

---

## 4. Concentration Analysis

### By User (CRITICAL)

| Rank | User | Changes | Unique Vendors | Countries Affected | % of Total |
|------|------|---------|----------------|--------------------|-----------:|
| 1 | **PMBURU** | **102** | 10 | ZA, KE, CN, TZ, RW | **65.8%** |
| 2 | CMBOTI | 53 | 5 | TZ, CN, KE | 34.2% |

**WARNING:** User PMBURU responsible for **>50% of all changes** - requires immediate SoD review.

### By Vendor

| Rank | Vendor | Changes | User | Bank Country |
|------|--------|---------|------|--------------|
| 1 | 2012579 | 17 | CMBOTI | CN (China) |
| 2 | 2001209 | 16 | PMBURU | KE (Kenya) |
| 3 | 2008336 | 16 | PMBURU | ZA (South Africa) |
| 4 | 2013143 | 16 | PMBURU | ZA (South Africa) |
| 5 | 2013161 | 16 | PMBURU | KE (Kenya) |

### By Bank Country

| Rank | Country | Changes | % of Total |
|------|---------|---------|------------|
| 1 | **KE (Kenya)** | 60 | **38.7%** |
| 2 | ZA (South Africa) | 40 | 25.8% |
| 3 | CN (China) | 33 | 21.3% |
| 4 | TZ (Tanzania) | 16 | 10.3% |
| 5 | RW (Rwanda) | 6 | 3.9% |

### Sample Bank Changes (High Risk)

| Vendor | Field | Old Value | New Value | User |
|--------|-------|-----------|-----------|------|
| 2008336 | BANKL | 006-32005 | 000-05972 | PMBURU |
| 2008336 | BANKN | 4098609090 | 1876236 | PMBURU |
| 2012579 | BANKL | 57-003 | ZJTLCNBHXXX | CMBOTI |
| 2012579 | BANKN | 1005843886350 | 330203602010000000 | CMBOTI |
| 2012944 | BANKL | 07-000 | 41-118 | CMBOTI |

---

## 5. Risk Assessment

### Classification

| Dimension | Value | Reasoning |
|-----------|-------|-----------|
| **Focus Area** | BUSINESS_PROTECTION | Fraud prevention - vendor bank changes are primary vector for payment fraud |
| **Severity** | **HIGH** | Bank account modifications can redirect legitimate payments to fraudulent accounts |
| **Risk Score** | **78/100** | High user concentration (30) + sensitive data (25) + multi-country scope (15) + volume (8) |
| **Fraud Indicator** | **INVESTIGATE** | Pattern indicates possible internal fraud scheme - 2 users, 15 vendors, 5 countries |

### Risk Score Breakdown

| Component | Points | Reasoning |
|-----------|--------|-----------|
| User Concentration | 30 | Single user (PMBURU) made 66% of changes |
| Data Sensitivity | 25 | Bank routing information - highest fraud risk field |
| Geographic Scope | 15 | 5 countries including emerging markets |
| Volume | 8 | 155 changes in 365 days above normal threshold |
| **Total** | **78** | |

### Risk Indicators

| Risk Type | Evidence | Recommended Action |
|-----------|----------|-------------------|
| **Potential Fraud** | Bank keys and account numbers changed for 15 vendors | Verify all changes with vendor documentation |
| **SoD Violation Risk** | Only 2 users made all changes | Check if users have payment processing roles |
| **Concentration Risk** | PMBURU: 66% of changes | Review user's authorization and activity history |
| **Cross-Border Risk** | Changes in KE, ZA, CN, TZ, RW | Verify vendor legitimacy in each country |

---

## 6. Recommended Actions

### Immediate (24-48 hours)

1. **Freeze Payments**
   - Place hold on payments to all 15 affected vendors
   - Route through secondary approval until verification complete
   - Document all pending payment amounts

2. **User Authorization Review**
   - Verify PMBURU and CMBOTI authorization levels
   - Check Segregation of Duties - confirm no payment processing access
   - Review user activity logs for past 30 days

3. **Vendor Verification**
   - Contact top 5 vendors (2012579, 2001209, 2008336, 2013143, 2013161)
   - Request written confirmation of bank change requests
   - Validate new bank details against vendor documentation

### Short-term (1-2 weeks)

1. **Full Audit Trail Analysis**
   - Review all 155 changes against change request tickets
   - Identify any changes without proper authorization
   - Document discrepancies for investigation

2. **Payment History Review**
   - Analyze payments made to affected vendors post-change
   - Compare payment amounts before/after bank changes
   - Flag any unusual payment patterns

3. **SoD Policy Enhancement**
   - Implement dual-approval for bank detail changes
   - Separate vendor master maintenance from payment processing
   - Add automated alerts for high-risk field changes

### Process Improvements

1. **Implement 4-eyes principle** for all vendor bank changes
2. **Require vendor confirmation** (email/letter) before activating bank changes
3. **Set up real-time monitoring** for changes to LFBK table

---

## 7. Technical Details

### Detection Logic

The alert uses SAP Change Document mechanism (CDHDR/CDPOS tables) to track modifications to the LFBK table (Vendor Bank Details). The ABAP function `/SKN/F_SW_10_06_MD_CHNG_LOG` queries:

1. **CDHDR** - Change document headers with OBJECTCLAS filter
2. **CDPOS** - Change document items filtered to TABNAME = 'LFBK'
3. **Fields tracked:** BANKL (bank key), BANKN (account number), BANKS (bank country), BKREF (reference), BVTYP (partner bank type)
4. **Key conversion** enabled to decompose composite keys for detailed tracking

### Transaction Code

All changes performed via **XK02** (Change Vendor: Purchasing) - standard SAP vendor master maintenance transaction.

### Artifacts Analyzed

| File | Description |
|------|-------------|
| `Explanation_Modified Vendor Bank Account_200025_001356.docx` | Business purpose documentation |
| `Metadata _Modified Vendor Bank Account_200025_001356.xlsx` | Alert configuration (4 sheets) |
| `Code_Modified Vendor Bank Account_200025_001356.txt` | ABAP detection logic (637 lines) |
| `Summary_Modified Vendor Bank Account_200025_001356.xlsx` | 155 change records |

### Content Analyzer Output

```json
{
  "alert_id": "200025_001356",
  "alert_name": "Modified Vendor Bank Account",
  "module": "MD",
  "source_system": "PS4",
  "analysis_date": "2025-11-28",
  "metrics": {
    "total_records": 155,
    "unique_vendors": 15,
    "unique_users": 2,
    "countries_affected": 5,
    "lookback_days": 365
  },
  "patterns": {
    "change_type": {"update": 117, "delete": 38},
    "by_field": {"BANKL": 80, "BANKN": 34, "BKREF": 19, "BVTYP": 19, "BANKS": 3},
    "by_user": {"PMBURU": 102, "CMBOTI": 53},
    "by_country": {"KE": 60, "ZA": 40, "CN": 33, "TZ": 16, "RW": 6}
  },
  "concentration": {
    "top_user_pct": 65.8,
    "top_vendor_changes": 17,
    "top_country_pct": 38.7
  },
  "classification": {
    "focus_area": "BUSINESS_PROTECTION",
    "severity": "HIGH",
    "risk_score": 78,
    "fraud_indicator": "INVESTIGATE"
  }
}
```

---

*Analysis generated following the Quantitative Alert Analysis Template v1.0*
*Workflow: Explanation → Metadata → Code → Summary → Risk Assessment → Report*
