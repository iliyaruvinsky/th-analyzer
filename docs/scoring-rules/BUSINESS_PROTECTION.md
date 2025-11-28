# BUSINESS_PROTECTION Alert Severity Classification

## Foundational Principle

**Alerts are NOT confirmations of fraud or bad events.** They expose POSSIBILITIES that require stakeholder review.

Severity reflects:
1. **Urgency of review required** - How quickly must someone look at this?
2. **Potential harm if ignored** - What's the worst-case scenario?
3. **Type of risk:**
   - Cybersecurity breach
   - Possible fraud
   - Compliance issues (e.g., SoD violations)
   - Business process deviation

---

## CRITICAL Severity (Base Score: 90)

**Characteristic:** Events that MUST be reviewed immediately. Either:
- Pure cybersecurity breaches (policy violations regardless of intent)
- Direct theft patterns (not "possible" - structural theft mechanism)
- Actions that grant unrestricted system access

| Alert Type | Risk Category | Why Critical |
|-----------|--------------|--------------|
| DEBUG system updates | Cybersecurity Breach | Bypasses all controls - unacceptable regardless of intent |
| SAP_ALL/SAP_NEW grants | Access Control | Full system access granted - MUST inform stakeholders even if legitimate |
| PO for One-Time Vendor | Direct Theft Pattern | Payment to untraceable vendor - structural mechanism for theft |
| Activating transactions by unauthorized users | Cybersecurity Breach | Security control bypass - succeeded despite no authorization |
| Creating DIALOG user by unauthorized parties | Cybersecurity Breach | User master manipulation by non-Basis/non-Auth team |

**Key Nuance:**
- SAP_ALL grant may be legitimate (some people need it), but it's CRITICAL because stakeholders MUST be informed
- PO for One-Time Vendor is actual theft pattern - "somebody paid using one-time vendor"

---

## HIGH Severity (Base Score: 75)

**Characteristic:** Strong indicators of POSSIBLE fraud requiring prompt review. Pattern suggests wrongdoing but could have explanation.

| Alert Type | Risk Category | Why High |
|-----------|--------------|----------|
| Vendor bank changed then reversed | Possible Fraud | Classic fraud pattern - but could be legitimate correction |
| Vendor credentials changed multiple times | Possible Fraud | Suspicious pattern - needs review |
| Suspicious material movements | Possible Theft | Could be theft OR part of normal process |
| Alternative payee assigned | Possible Fraud | Payment redirection - wrong procedure or fraud |
| Account payable fraud indicators | Possible Fraud | Suspicious when person is in unrelated position |
| Inventory variance (booked vs. counted) | Possible Theft | Significant discrepancy needs investigation |
| Login to DIALOG user via password (not SSO) | Security Violation | Bypasses Single Sign-On policy |
| Rarely Used Vendors (RUV) | Possible Fraud | Silent for years then rare transaction = someone must check what it was for |
| SoD violation AND possible fraud | Compliance + Fraud | Dual concern escalates to HIGH |
| Sensitive transaction usage | Audit/Compliance | Stakeholders need to know WHO, WHY, HOW |

**Key Nuance:**
- "Possible fraud" means investigation needed - NOT confirmation
- Suspicious material movement may be "part of the process as client defined it"
- Person's position matters - AP clerk doing AP things is different from unrelated position doing AP things
- RUV: A vendor silent for years with occasional rare transactions is a fraud indicator requiring investigation
- Sensitive transactions: Not just tracking - stakeholders actively want answers about who/why/how

---

## MEDIUM Severity (Base Score: 60)

**Characteristic:** SoD violations and process deviations that MAY be acceptable in some organizations but need documentation/review.

| Alert Type | Risk Category | Why Medium |
|-----------|--------------|------------|
| PO/PR approved by creator | Pure SoD Violation | May be OK in thin-staffed orgs |
| FI doc parked/posted by same user | Pure SoD Violation | Could be legitimate in small teams |
| GR/IR + Vendor data altered by same user | Pure SoD Violation | Resource constraint possible |
| PO created retroactively | Process Deviation | Might be part of process |
| Vendor payment terms mismatch | Process Error | Must address to avoid money loss |
| Exceptional postings by GL account | Anomaly | Unusual posting - needs review |
| Over delivery tolerance changed | Control Bypass | Potential misuse |

