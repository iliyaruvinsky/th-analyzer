# Quick Start Guide

## Fastest Way to Test (5 minutes)

### 1. Start the system
```bash
cd treasure-hunt-analyzer
docker compose up -d
```

### 2. Initialize database
```bash
docker compose exec backend python -m app.utils.init_db
```

### 3. Test with a sample file

**Option A: Using curl**
```bash
curl -X POST "http://localhost:3011/api/v1/ingestion/upload" \
  -F "file=@../Skywind Output (Real Reports and Alerts)/4C Alerts/Summary_SAFAL SM04 Long Time Logged On Users (24+ hours) SLG_200025_000327.xlsx"
```

**Option B: Using Python script**
```bash
python test_upload.py "../Skywind Output (Real Reports and Alerts)/4C Alerts/Summary_SAFAL SM04 Long Time Logged On Users (24+ hours) SLG_200025_000327.xlsx"
```

**Option C: Using Swagger UI**
1. Open http://localhost:3011/docs
2. Find `/api/v1/ingestion/upload`
3. Click "Try it out"
4. Upload a file
5. Copy the `data_source_id` from response
6. Use `/api/v1/analysis/run` to analyze it

### 4. View results
- **API Docs**: http://localhost:3011/docs
- **Frontend**: http://localhost:3010
- **Health Check**: http://localhost:3011/health

## What to Expect

After uploading a 4C alert file:
- File is parsed and stored
- Alert metadata is extracted
- Data rows are stored in database

After running analysis:
- Findings are created and classified
- Risk scores are calculated
- Issue types are assigned
- Findings are grouped by issue type

## Common Issues

**Port already in use?**
```bash
# Stop existing containers
docker compose down

# Or change ports in docker compose.yml
```

**Database connection error?**
- Check PostgreSQL is running in Docker
- Verify DATABASE_URL in backend/.env

**File upload fails?**
- Check file path is correct
- Verify file format is supported (XLSX, PDF, CSV, DOCX)
- Check backend logs: `docker compose logs backend`

