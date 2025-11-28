# Negative Profit Deal - Alert Analysis

> **TEMPLATE: Quantitative Alert Analysis**

---

## BUSINESS CONTEXT

> **Business Purpose:** This alert identifies sales transactions where products are sold below their cost price, resulting in direct financial loss to the company. It helps detect pricing errors, unauthorized discounts, or potential fraud schemes where employees may be favoring specific customers through below-cost pricing. Every flagged transaction represents real money lost that cannot be recovered.

### What This Alert Monitors

**Sales Order Pricing** - Detects when products are sold below cost (NETWR < WAVWR), resulting in direct financial loss on each transaction.

### Why It Matters

| Risk Type | Business Impact |
|-----------|-----------------|
| **Revenue Leakage** | Every flagged item = money lost |
| **Pricing Control Gap** | No hard stop preventing below-cost sales |
| **Potential Fraud** | Manual overrides to favor specific customers |

### Interpreting the Findings

| Pattern | Legitimate Cause | Red Flag |
|---------|------------------|----------|
| Zero-price items | Free samples, project billing separate | Goods given away without approval |
| Manual override + loss | Customer negotiation, strategic deal | Kickbacks, unauthorized discounting |
| Single large loss | One-time market entry pricing | **Almost always requires investigation** |

---

## EXECUTIVE SUMMARY

### Alert Identity

| | |
|---|---|
| **Alert Name** | Negative Profit Deal |
| **Alert ID** | 200025_001441 |
| **Module** | SD (Sales & Distribution) |
| **Category** | Applications |
| **Subcategory** | SD Alerts |

### Execution Context

| | |
|---|---|
| **Source System** | Production S4 (PS4) |
| **Created** | 28.10.2025 at 14:25 by SKYWATCH |
| **Last Executed** | 27.11.2025 at 09:42 by ILIYAR |
| **Exception Indicator** | SW_10_01_SALES_REV |

### Alert Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| BACKDAYS | 365 | Data from past 365 days |
| WAERK | USD | Document Currency = USD only |
| VBTYP | C | SD document category = Order |
| ABGRU | (none) | No rejection reason filter |
| UEPOS | (none) | No higher-level item filter |

### THE BOTTOM LINE

| | |
|---|---|
| **Total Financial Loss** | **$14,152,997** |
| **Records Affected** | 2,044 line items |
| **Severity** | CRITICAL |
| **Fraud Indicator** | YES - Requires Investigation |

### WHAT HAPPENED

2,044 sales order line items were sold **below cost**, resulting in $14.15M direct financial loss. 59% are zero-price items, 39% involve manual price overrides. Single largest loss: $8.1M to KAMURU TRADING COMPANY.

### TOP 3 FINDINGS

1. **$8.1M single transaction** to KAMURU TRADING COMPANY (manual override) - **INVESTIGATE IMMEDIATELY**
2. **81% of total loss** concentrated in KE01 (Kenya MRM)
3. **100% of top 10 losses** are manual price overrides

### IMMEDIATE ACTIONS REQUIRED

1. **URGENT**: Investigate KAMURU TRADING COMPANY - $8.1M loss on 14 items
2. Review all manual price changes exceeding $50K
3. Audit KE01 sales organization processes

---

## KEY METRICS

### Financial Impact

| Metric | Value |
|--------|-------|
| Total Loss | $14,152,997 |
| Total Revenue Recorded | $11,808,927 |
| Total Cost | $25,961,924 |
| Average Loss Per Item | $6,923 |
| Maximum Single Loss | $8,105,816 |

### Volume

| Metric | Value |
|--------|-------|
| Line Items | 2,044 |
| Sales Orders | 466 |
| Customers | 128 |
| Sales Organizations | 6 |

### Patterns

| Pattern | Count | % |
|---------|-------|---|
| Zero-Price Items (NETWR=0) | 1,205 | 59% |
| Manual Price Override | 796 | 39% |
| System-Calculated Loss | 1,246 | 61% |

---

## CONCENTRATION ANALYSIS

### By Sales Organization

| Rank | Org | Name | Loss | % of Total |
|------|-----|------|------|------------|
| 1 | **KE01** | MRM Sales Org (Kenya) | **$11,446,868** | **81%** |
| 2 | TZ01 | Tanzania | $1,392,422 | 10% |
| 3 | UG01 | UBL Sales Org | $829,884 | 6% |
| 4 | KE03 | SBS Sales Org | $330,235 | 2% |
| 5 | ZM01 | Zambia | $124,845 | <1% |
| 6 | RW01 | Rwanda | $28,743 | <1% |

**Insight**: KE01 has only 21% of items but 81% of the loss.

### By Customer (Top 5)

