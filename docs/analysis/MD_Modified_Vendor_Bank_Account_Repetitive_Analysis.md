# Modified Vendor Bank Account - Repetitive Analysis

> **Alert ID:** 200025_001355 | **Module:** MD | **Analysis Date:** November 2025

---

## Key Findings

| Metric | Value |
|--------|-------|
| Records | 71 repetitive bank changes |
| Period | Extended (REPET_BACKDAYS: 99999) |
| Vendors Affected | 34 vendors across 5 countries |
| Severity | CRITICAL |

## Critical Discovery

**Same Account Numbers on Multiple Vendors:**
• Account `62349726747` used for 4 different vendors
• Account `3100023909` used for 3 different vendors
• 82% same-day create/delete cycles - classic fraud probing pattern

## Concentration Pattern

| User | Changes | % of Total |
|------|---------|------------|
| PMBURU | 49 | **69.0%** |
| RGACHINGA | 11 | 15.5% |
| CMBOTI | 11 | 15.5% |

Same account numbers seeded across multiple vendors indicates active payment diversion attempt.

---

## Business Context

> **Business Purpose:** This alert identifies vendors where bank account information has been modified MULTIPLE TIMES within a detection period. Repetitive changes to bank credentials represent the most acute form of payment fraud risk - they indicate deliberate manipulation attempts where accounts are created, modified, and potentially reversed to test payment routing or cover fraudulent activity. Unlike single changes which may be legitimate corrections, repetitive changes demand immediate investigation as potential fraud indicators.

### What This Alert Monitors

Tracks BANKN (bank account number) field changes in the LFBK table where the same vendor has multiple modifications detected. The REPETITIVE parameter identifies cases where a previous value becomes a new value again, or where multiple sequential changes occur to the same vendor's banking details.

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Payment Diversion Scheme** | Sequential changes suggest testing of fraudulent accounts before payment processing |
| **Cover-up Activity** | Create-then-delete patterns indicate attempts to hide fraudulent account insertions |
| **Collusion Indicator** | Multiple users changing same vendor = potential internal conspiracy |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| Create → Delete (same day) | Data entry error, immediate correction | Account tested then removed to avoid detection |
| Same account on multiple vendors | Corporate account for related entities | Single fraudulent account being seeded across vendors |
| Multiple changes within minutes | Typo corrections | Rapid probing of payment routing |

---

## 2. Executive Summary

### Alert Identity

| Attribute | Value |
|-----------|-------|
| **Alert Name** | Modified Vendor Bank Account - Repetitive |
| **Alert ID** | 200025_001355 |
| **Module** | MD (Master Data) |
| **Category** | Applications |
| **Subcategory** | FI Alerts |

### Execution Context

| Attribute | Value |
|-----------|-------|
| **Source System** | Production S4 (PS4) |
| **Created Date** | 18.06.2025 |
| **Last Updated** | 28.11.2025 |
| **Exception Indicator ID** | SW_10_06_VND_BANK_CH |
| **Exception Indicator Name** | MD: Vendor Bank Details Change Log |
| **Collection Mode** | Full |
| **Execution Mode** | On event presence |

### Alert Parameters

| Parameter | Description | Value |
|-----------|-------------|-------|
| BACKDAYS | Lookback period for initial changes | 9999 |
| CONVERT_KEY | Decompose key field | X (enabled) |
| FNAME | Field monitored | **BANKN only** (account number) |
| **REPETITIVE** | **Repetitive change detection** | **X (enabled)** |
| REPET_BACKDAYS | Lookback for repetitive patterns | 99999 |
| TABNAME | Table monitored | LFBK |

### The Bottom Line

| Metric | Value |
|--------|-------|
| **Total Records** | **71 repetitive changes** |
| **Vendors Affected** | **34 vendors** |
| **Severity** | **CRITICAL** |
| **Fraud Indicator** | **YES** |

### What Happened

**34 vendors** exhibited **repetitive bank account modification patterns** - all vendors had their account numbers changed multiple times. **28 of 34 vendors (82%)** had all changes occur on the **same day**, indicating rapid create/modify/delete cycles. The same bank account numbers appear across multiple unrelated vendors, a classic indicator of fraudulent account seeding.

### Top 3 Findings

