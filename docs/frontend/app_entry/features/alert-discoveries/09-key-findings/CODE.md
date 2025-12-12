# Key Findings - Code Reference

**Feature:** 09-key-findings  
**Location:** `DiscoveryDetailPanel` component

---

## File Locations

### Implementation

- **File:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`
- **Lines:** 161-187 (table), 235 (fallback)

### Usage

**In DiscoveryDetailPanel.tsx:**
```typescript
{discovery.key_findings && discovery.key_findings.length > 0 && (
  <div className="findings-block">
    <h4 className="findings-title">KEY FINDINGS</h4>
    <table className="findings-table">
      <thead>
        <tr>
          <th className="col-rank">#</th>
          <th className="col-finding">Finding</th>
          <th className="col-category">Category</th>
        </tr>
      </thead>
      <tbody>
        {discovery.key_findings
          .sort((a, b) => a.finding_rank - b.finding_rank)
          .map((finding) => (
            <tr key={finding.id}>
              <td className="cell-rank">{finding.finding_rank}</td>
              <td className="cell-finding">{finding.finding_text}</td>
              <td className="cell-category">
                <span className="category-tag">{finding.finding_category || 'General'}</span>
              </td>
            </tr>
          ))}
      </tbody>
    </table>
  </div>
)}
```

---

## Data Source

**Field:** `discovery.key_findings`  
**Type:** `KeyFinding[]`  
**Source:** `AlertAnalysis.key_findings` from backend

**Backend:** `backend/app/api/alert_dashboard.py` (lines 181-184)

---

## Data Structure

```typescript
interface KeyFinding {
  id: number;
  finding_rank: number;
  finding_text: string;
  finding_category?: string;
}
```

---

## CSS Classes

- `.findings-block` - Container
- `.findings-table` - Table
- `.col-rank` - Rank column
- `.col-finding` - Finding text column
- `.col-category` - Category column
- `.category-tag` - Category badge

**Location:** `frontend/src/pages/AlertDashboard.css`

---

## Related Files

- Analysis reports in `docs/analysis/` - Should link to these

