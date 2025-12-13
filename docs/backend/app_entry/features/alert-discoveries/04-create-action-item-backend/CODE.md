# Create Action Item Backend - Code References

**Feature:** 04-create-action-item-backend  
**Last Updated:** 2025-12-12

---

## Code Locations

### API Endpoint

**File:** `backend/app/api/alert_dashboard.py`

**Create Endpoint:**
```591:601:backend/app/api/alert_dashboard.py
@router.post("/action-items", response_model=ActionItemResponse)
async def create_action_item(
    action_item: ActionItemCreate,
    db: Session = Depends(get_db)
):
    """Create an action item."""
    db_item = ActionItem(**action_item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return ActionItemResponse.model_validate(db_item)
```

**Update Endpoint:**
```604:626:backend/app/api/alert_dashboard.py
@router.patch("/action-items/{item_id}", response_model=ActionItemResponse)
async def update_action_item(
    item_id: int,
    update: ActionItemUpdate,
    db: Session = Depends(get_db)
):
    """Update an action item (e.g., change status, assign, resolve)."""
    item = db.query(ActionItem).filter(ActionItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")

    update_data = update.model_dump(exclude_unset=True)

    # Handle resolution
    if update_data.get('status') in ['REMEDIATED', 'FALSE_POSITIVE']:
        update_data['resolved_at'] = datetime.utcnow()

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return ActionItemResponse.model_validate(item)
```

**Bulk Create Endpoint:**
```629:640:backend/app/api/alert_dashboard.py
@router.post("/action-items/bulk", response_model=List[ActionItemResponse])
async def create_action_items_bulk(
    action_items: List[ActionItemCreate],
    db: Session = Depends(get_db)
):
    """Create multiple action items at once."""
    db_items = [ActionItem(**a.model_dump()) for a in action_items]
    db.add_all(db_items)
    db.commit()
    for item in db_items:
        db.refresh(item)
    return [ActionItemResponse.model_validate(item) for item in db_items]
```

### Schema Definition

**File:** `backend/app/schemas/alert_dashboard.py`

**Request Schema:**
```265:277:backend/app/schemas/alert_dashboard.py
class ActionItemBase(BaseModel):
    action_type: str = Field(..., max_length=50, description="IMMEDIATE, SHORT_TERM, PROCESS_IMPROVEMENT")
    priority: Optional[int] = Field(None, ge=1, le=5)
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: str = Field("OPEN", max_length=30, description="OPEN, IN_REVIEW, REMEDIATED, FALSE_POSITIVE")
    assigned_to: Optional[str] = Field(None, max_length=100)
    due_date: Optional[date] = None


class ActionItemCreate(ActionItemBase):
    alert_analysis_id: int
```

**Response Schema:**
```286:295:backend/app/schemas/alert_dashboard.py
class ActionItemResponse(ActionItemBase):
    id: int
    alert_analysis_id: int
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
```

### Database Model

**File:** `backend/app/models/action_item.py`

---

## Related Code

### Frontend Usage

**Used by:** `frontend/src/pages/alert-discoveries/features/create-action-item/CreateActionItemModal.tsx`