**Key Nuance:**
- Pure SoD violations (without fraud indicator) remain MEDIUM because they MAY be acceptable in resource-constrained organizations
- SoD violations may be acceptable "in rare cases when the org is thin on human resources"
- Process deviations might be "part of the process" per client definition
- These still need documentation for audit trail

---

## LOW Severity (Base Score: 50)

**Characteristic:** Events that should be tracked for awareness/housekeeping but don't indicate immediate risk.

| Alert Type | Risk Category | Why Low |
|-----------|--------------|---------|
| One-time vendor created | Tracking | Track for later - could escalate based on usage |
| Customer credit limit changed | Business Exposure | Business decision tracking |
| Inactive vendor (no balance) | Housekeeping | System cleanup needed |
| Inactive vendor with balance | Financial Risk | Can cause headache if balance not closed |

**Key Nuance:**
- "Inactive vendor with balance" can escalate if amounts are significant (quantitative factor)
- "One-time vendor created" is LOW but "PO for one-time vendor" is CRITICAL

---

## Severity Assignment Logic

```
SEVERITY = f(Risk_Type, Certainty_Level, Required_Response_Time)

Where:
- CRITICAL: Cybersecurity breach OR direct theft mechanism OR full access grant
           → Requires IMMEDIATE review regardless of legitimacy

- HIGH:    "Possible fraud/theft" pattern - classic indicators
           → Requires PROMPT review within hours/day

- MEDIUM:  SoD violation OR process deviation - MAY be acceptable
           → Requires REVIEW for documentation/audit

- LOW:     Tracking/housekeeping - no immediate risk indicator
           → Requires AWARENESS for trend monitoring
```

---

## Important Distinctions

| What Alert Says | What It Means | Severity Impact |
|-----------------|---------------|-----------------|
| "Unacceptable and dangerous action" | Policy violation - review required | CRITICAL |
| "Intentional Fraud" | Strong indicator BUT still needs verification | HIGH (not auto-confirmed) |
| "Possible fraud" | Investigation trigger - not conclusion | HIGH |
| "SoD violation and possible fraud" | Dual concern - escalates severity | HIGH |
| "Misbehavior leading to..." | Process deviation - context matters | MEDIUM |
| "Should be tracked" | Awareness item | LOW |

---

## Scoring Factors Summary

This classification is **Factor 1 (Alert Nature)** of the overall severity calculation.

The final risk score also incorporates:
- **Factor 2:** Count (normalized by BACKDAYS)
- **Factor 3:** Monetary amounts involved
- **Factor 4:** Focus area multiplier (1.2 for BUSINESS_PROTECTION)
- **Factor 5:** Quantity/pattern adjustments

```
Final Score = (Factor1 + Factor2 + Factor3 + Factor5) × Factor4
```

---

## Implementation Status

- [x] Severity base scores updated (90/75/60/50)
- [x] Alert-type to severity mapping implemented
- [x] BACKDAYS extraction from Metadata AND Code files
- [x] Factor 5 (quantities) added
- [x] Unit tests created (79 tests passing)
- [x] Tested with real alerts: Rarely Used Vendors, Modified Vendor Bank, Inventory Count, etc.
- [x] **BUG FIX**: Quantitative extraction from Summary_* only (not Explanation_* template text)
- [ ] Refinement based on user feedback (this document)

## ⚠️ Data Source Principle

**Quantitative data (counts, monetary amounts) MUST be extracted ONLY from Summary_* files.**

| File | Extract Numbers? | Why |
|------|------------------|-----|
| Summary_* | ✅ YES | Contains actual alert output data |
| Explanation_* | ❌ NO | Contains template/example text (may have fake numbers) |
| Code_* | ❌ NO | Contains ABAP code, not data |
| Metadata_* | ⚠️ BACKDAYS only | Parameters only, not data |

## Unit Test Coverage

Tests located in `backend/tests/content_analyzer/`:
- `test_classification.py` - Focus area classification (17 tests)
- `test_severity.py` - Severity determination (22 tests)
- `test_scoring.py` - Score calculation & BACKDAYS (40 tests)

Run tests: `docker compose exec backend python -m pytest tests/ -v`

---

*Last Updated: 2025-11-26 (Session 2 - Data Source Fix)*
*Make corrections directly in this file*
