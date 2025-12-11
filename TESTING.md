# Treasure Hunt Analyzer - Testing Guide

Complete testing guide for the THA system. Choose your testing path based on your setup.

---

## Quick Navigation

- [Quick Test (5 min)](#quick-test-5-minutes) - Fastest way to verify system works
- [Full Testing](#full-testing-checklist) - Comprehensive testing checklist
- [Without Docker](#testing-without-docker) - Manual setup if Docker unavailable
- [Troubleshooting](#troubleshooting) - Common issues and fixes

---

## Quick Test (5 Minutes)

Fastest way to verify the system works end-to-end.

### Prerequisites

- Docker Desktop installed and running
- Sample Skywind files (4C alerts or SoDA reports)

### Step 1: Start the System (2 minutes)

```bash
cd treasure-hunt-analyzer
docker compose up -d
```

Wait for containers to start (~30 seconds), then initialize database:

```bash
docker compose exec backend python -m app.utils.init_db
```

**Verify services are running:**
```bash
docker compose ps
curl http://localhost:3011/health
```

Expected: All containers "Up" and health endpoint returns `{"status":"healthy"}`

### Step 2: Test File Upload (3 minutes)

**Option A: Using Swagger UI (Easiest)**

1. Open http://localhost:3011/docs
2. Find `POST /api/v1/ingestion/upload`
3. Click "Try it out"
4. Upload a Skywind 4C alert Excel file
5. Click "Execute"
6. Copy the `data_source_id` from response

**Option B: Using curl**

```bash
curl -X POST "http://localhost:3011/api/v1/ingestion/upload" \
  -F "file=@path/to/your/alert.xlsx"
```

### Step 3: Run Analysis (2 minutes)

**Using Swagger UI:**
1. Find `POST /api/v1/analysis/run`
2. Click "Try it out"
3. Enter: `{"data_source_id": 1}` (use your actual ID)
4. Click "Execute"

**Using curl:**
```bash
curl -X POST "http://localhost:3011/api/v1/analysis/run" \
  -H "Content-Type: application/json" \
  -d '{"data_source_id": 1}'
```

### Step 4: View Results (3 minutes)

**Check Frontend:**
1. Open http://localhost:3010
2. Dashboard should show data in cards and charts
3. Click "Findings" in sidebar
4. Click on a finding to see details
5. Test "Reports" page export

**Check API:**
```bash
# Get all findings
curl http://localhost:3011/api/v1/analysis/findings

# Get analysis runs
curl http://localhost:3011/api/v1/analysis/runs
```

### ✅ Success Criteria

- [ ] File upload returns `data_source_id`
- [ ] Analysis returns `total_findings` > 0
- [ ] Frontend dashboard loads without errors
- [ ] Findings appear in table
- [ ] Charts render (even if empty)

---

## Full Testing Checklist

Comprehensive testing checklist for systematic validation.

### 1. System Startup Testing

#### Docker Compose
- [ ] Run `docker compose up -d`
- [ ] All containers start successfully (`docker compose ps`)
- [ ] No errors in logs (`docker compose logs`)

#### Database Initialization
- [ ] Database init completes without errors
- [ ] 6 focus areas created
- [ ] Issue types created
- [ ] Seed data loaded

#### Health Checks
- [ ] Backend: `curl http://localhost:3011/health`
- [ ] Frontend: http://localhost:3010 loads
- [ ] API docs: http://localhost:3011/docs accessible

### 2. Backend API Testing

#### File Upload Endpoint
- [ ] Upload 4C alert Excel file
- [ ] Upload SoDA report Excel file
- [ ] Upload PDF file (if available)
- [ ] Upload CSV file (if available)
- [ ] Error handling: invalid file format
- [ ] Error handling: missing file

#### Data Source Endpoints
- [ ] List all data sources
- [ ] Get specific data source by ID
- [ ] Metadata is correct (filename, size, status)

#### Analysis Endpoints
- [ ] Run analysis on uploaded file
- [ ] Analysis run created successfully
- [ ] Findings created
- [ ] List all analysis runs
- [ ] Get specific analysis run details

#### Findings Endpoint
- [ ] Get all findings
- [ ] Filter by focus area
- [ ] Filter by severity
- [ ] Filter by status
- [ ] Filter by date range
- [ ] Combine multiple filters

### 3. File Parser Testing

#### 4C Alert Parser
- [ ] Alert metadata extracted correctly
- [ ] Alert records saved to database
- [ ] Field mappings correct
- [ ] Test with different 4C alert types

#### SoDA Report Parser
- [ ] Parameters sheet parsed
- [ ] KPIs sheet parsed
- [ ] Result sheet parsed
- [ ] Report metadata extracted

### 4. Analysis Engine Testing

#### Classification
- [ ] Findings classified into correct focus areas
- [ ] Classification confidence scores reasonable
- [ ] Issue types assigned correctly
- [ ] Test with different alert types

#### Risk Scoring
- [ ] Risk scores calculated
- [ ] Risk levels assigned (Critical/High/Medium/Low)
- [ ] Risk assessments created
- [ ] Scores are reasonable

#### Money Loss Calculation
- [ ] Money loss calculated (if LLM configured)
- [ ] Fallback calculations work (without LLM)
- [ ] Confidence scores present
- [ ] Amounts are reasonable

### 5. Frontend Testing

#### Dashboard Page
- [ ] Loads without errors
- [ ] KPI cards show correct numbers
- [ ] Focus Area chart renders
- [ ] Risk Level chart renders
- [ ] Findings table displays data
- [ ] Filters work
- [ ] Chart updates with filters
- [ ] Table updates with filters

#### Upload Page
- [ ] File input accepts files
- [ ] Upload works
- [ ] Progress indicator shows
- [ ] Success/error messages display
- [ ] Automatic analysis triggers

#### Findings Page
- [ ] All findings display
- [ ] Filters work
- [ ] Table sorting works
- [ ] Clicking row navigates to detail

#### Finding Detail Page
- [ ] Details display correctly
- [ ] Risk assessment shows
- [ ] Money loss shows
- [ ] Back button works

#### Reports Page
- [ ] Report preview shows
- [ ] PDF export works
- [ ] Excel export works
- [ ] Exported files contain correct data

### 6. Integration Testing

#### Complete Workflow
- [ ] Upload → Analysis → Dashboard shows data
- [ ] Filter → View detail → Export report
- [ ] Multiple uploads → All appear
- [ ] Data persists after page refresh

#### Data Consistency
- [ ] Database matches API responses
- [ ] Frontend matches API data
- [ ] Charts reflect actual data
- [ ] Reports match displayed data

### 7. Error Handling

#### Backend Errors
- [ ] Invalid file format handled gracefully
- [ ] Missing file handled
- [ ] Database errors handled
- [ ] Proper HTTP status codes returned

#### Frontend Errors
- [ ] Network errors handled
- [ ] API errors displayed to user
- [ ] Loading states shown
- [ ] Empty states displayed

### 8. Performance

#### Backend
- [ ] File upload < 30 seconds
- [ ] Analysis < 60 seconds
- [ ] API responses < 1 second

#### Frontend
- [ ] Page loads < 3 seconds
- [ ] Charts render smoothly
- [ ] Table scrolling smooth

### 9. Browser Compatibility

- [ ] Chrome/Edge works
- [ ] Firefox works
- [ ] Safari works (if on Mac)
- [ ] Mobile browser responsive

---

## Testing Without Docker

If Docker is unavailable, test manually with local setup.

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Step 1: Install PostgreSQL

1. Download from https://www.postgresql.org/download/
2. Install with default settings
3. Note the password for `postgres` user
4. PostgreSQL runs on `localhost:5432`

### Step 2: Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/treasure_hunt_analyzer
SECRET_KEY=test-secret-key
DEBUG=True
STORAGE_TYPE=local
STORAGE_PATH=./storage
```

Create database:
```sql
CREATE DATABASE treasure_hunt_analyzer;
```

Initialize and start:
```bash
python -m app.utils.init_db
uvicorn app.main:app --reload
```

Backend runs on http://localhost:3011

### Step 3: Set Up Frontend

Open new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

Frontend runs on http://localhost:3010

### Step 4: Test

Follow [Quick Test](#quick-test-5-minutes) steps above.

---

## Troubleshooting

### Docker Issues

**Docker command not recognized:**
1. Check Docker Desktop is running (system tray icon)
2. Restart terminal (PATH updated when Docker starts)
3. Try `docker --version` in new terminal
4. If still failing, restart computer

**Port already in use:**
```bash
# Stop containers
docker compose down

# Or change ports in docker-compose.yml
```

**Containers won't start:**
```bash
# View logs
docker compose logs backend
docker compose logs frontend
docker compose logs postgres

# Rebuild
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Database Issues

**Connection error:**
```bash
# Verify PostgreSQL running
docker compose ps

# Re-initialize database
docker compose exec backend python -m app.utils.init_db
```

**No data in tables:**
```bash
# Check seed data loaded
docker compose exec backend python -c "from app.core.database import engine; from sqlalchemy import text; result = engine.connect().execute(text('SELECT COUNT(*) FROM focus_areas')); print(result.scalar())"
```

### Frontend Issues

**Not loading:**
- Check backend is running: `curl http://localhost:3011/health`
- Check browser console for errors (F12)
- Clear browser cache: Ctrl+Shift+Delete
- Hard refresh: Ctrl+Shift+R

**Changes not visible:**
```bash
# Rebuild frontend
cd frontend
npm run build

# Or restart dev server
npm run dev
```

### File Upload Issues

**Upload fails:**
- Verify file format supported (XLSX, PDF, CSV, DOCX)
- Check file path is correct
- View backend logs: `docker compose logs backend`

**Analysis fails:**
- Check database initialized
- Verify focus areas exist
- Check backend logs for errors

### Performance Issues

**Slow uploads:**
- Check file size (very large files take time)
- Verify disk space available
- Check network if remote

**Slow analysis:**
- Normal for first run (database warming up)
- Check CPU usage (should not be 100%)
- View logs for stuck operations

---

## Quick Verification Commands

```bash
# Check all services running
docker compose ps

# Check backend health
curl http://localhost:3011/health

# Check database connection
docker compose exec backend python -c "from app.core.database import engine; engine.connect(); print('OK')"

# View recent logs
docker compose logs --tail=50

# Check focus areas loaded
curl http://localhost:3011/api/v1/dashboard/kpis
```

---

## Expected Test Results

### For 4C Alert (Example: Long Time Logged On Users)
- **Focus Area**: ACCESS_GOVERNANCE
- **Issue Type**: LONG_SESSION
- **Risk Level**: Medium to High
- **Findings**: One finding per user session

### For SoDA Report (Example: Access Violation Review)
- **Focus Area**: ACCESS_GOVERNANCE
- **Issue Type**: SOD_VIOLATION or UNAUTHORIZED_ACCESS
- **Risk Level**: High to Critical
- **Findings**: Based on violations in report

---

## Next Steps After Testing

**If tests pass:**
1. Test with different file types
2. Test filtering and sorting
3. Test report export
4. Review data accuracy

**If tests fail:**
1. Check logs for error messages
2. Verify prerequisites met
3. Try rebuilding containers
4. Check this troubleshooting guide

---

*For detailed deployment, see [DEPLOYMENT.md](DEPLOYMENT.md)*  
*For development workflow, see [CLAUDE.md](CLAUDE.md)*

