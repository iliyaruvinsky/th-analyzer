# BUSINESS_CONTROL Alert Severity Classification

## Foundational Principle

**Alerts are NOT confirmations of errors or bad events.** They expose POSSIBILITIES that require stakeholder review.

Severity reflects:
1. **Urgency of review required** - How quickly must someone look at this?
2. **Potential harm if ignored** - What's the worst-case scenario?
3. **Type of risk:**
   - Revenue loss (unbilled deliveries)
   - Process breakdowns (bottlenecks, stuck orders)
   - Business process deviations
   - Operational inefficiencies

---

## CRITICAL Severity (Base Score: 90)

**Characteristic:** System-wide failures or critical business process breakdowns that require immediate attention.

**Note:** BUSINESS_CONTROL typically doesn't have critical alerts. Critical issues would typically be classified as:
- BUSINESS_PROTECTION (fraud/security)
- TECHNICAL_CONTROL (system failures)

**Current Status:** No CRITICAL patterns defined for BUSINESS_CONTROL.

---

## HIGH Severity (Base Score: 75)

**Characteristic:** Significant business process issues requiring prompt review. These indicate potential revenue loss, customer impact, or critical process failures.

| Alert Type | Risk Category | Why High |
|-----------|--------------|----------|
| Unbilled Delivery | Revenue Risk | Goods shipped but not invoiced - direct revenue loss risk |
| Process Bottleneck | Process Breakdown | Critical process stuck - impacts operations |
| Stuck Order / Blocked Order | Customer Impact | Orders blocked - customer satisfaction risk |
| Negative Profit Deal | Business Loss | Deals with negative profit - direct financial loss |
| Exceptional Posting | Accounting Risk | Unusual accounting entries - may indicate errors |
| Data Exchange Failure | Integration Risk | Critical integration failure - impacts operations |
| Incomplete Service | Service Delivery | Service delivery incomplete - customer impact |
| Overdue Order/Delivery | Customer Impact | Overdue orders/deliveries - customer satisfaction risk |

**Key Nuance:**
- Unbilled deliveries represent direct revenue risk - money is owed but not collected
- Process bottlenecks can cascade to other processes
- Negative profit deals indicate pricing or cost calculation errors

---

## MEDIUM Severity (Base Score: 60)

**Characteristic:** Process deviations, approval delays, or pricing issues that need review but may be acceptable with proper documentation.

| Alert Type | Risk Category | Why Medium |
|-----------|--------------|------------|
| Payment Terms Mismatch | Process Error | Process deviation - needs review for documentation |
| Over Delivery Tolerance | Control Bypass | Control bypass potential - may be acceptable |
| Approval Delay / Waiting Approval | Process Delay | Process delay - may be normal in approval workflows |
| Pricing Issue | Pricing Anomaly | Pricing anomaly - needs review |
| Margin Issue | Margin Concern | Margin concern - needs review |
| Goods Receipt Issue | GR/IR Issue | GR/IR reconciliation issues |
| Purchase/Sales Order Issue | Order Process | Order process issues - needs review |
| Delay / Anomaly | General | General delays/anomalies - needs review |

**Key Nuance:**
- Process deviations may be acceptable in thin-staffed organizations
- Approval delays may be normal in complex approval workflows
- Pricing issues need review but may be legitimate business decisions

---

## LOW Severity (Base Score: 50)

**Characteristic:** Tracking/housekeeping items - no immediate risk indicator, but useful for trend monitoring.

| Alert Type | Risk Category | Why Low |
|-----------|--------------|---------|
| Credit Limit Changed | Business Decision | Business decision - tracking for audit |
| Inactive Vendor/Customer (no balance) | Housekeeping | Housekeeping - no financial impact |
| Master Data Change | Informational | Master data updates - informational |
| Vendor/Customer Created | Tracking | Entity creation - tracking for awareness |

**Key Nuance:**
- These are informational/tracking alerts
- Useful for trend monitoring and audit trails
- No immediate action required

---

## Severity Decision Flow

```
CRITICAL: System-wide failures, critical breakdowns
→ Requires IMMEDIATE review

HIGH:    Significant business process issues, revenue risk
         → Requires PROMPT review within hours/day

MEDIUM:  Process deviations, approval delays
         → Requires REVIEW for documentation/audit

LOW:     Tracking/housekeeping - no immediate risk
         → Requires AWARENESS for trend monitoring
```

---

## Important Distinctions

| What Alert Says | What It Means | Severity Impact |
|-----------------|---------------|-----------------|
| "Unbilled delivery" | Revenue not collected | HIGH (revenue risk) |
| "Process bottleneck" | Critical process stuck | HIGH (operational impact) |
| "Negative profit" | Deal losing money | HIGH (financial loss) |
| "Approval delay" | Process taking longer | MEDIUM (may be normal) |
| "Pricing issue" | Pricing anomaly | MEDIUM (needs review) |
| "Credit limit changed" | Business decision | LOW (tracking) |

---

## Scoring Factors Summary

This classification is **Factor 1 (Alert Nature)** of the overall severity calculation.

The final risk score also incorporates:
- **Factor 2:** Count (normalized by BACKDAYS)
- **Factor 3:** Monetary amounts involved
- **Factor 4:** Focus area multiplier (1.0 for BUSINESS_CONTROL - standard risk)
- **Factor 5:** Quantity/pattern adjustments

```
Final Score = (Factor1 + Factor2 + Factor3 + Factor5) × Factor4
```

---

## Implementation Status

- [x] Severity base scores defined (90/75/60/50)
- [x] Alert-type to severity mapping implemented
- [x] Patterns compiled for efficient matching
- [ ] Unit tests created
- [ ] Tested with real BUSINESS_CONTROL alerts
- [ ] Refinement based on user feedback

---

## Pattern Matching Examples

| Alert Name | Matched Pattern | Severity | Reasoning |
|-----------|----------------|----------|-----------|
| "Unbilled Delivery Alert" | `unbilled.*delivery` | HIGH | Revenue risk - goods shipped but not invoiced |
| "Process Bottleneck Detected" | `process.*bottleneck` | HIGH | Critical process stuck |
| "Stuck Purchase Orders" | `stuck.*order` | HIGH | Orders blocked - customer impact |
| "Negative Profit Deals" | `negative.*profit` | HIGH | Direct financial loss |
| "Payment Terms Mismatch" | `payment.*terms.*mismatch` | MEDIUM | Process deviation - needs review |
| "Approval Delay Warning" | `approval.*delay` | MEDIUM | Process delay - may be normal |
| "Credit Limit Changed" | `credit limit changed` | LOW | Business decision - tracking |

---

## Related Documentation

- **[BUSINESS_PROTECTION.md](BUSINESS_PROTECTION.md)** - Similar structure for fraud/security alerts
- **[QUANTITATIVE_ALERT_WORKFLOW.md](../th-context/analysis-rules/QUANTITATIVE_ALERT_WORKFLOW.md)** - Overall analysis workflow
- **[scoring_engine.py](../../../backend/app/services/content_analyzer/scoring_engine.py)** - Implementation