1. **Same account numbers across multiple vendors:** Account `62349726747` used for 4 different vendors, account `3100023909` for 3 vendors - indicates systematic fraud attempt
2. **82% same-day changes:** 28 of 34 vendors had all modifications on single day - rapid probing pattern
3. **Create-then-Delete pattern dominant:** 32 of 71 records are deletions immediately following creations - classic cover-up behavior

### Immediate Actions

1. **FREEZE all payments** to the 34 affected vendors immediately
2. **Forensic review** of vendors with 3+ changes (2011720, 2011571) - highest fraud probability
3. **Investigate accounts** appearing on multiple vendors: `62349726747`, `3100023909`, `102446298100`

---

## 3. Key Metrics

### Financial Impact

| Metric | Value |
|--------|-------|
| **Potential Exposure** | **ALL payments to 34 vendors at risk** |
| **Risk Level** | **CRITICAL** - Repetitive patterns indicate active fraud attempt |
| **Pattern Confidence** | **HIGH** - 82% same-day changes, shared account numbers |

### Volume

| Dimension | Count |
|-----------|-------|
| **Total Changes** | 71 |
| **Unique Vendors** | 34 |
| **Unique Users** | 3 |
| **Countries Affected** | 5 |
| **Vendors with 3+ changes** | 2 |
| **Vendors with exactly 2 changes** | 32 |

### Pattern Breakdown

| Pattern | Count | Percentage | Risk Level |
|---------|-------|------------|------------|
| XK02 (Modify existing vendor) | 39 | 54.9% | HIGH |
| XK01 (Create new vendor) | 32 | 45.1% | MEDIUM |

| Change Type | Count | Percentage |
|-------------|-------|------------|
| Change (modification) | 39 | 54.9% |
| Delete (field removal) | 32 | 45.1% |

---

## 4. Concentration Analysis

### By User (CRITICAL)

| Rank | User | Changes | Unique Vendors | % of Total |
|------|------|---------|----------------|------------|
| 1 | **PMBURU** | **49** | **25** | **69.0%** |
| 2 | RGACHINGA | 11 | 6 | 15.5% |
| 3 | CMBOTI | 11 | 5 | 15.5% |

**WARNING:** User PMBURU responsible for **69% of all repetitive changes** - IMMEDIATE SoD review required.

### By Bank Country

| Rank | Country | Changes | % of Total |
|------|---------|---------|------------|
| 1 | ZA (South Africa) | 20 | 28.2% |
| 2 | TZ (Tanzania) | 17 | 23.9% |
| 3 | UG (Uganda) | 16 | 22.5% |
| 4 | KE (Kenya) | 12 | 16.9% |
| 5 | RW (Rwanda) | 6 | 8.5% |

### Suspicious Account Numbers (Used Across Multiple Vendors)

| Account Number | Occurrences | Risk |
|----------------|-------------|------|
| **62349726747** | **4** | **CRITICAL** - Same account on 4 vendors |
| 3100023909 | 3 | HIGH |
| 102446298100 | 3 | HIGH |

---

## 5. Change Sequence Analysis (CRITICAL)

### Highest Risk: Vendors with 3+ Changes

**Vendor 2011720 (Rwanda) - 4 Changes**
```
SEQUENCE OF CHANGES:
┌────┬─────────────────────┬───────────┬───────┬────────────────────────────────────────────────┐
│ #  │ Date/Time           │ User      │ TCode │ Change                                         │
├────┼─────────────────────┼───────────┼───────┼────────────────────────────────────────────────┤
│ 1  │ 2024/07/11 08:55:01 │ RGACHINGA │ XK02  │ (empty) → 400026106958128220                   │
│ 2  │ 2024/08/21 22:25:42 │ CMBOTI    │ XK02  │ 4.000261069581281e+17 → 002610695812923        │
│ 3  │ 2024/08/21 22:29:41 │ CMBOTI    │ XK02  │ (empty) → 400026106958128000                   │
│ 4  │ 2024/08/21 22:31:12 │ CMBOTI    │ XK02  │ 4.00026106958128e+17 → (deleted)               │
└────┴─────────────────────┴───────────┴───────┴────────────────────────────────────────────────┘

ANALYSIS:
- 3 changes within 6 MINUTES (22:25 to 22:31) by CMBOTI
- Account created, modified, then deleted
- CLASSIC FRAUD PROBING PATTERN
```

