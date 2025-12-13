# Key Findings Backend - Code References

**Feature:** 09-key-findings-backend  
**Last Updated:** 2025-12-12

---

## Code Locations

### API Endpoint

**File:** `backend/app/api/alert_dashboard.py`

**Field Inclusion:**
```181:183:backend/app/api/alert_dashboard.py
key_findings=[
    KeyFindingResponse.model_validate(f)
    for f in analysis.key_findings
],
```

**Eager Loading:**
```147:147:backend/app/api/alert_dashboard.py
joinedload(AlertAnalysis.key_findings),
```

### Schema Definition

**File:** `backend/app/schemas/alert_dashboard.py`

**Field in Response Schema:**
```333:333:backend/app/schemas/alert_dashboard.py
key_findings: List[KeyFindingResponse] = []
```

**KeyFindingResponse:**
```213:230:backend/app/schemas/alert_dashboard.py
class KeyFindingBase(BaseModel):
    finding_rank: int = Field(..., ge=1, description="Rank (1, 2, 3)")
    finding_text: str = Field(..., description="Finding description")
    finding_category: Optional[str] = Field(None, max_length=50, description="Concentration, Anomaly, Data Quality, Process Gap")
    financial_impact_usd: Optional[Decimal] = None


class KeyFindingCreate(KeyFindingBase):
    alert_analysis_id: int


class KeyFindingResponse(KeyFindingBase):
    id: int
    alert_analysis_id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

### Database Model

**File:** `backend/app/models/key_finding.py`

---

## Related Code

### Frontend Usage

**Used by:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`

The frontend displays key findings in a list.

