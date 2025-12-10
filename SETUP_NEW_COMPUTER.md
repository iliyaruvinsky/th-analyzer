# Setup THA on New Computer

## Prerequisites
- Docker Desktop installed and running
- Git installed

## Step 1: Clone Repository

```bash
git clone https://github.com/iliyaruvinsky/th-analyzer.git tha-new
cd tha-new
```

Or if already cloned:
```bash
cd tha-new
git pull origin main
```

## Step 2: Start Docker Services

```bash
# Build and start all containers
docker compose up -d --build

# Wait 30-60 seconds for services to initialize
# Check status:
docker compose ps
```

Expected output - all services should show "running" or "healthy":
```
NAME           STATUS
tha-postgres   Up (healthy)
tha-backend    Up (healthy)
tha-frontend   Up
```

## Step 3: Initialize Database

```bash
docker compose exec backend python -m app.utils.init_db
```

## Step 4: Verify Services

```bash
# Check backend health
curl http://localhost:3011/health
```

## Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3010 |
| Backend API | http://localhost:3011 |
| Swagger Docs | http://localhost:3011/docs |

---

# Prompt for Claude Code Agent

Copy everything below this line and paste into Claude Code:

---

I'm continuing development on THA project. Just set up Docker services on this new computer.

## Setup Completed
- Cloned repo from https://github.com/iliyaruvinsky/th-analyzer.git
- Ran: `docker compose up -d --build`
- Initialized DB: `docker compose exec backend python -m app.utils.init_db`

## Previous Session Summary (2025-12-10)
Added 4 features to Critical Discoveries detail panel:
1. **Alert Explanation** - business_purpose text below alert title
2. **Output Popover** - shows raw_summary_data JSON
3. **Params Popover** - shows parameters JSON from Metadata
4. **Collapsible Sidebar Filters** - Focus Area, Module, Severity
5. **Dynamic Risk Score** - threshold-based explanation text

## Layout Fixes Applied (Need Verification)
- Removed blue background from explanation box (now transparent gray italic)
- Repositioned Output/Params buttons inline with title row
- Fixed title row alignment

## Your First Task
1. Navigate browser to http://localhost:3010/alert-discoveries/200025_001355
2. Take a screenshot of the detail panel
3. Verify the layout:
   - Explanation text should be gray/italic (NO blue background box)
   - Output/Params buttons should be INLINE with title (not on separate row below)
   - "Create Action Item" button on the right
   - Collapsible "FILTERS" section in sidebar works

## If Layout Still Has Issues
CSS fixes are in these files:
- `frontend/src/pages/AlertDashboard.css` (lines 877-908) - explanation box styles
- `frontend/src/components/DiscoveryDetailPanel.tsx` (lines 54-93) - button positioning

## Key Documentation
- Read `llm_handover.md` for full project context and changelog
- Read `CLAUDE.md` for development guidelines

## Expected UI Layout
```
+------------------------------------------------------------------+
|  Alert Title                    [Output] [Params] [+ Action]     |
|  i Business purpose explanation text (gray italic)               |
+------------------------------------------------------------------+
|  ! Fraud Indicator Detected - Immediate Review Required          |
+------------------------------------------------------------------+
|  MODULE | SEVERITY | RECORDS | PERIOD | FINANCIAL EXPOSURE       |
+------------------------------------------------------------------+
```

Start by taking a screenshot of the current UI state and report what you see.
