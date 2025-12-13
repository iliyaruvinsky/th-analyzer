# Create Action Item Backend - Specification

**Feature:** 04-create-action-item-backend  
**Frontend Feature:** [04-create-action-item](../../../frontend/app_entry/features/alert-discoveries/04-create-action-item/)  
**API Endpoint:** `POST /alert-dashboard/action-items`  
**Status:** ✅ Working

---

## Requirements

### Functional Requirements

1. **Create Action Item**
   - Accept action item data from frontend
   - Validate required fields
   - Link to `alert_analysis_id`
   - Store in database

2. **Support Bulk Creation**
   - Accept multiple action items at once
   - Create all in single transaction

### API Specification

**Endpoint:** `POST /alert-dashboard/action-items`

**Request Body:** `ActionItemCreate`

```python
{
    "alert_analysis_id": int,
    "action_type": str,  # IMMEDIATE, SHORT_TERM, PROCESS_IMPROVEMENT
    "priority": int,  # 1-5
    "title": str,
    "description": str,
    "status": str,  # OPEN, IN_REVIEW, REMEDIATED, FALSE_POSITIVE
    "assigned_to": str,
    "due_date": date
}
```

**Response:** `ActionItemResponse`

**Bulk Endpoint:** `POST /alert-dashboard/action-items/bulk`

**Request Body:** `List[ActionItemCreate]`

**Response:** `List[ActionItemResponse]`

---

## Expected Behavior

1. **Validation**
   - Validate `alert_analysis_id` exists
   - Validate `action_type` is valid enum value
   - Validate `priority` is 1-5
   - Validate `status` is valid enum value

2. **Database Operations**
   - Create `ActionItem` record
   - Set `created_at` timestamp
   - Return created item with ID

3. **Error Handling**
   - Return 404 if `alert_analysis_id` not found
   - Return 400 for validation errors

---

## Related Frontend Feature

The frontend `CreateActionItemModal` component uses this endpoint to create action items from discoveries.