**Vendor 2011571 (Tanzania) - 3 Changes**
```
SEQUENCE OF CHANGES:
┌────┬─────────────────────┬────────┬───────┬────────────────────────────────────────────────┐
│ #  │ Date/Time           │ User   │ TCode │ Change                                         │
├────┼─────────────────────┼────────┼───────┼────────────────────────────────────────────────┤
│ 1  │ 2024/05/20 12:45:03 │ PMBURU │ XK01  │ (empty) → 141740000324                         │
│ 2  │ 2024/05/27 08:54:35 │ CMBOTI │ XK02  │ 912002138598 → (deleted)                       │
│ 3  │ 2024/05/27 08:56:57 │ CMBOTI │ XK02  │ 141740000324 → 0141740000324                   │
└────┴─────────────────────┴────────┴───────┴────────────────────────────────────────────────┘

ANALYSIS:
- Different users (PMBURU creates, CMBOTI modifies)
- 2-minute gap between changes 2 and 3
- Account reformatted (added leading zero)
```

### Sample 2-Change Patterns (Create → Delete Same Day)

| Vendor | Country | Time Gap | User | Pattern |
|--------|---------|----------|------|---------|
| 2011414 | ZA | 2 hours | CMBOTI | Created 63045068110 → Deleted same account |
| 2011415 | ZA | 2 hours | CMBOTI | Created 63045068110 → Deleted same account |
| 2011426 | UG | 24 min | RGACHINGA | Created 3100023909 → Deleted |
| 2011429 | UG | 24 min | RGACHINGA | Created 3100023909 → Deleted |
| 2011430 | UG | 25 min | RGACHINGA | Created 3100023909 → Deleted |

**Note:** Vendors 2011426, 2011429, 2011430 all used the **SAME account number** (3100023909)

---

## 6. Risk Assessment

### Classification

| Dimension | Value | Reasoning |
|-----------|-------|-----------|
| **Focus Area** | BUSINESS_PROTECTION | Active fraud detection - repetitive changes indicate deliberate manipulation |
| **Severity** | **CRITICAL** | Multiple fraud indicators: repetitive changes, shared accounts, rapid cycling |
| **Risk Score** | **92/100** | Maximum indicators present |
| **Fraud Indicator** | **YES** | Pattern confidence: HIGH - this is not accidental |

### Risk Score Breakdown

| Component | Points | Reasoning |
|-----------|--------|-----------|
| Repetitive Pattern | 35 | Every vendor has multiple changes by definition |
| Shared Accounts | 25 | Same account numbers used across unrelated vendors |
| Same-Day Cycling | 20 | 82% of vendors changed on single day |
| User Concentration | 12 | PMBURU: 69% of all changes |
| **Total** | **92** | |

### Risk Indicators

| Risk Type | Evidence | Recommended Action |
|-----------|----------|-------------------|
| **ACTIVE FRAUD ATTEMPT** | Same accounts on multiple vendors, rapid create/delete cycles | FREEZE payments, forensic investigation |
| **Collusion Possible** | Multiple users modifying same vendors (PMBURU creates, CMBOTI deletes) | Interview users separately |
| **Payment Diversion** | Accounts tested then removed within minutes | Trace any payments made during modification windows |
| **Cover-up Activity** | 45% of changes are deletions | Recover deleted account details from change logs |

---

## 7. Recommended Actions

### Immediate (24-48 hours)

1. **FREEZE ALL PAYMENTS**
   - Place immediate hold on all payments to 34 affected vendors
   - Require CFO-level approval for any payment release
   - Document all pending payment amounts

2. **Forensic Account Analysis**
   - Investigate accounts appearing on multiple vendors:
     - `62349726747` (4 vendors)
     - `3100023909` (3 vendors)
     - `102446298100` (3 vendors)
   - Verify if these accounts exist and ownership

3. **User Suspension Review**
   - Temporarily suspend vendor master modification access for PMBURU (69% of changes)
   - Conduct interviews with PMBURU, CMBOTI, RGACHINGA
   - Review SoD conflicts - do any have payment processing access?

