# Concentration Metrics Backend - Code References

**Feature:** 08-concentration-metrics-backend  
**Last Updated:** 2025-12-12

---

## Code Locations

### API Endpoint

**File:** `backend/app/api/alert_dashboard.py`

**Field Inclusion:**
```177:179:backend/app/api/alert_dashboard.py
concentration_metrics=[
    ConcentrationMetricResponse.model_validate(m)
    for m in analysis.concentration_metrics
],
```

**Eager Loading:**
```146:146:backend/app/api/alert_dashboard.py
joinedload(AlertAnalysis.concentration_metrics),
```

### Schema Definition

**File:** `backend/app/schemas/alert_dashboard.py`

**Field in Response Schema:**
```332:332:backend/app/schemas/alert_dashboard.py
concentration_metrics: List[ConcentrationMetricResponse] = []
```

**ConcentrationMetricResponse:**
```237:258:backend/app/schemas/alert_dashboard.py
class ConcentrationMetricBase(BaseModel):
    dimension_type: str = Field(..., max_length=50, description="SALES_ORG, CUSTOMER, REGION")
    dimension_code: str = Field(..., max_length=50)
    dimension_name: Optional[str] = Field(None, max_length=255)
    record_count: Optional[int] = None
    value_local: Optional[Decimal] = None
    value_usd: Optional[Decimal] = None
    percentage_of_total: Optional[Decimal] = None
    rank: Optional[int] = None


class ConcentrationMetricCreate(ConcentrationMetricBase):
    alert_analysis_id: int


class ConcentrationMetricResponse(ConcentrationMetricBase):
    id: int
    alert_analysis_id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

### Database Model

**File:** `backend/app/models/concentration_metric.py`

---

## Related Code

### Frontend Usage

**Used by:** `frontend/src/pages/alert-discoveries/features/detail-panel/DiscoveryDetailPanel.tsx`

The frontend displays concentration metrics in a table.

