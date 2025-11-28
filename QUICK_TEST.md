# Quick Test Guide - 10 Minutes

Fastest way to verify the system works end-to-end.

## Prerequisites Check

**Do you have Docker installed?**
- Check: Run `docker --version` in command prompt
- If not installed: See [Installation Options](#installation-options) below

## Step 1: Start the System (2 minutes)

### Option A: With Docker (Recommended)

```bash
cd treasure-hunt-analyzer
docker-compose up -d
```

**Note:** If you get `'docker-compose' is not recognized`, try:
- `docker compose up -d` (newer Docker versions use space instead of hyphen)
- Or install Docker Desktop: https://www.docker.com/products/docker-desktop/

### Option B: Without Docker

See [TESTING_WITHOUT_DOCKER.md](TESTING_WITHOUT_DOCKER.md) for manual setup instructions.

Wait for containers to start (about 30 seconds), then:

```bash
docker-compose exec backend python -m app.utils.init_db
```

**If using `docker compose` (without hyphen):**
```bash
docker compose exec backend python -m app.utils.init_db
```

## Step 2: Test File Upload (3 minutes)

### Option A: Using Swagger UI (Easiest)

1. Open http://localhost:3011/docs in your browser
2. Find `POST /api/v1/ingestion/upload`
3. Click "Try it out"
4. Click "Choose File" and select a Skywind 4C alert Excel file
5. Click "Execute"
6. Copy the `data_source_id` from the response (e.g., `1`)

### Option B: Using curl

```bash
curl -X POST "http://localhost:3011/api/v1/ingestion/upload" \
  -F "file=@../Skywind Output (Real Reports and Alerts)/4C Alerts/Summary_SAFAL SM04 Long Time Logged On Users (24+ hours) SLG_200025_000327.xlsx"
```

Note the `data_source_id` from the response.

## Step 3: Run Analysis (2 minutes)

### Using Swagger UI:

1. In http://localhost:3011/docs, find `POST /api/v1/analysis/run`
2. Click "Try it out"
3. Enter: `{"data_source_id": 1}` (use your actual ID)
4. Click "Execute"
5. Wait for response (should show `total_findings` > 0)

### Using curl:

```bash
curl -X POST "http://localhost:3011/api/v1/analysis/run" \
  -H "Content-Type: application/json" \
  -d "{\"data_source_id\": 1}"
```

## Step 4: View Results (3 minutes)

### Check API Results:

```bash
# Get all findings
curl http://localhost:3011/api/v1/analysis/findings

# Get analysis runs
curl http://localhost:3011/api/v1/analysis/runs
```

### Check Frontend:

1. Open http://localhost:3010 in your browser
2. You should see the Dashboard with:
   - Summary cards showing numbers
   - Charts (may be empty if no data)
   - Findings table
3. Click "Findings" in the sidebar
4. You should see the findings list
5. Click on a finding to see details
6. Click "Reports" to test export

## Installation Options

### Install Docker Desktop

1. **Download:** https://www.docker.com/products/docker-desktop/
2. **Install:** Run the installer
3. **Restart:** Restart your computer
4. **Verify:** Open command prompt and run `docker --version`

**System Requirements:**
- Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
- WSL 2 feature enabled
- Virtualization enabled in BIOS

### Alternative: Test Without Docker

If you can't install Docker, you can test manually:
- See [TESTING_WITHOUT_DOCKER.md](TESTING_WITHOUT_DOCKER.md)
- Requires: Python 3.11+, Node.js 18+, PostgreSQL 15+

## Expected Results

✅ **Success Indicators:**
- File upload returns `data_source_id`
- Analysis returns `total_findings` > 0
- Frontend dashboard loads
- Findings appear in the table
- Charts render (even if empty)

❌ **If Something Fails:**

1. **Backend not responding:**
   ```bash
   docker-compose logs backend
   ```

2. **Frontend not loading:**
   ```bash
   docker-compose logs frontend
   ```

3. **Database errors:**
   ```bash
   docker-compose logs postgres
   docker-compose exec backend python -m app.utils.init_db
   ```

4. **No findings created:**
   - Check if file was parsed: `curl http://localhost:3011/api/v1/ingestion/data-sources`
   - Check analysis run status: `curl http://localhost:3011/api/v1/analysis/runs`
   - Check backend logs: `docker-compose logs backend`

## Quick Verification Commands

```bash
# Check all services are running
docker-compose ps

# Check backend health
curl http://localhost:3011/health

# Check database connection
docker-compose exec backend python -c "from app.core.database import engine; engine.connect(); print('OK')"

# View recent logs
docker-compose logs --tail=50
```

## Next Steps After Quick Test

If the quick test passes:
1. Test with different file types (SoDA reports, PDFs)
2. Test filtering and sorting in frontend
3. Test report export
4. Review the full [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)

If the quick test fails:
1. Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) section
2. Review error messages in logs
3. Verify all prerequisites are met