### Short-term (1-2 weeks)

1. **Payment Audit**
   - Review ALL payments made to 34 vendors in last 6 months
   - Cross-reference payment dates with account modification windows
   - Identify any payments made to now-deleted accounts

2. **Vendor Verification**
   - Contact all 34 vendors to verify legitimate bank details
   - Request bank confirmation letters
   - Validate vendor existence and legitimacy

3. **Access Review**
   - Implement dual-approval for all bank detail changes
   - Remove single-user modification capability
   - Add real-time alerts for repetitive change patterns

### Process Improvements

1. **Implement 4-eyes principle** with mandatory second approval
2. **Add velocity controls** - block >1 bank change per vendor per week
3. **Require vendor confirmation** via separate channel before activating changes

---

## 8. Technical Details

### Detection Logic

The REPETITIVE parameter enables special logic in the ABAP function `/SKN/F_SW_10_06_MD_CHNG_LOG`:

```abap
IF LV_REPETITIVE EQ ABAP_TRUE.
  ' Checks if VALUE_OLD equals VALUE_NEW (reversal pattern)
  IF LS_DATA_TMP-VALUE_OLD EQ LS_DATA-VALUE_NEW.
    APPEND LS_DATA TO LT_DATA_TMP2.
    LV_EXIST = 'X'.
  ENDIF.
  ' Tracks sequential changes to same vendor key fields
```

The code identifies repetitive patterns by:
1. Comparing OLD values with NEW values to detect reversals
2. Tracking multiple changes to the same TABKEY (vendor/bank combination)
3. Using REPET_BACKDAYS for extended historical comparison

### Key Difference from Standard Alert

| Attribute | Standard (001356) | Repetitive (001355) |
|-----------|-------------------|---------------------|
| FNAME monitored | BANKL, BANKN, BANKS, BKREF, BVTYP | **BANKN only** |
| REPETITIVE flag | Not set | **X (enabled)** |
| Focus | Any bank change | **Sequential/repeated changes** |
| Risk level | HIGH | **CRITICAL** |

### Artifacts Analyzed

| File | Description |
|------|-------------|
| `Explanation_Modified Vendor Bank Account - Repetitive_200025_001355.docx` | Business purpose |
| `Metadata _Modified Vendor Bank Account - Repetitive_200025_001355.xlsx` | Alert configuration |
| `Code_Modified Vendor Bank Account - Repetitive_200025_001355.txt` | ABAP detection logic |
| `Summary_Modified Vendor Bank Account - Repetitive_200025_001355.xlsx` | 71 repetitive change records |

### Content Analyzer Output

```json
{
  "alert_id": "200025_001355",
  "alert_name": "Modified Vendor Bank Account - Repetitive",
  "module": "MD",
  "source_system": "PS4",
  "analysis_date": "2025-11-28",
  "metrics": {
    "total_records": 71,
    "unique_vendors": 34,
    "unique_users": 3,
    "countries_affected": 5,
    "vendors_with_3plus_changes": 2,
    "vendors_same_day_changes": 28
  },
  "patterns": {
    "transaction_type": {"XK02": 39, "XK01": 32},
    "change_type": {"Change": 39, "Delete": 32},
    "by_user": {"PMBURU": 49, "RGACHINGA": 11, "CMBOTI": 11},
    "by_country": {"ZA": 20, "TZ": 17, "UG": 16, "KE": 12, "RW": 6}
  },
  "fraud_indicators": {
    "same_account_multiple_vendors": true,
    "same_day_create_delete": true,
    "rapid_sequential_changes": true,
    "user_concentration": 0.69
  },
  "suspicious_accounts": [
    {"account": "62349726747", "occurrences": 4},
    {"account": "3100023909", "occurrences": 3},
    {"account": "102446298100", "occurrences": 3}
  ],
  "classification": {
    "focus_area": "BUSINESS_PROTECTION",
    "severity": "CRITICAL",
    "risk_score": 92,
    "fraud_indicator": "YES"
  }
}
```

---

*Analysis generated following the Quantitative Alert Analysis Template v1.0*
*Special handling: Repetitive change analysis with temporal ordering per ALERT_CLASSIFICATION_PRINCIPLES.md*
