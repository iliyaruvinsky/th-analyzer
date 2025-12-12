# Risk Score Explanation - Analysis

**Feature:** 07-risk-score  
**Date:** 2025-12-11  
**Status:** ⚠️ Not real explanation

---

## Current State

### What Works

- ✅ Risk score displayed in KPI metrics
- ✅ Shows numeric value (0-100)
- ✅ Generic categorization text

### Issues Identified

1. **Hardcoded Text**
   - Just categorization based on ranges:
     - `>= 70`: "High Risk Alert: Score X/100 indicates urgent review needed"
     - `40-69`: "Moderate Risk: Score X/100 - monitor and investigate"
     - `< 40`: "Low Risk: Score X/100 - routine monitoring recommended"
   - Not a real explanation

2. **Missing Information**
   - No explanation of HOW score was calculated
   - No factors that contributed
   - No link to scoring methodology
   - No context-specific reasoning

---

## Code Location

**Component:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`

**Key Code:**
```typescript
// Risk score display (lines 242-248)
if (discovery.risk_score) {
  metrics.push(
    <div key="risk" className="kpi-metric-card accent">
      <span className="kpi-metric-value">{discovery.risk_score}</span>
      <span className="kpi-metric-label">RISK SCORE</span>
    </div>
  );
}

// Hardcoded explanation (lines 256-265)
{discovery.risk_score && discovery.risk_score >= 70 && (
  <p className="risk-warning"><strong>High Risk Alert:</strong> Score {discovery.risk_score}/100 indicates urgent review needed</p>
)}
```

---

## Recommendations

1. **Real Explanation**
   - Show calculation methodology
   - Display contributing factors
   - Link to scoring rules documentation

2. **Context-Specific**
   - Adapt explanation to alert type
   - Show relevant factors
   - Provide actionable insights

3. **Link to Methodology**
   - Link to `docs/scoring-rules/BUSINESS_PROTECTION.md`
   - Show base scores and multipliers
   - Explain normalization