| Rank | Customer | Loss | Items | Manual? |
|------|----------|------|-------|---------|
| 1 | **KAMURU TRADING COMPANY** | **$8,148,934** | 14 | Yes |
| 2 | EASTERN HOPE LTD | $550,728 | 2 | Yes |
| 3 | BINA TRADES PVT LTD | $479,024 | 1 | Yes |
| 4 | ADLER STEEL LTD | $448,189 | 1 | Yes |
| 5 | DIEUDO TRADING | $392,424 | 20 | Yes |

**Insight**: Top 5 = $10M (71% of total). All involve manual price changes.

### Largest Single Transactions

| Loss | Customer | Material | Manual? |
|------|----------|----------|---------|
| **$8,105,816** | KAMURU TRADING | P-R.H.S 60X40-1.15MM-5.8M | **Yes** |
| $479,024 | BINA TRADES | USED STEEL ROLLS | Yes |
| $448,189 | ADLER STEEL | USED STEEL ROLLS | Yes |
| $290,991 | EASTERN HOPE | HR SLIT PROFILED PACK | Yes |
| $259,738 | EASTERN HOPE | HR SLIT PROFILED PACK | Yes |

**Critical**: 100% of top losses are manual overrides.

---

## RISK ASSESSMENT

### Classification

| Attribute | Value | Reasoning |
|-----------|-------|-----------|
| Focus Area | BUSINESS_CONTROL | Revenue/margin leakage from process failure |
| Severity | CRITICAL | $14M+ loss, fraud indicators present |
| Risk Score | 95/100 | High financial impact + concentration + fraud pattern |
| Fraud Indicator | YES | Manual overrides, single large transaction, customer concentration |

### Risk Indicators

| Risk | Evidence | Action |
|------|----------|--------|
| **Potential Fraud** | $8.1M to one customer via manual override | Investigate relationship |
| **Process Gap** | No hard stop on below-cost pricing | Implement validation |
| **Concentration** | 81% loss in KE01, 58% to one customer | Review controls |
| **Override Abuse** | 100% top losses = manual changes | Add approval workflow |

---

## RECOMMENDED ACTIONS

### Immediate (24-48 hours)

1. **Investigate KAMURU TRADING COMPANY**
   - Review $8.1M transaction details
   - Check customer relationship/ownership
   - Identify who approved the price override

2. **Review KE01 Sales Organization**
   - Why 81% of loss concentrated here?
   - Who has manual pricing authority?

### Short-term (1-2 weeks)

3. **Audit all manual price changes > $50K**
   - Pull list of approvers
   - Check authorization levels

4. **Review Project WBS Orders (Z004)**
   - 1,118 items with $0 pricing
   - Likely configuration issue

### Process Improvements

5. **Implement hard stop** for pricing below cost threshold
6. **Add approval workflow** for discounts exceeding X%
7. **Create exception report** for manual price overrides

---

## DETECTION LOGIC

**What the alert detects**: Sales order line items where Net Value < Cost

```
VBAP-NETWR < VBAP-WAVWR
```

Where:
- **NETWR** = Net Value (what customer pays)
- **WAVWR** = Cost (what it cost to produce/buy)
- **MPROK = 'A'** = Manual price change flag

---

## ARTIFACTS ANALYZED

| Artifact | File |
|----------|------|
| Code | `Code_Negative Profit Deal_200025_001441.txt` |
| Summary | `Summary_Negative Profit Deal_200025_001441_USD_ONLY.csv` |
| Explanation | `Explanation_Negative Profit Deal_200025_001441.docx` |
| Metadata | `Metadata _Negative Profit Deal_200025_001441.xlsx` |

**Location**: `docs/skywind-4c-alerts-output/Applications/SD/200025_001441 - Negative Profit Deal/`

---

## CONTENT ANALYZER OUTPUT

```json
{
  "alert_id": "200025_001441",
  "alert_name": "Negative Profit Deal",
  "module": "SD",
  "classification": {
    "focus_area": "BUSINESS_CONTROL",
    "severity": "CRITICAL",
    "risk_score": 95,
    "fraud_indicator": true
  },
  "metrics": {
    "record_count": 2044,
    "total_loss": 14152997,
    "max_single_loss": 8105816,
    "currency": "USD"
  },
  "concentration": {
    "top_org": {"code": "KE01", "loss": 11446868, "pct": 81},
    "top_customer": {"name": "KAMURU TRADING COMPANY", "loss": 8148934}
  },
  "key_finding": "2,044 sales items sold below cost. $8.1M single transaction to one customer via manual override requires immediate investigation.",
  "recommended_actions": [
    "Investigate KAMURU TRADING COMPANY $8.1M transaction",
    "Review KE01 sales org controls",
    "Audit manual price changes > $50K"
  ]
}
```

---

*Analysis Date: 2025-11-27 | Template Version: 1.0*
