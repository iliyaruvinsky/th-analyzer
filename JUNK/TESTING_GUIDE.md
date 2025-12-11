# Treasure Hunt Analyzer - Testing Guide

## Prerequisites

1. **Python 3.11+** installed
2. **Node.js 18+** installed
3. **PostgreSQL 15+** installed and running (or use Docker)
4. **Docker and Docker Compose** (optional, for easier setup)

## Option 1: Quick Test with Docker Compose (Recommended)

### Step 1: Navigate to project directory
```bash
cd treasure-hunt-analyzer
```

### Step 2: Create environment file
```bash
cd backend
cp .env.example .env
```

Edit `.env` file with your configuration:
```env
DATABASE_URL=postgresql://tha_user:tha_password@postgres:5432/treasure_hunt_analyzer
SECRET_KEY=your-secret-key-here-change-this
DEBUG=True
ENVIRONMENT=development
STORAGE_TYPE=local
STORAGE_PATH=./storage

# Optional: LLM Configuration (for money loss calculation)
OPENAI_API_KEY=your-key-here  # Optional
ANTHROPIC_API_KEY=your-key-here  # Optional
LLM_PROVIDER=openai  # or anthropic
```

### Step 3: Start services with Docker Compose
```bash
cd ..
docker compose up -d
```

This will start:
- PostgreSQL database
- Backend API (port 3011)
- Frontend (port 3010)

### Step 4: Initialize database
```bash
docker compose exec backend python -m app.utils.init_db
```

### Step 5: Access the application
- **Frontend**: http://localhost:3010
- **Backend API**: http://localhost:3011
- **API Documentation**: http://localhost:3011/docs

## Option 2: Manual Setup (Local Development)

### Backend Setup

#### Step 1: Create virtual environment
```bash
cd treasure-hunt-analyzer/backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Configure environment
```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL connection:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/treasure_hunt_analyzer
SECRET_KEY=your-secret-key-here
DEBUG=True
STORAGE_TYPE=local
STORAGE_PATH=./storage
```

#### Step 4: Create PostgreSQL database
```sql
CREATE DATABASE treasure_hunt_analyzer;
```

#### Step 5: Initialize database
```bash
python -m app.utils.init_db
```

#### Step 6: Run database migrations (if needed)
```bash
alembic upgrade head
```

#### Step 7: Start backend server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

#### Step 1: Install dependencies
```bash
cd treasure-hunt-analyzer/frontend
npm install
```

#### Step 2: Start development server
```bash
npm run dev
```

Frontend will be available at http://localhost:3010

## Testing the System

### Test 1: Health Check

```bash
curl http://localhost:3011/health
```

Expected response:
```json
{"status": "healthy"}
```

### Test 2: Upload a Skywind 4C Alert File

Using the sample file from your directory:
```bash
curl -X POST "http://localhost:3011/api/v1/ingestion/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@../Skywind Output (Real Reports and Alerts)/4C Alerts/Summary_SAFAL SM04 Long Time Logged On Users (24+ hours) SLG_200025_000327.xlsx"
```

Or use the Swagger UI at http://localhost:3011/docs:
1. Navigate to `/api/v1/ingestion/upload`
2. Click "Try it out"
3. Choose file
4. Click "Execute"

Expected response includes:
- `data_source_id`: ID of uploaded file
- `status`: "completed" or "error"
- `parse_result`: Contains metadata and parsed data

### Test 3: Upload a SoDA Report

```bash
curl -X POST "http://localhost:3011/api/v1/ingestion/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@../Skywind Output (Real Reports and Alerts)/SoDA Reports/AVR_by_UG01-Ver.00_10.11.25_12_58.xlsx"
```

### Test 4: List Uploaded Data Sources

```bash
curl http://localhost:3011/api/v1/ingestion/data-sources
```

### Test 5: Run Analysis on Uploaded File

First, get the `data_source_id` from the upload response, then:

```bash
curl -X POST "http://localhost:3011/api/v1/analysis/run" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{\"data_source_id\": 1}"
```

Replace `1` with your actual `data_source_id`.

### Test 6: Check Analysis Results

```bash
curl http://localhost:3011/api/v1/analysis/runs
```

### Test 7: View Analysis Run Details

```bash
curl http://localhost:3011/api/v1/analysis/runs/1
```

Replace `1` with your actual analysis run ID.

## Testing with Python Script

Create a test script `test_upload.py`:

```python
import requests

# Upload file
with open('path/to/your/file.xlsx', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:3011/api/v1/ingestion/upload',
        files=files
    )
    print("Upload Response:", response.json())
    data_source_id = response.json()['data_source_id']

# Run analysis
analysis_response = requests.post(
    'http://localhost:3011/api/v1/analysis/run',
    json={'data_source_id': data_source_id}
)
print("Analysis Response:", analysis_response.json())
```

Run it:
```bash
python test_upload.py
```

## Expected Results

### For 4C Alert (Long Time Logged On Users):
- **Focus Area**: ACCESS_GOVERNANCE
- **Issue Type**: LONG_SESSION
- **Risk Level**: Medium to High
- **Findings**: One finding per user session

### For SoDA Report (AVR - Access Violation Review):
- **Focus Area**: ACCESS_GOVERNANCE
- **Issue Type**: SOD_VIOLATION or UNAUTHORIZED_ACCESS
- **Risk Level**: High to Critical
- **Findings**: Based on violations in the report

## Troubleshooting

### Database Connection Error
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in `.env` file
- Ensure database exists: `psql -l | grep treasure_hunt_analyzer`

### File Upload Fails
- Check file format is supported (PDF, CSV, DOCX, XLSX)
- Verify file path is correct
- Check storage directory exists and is writable

### Analysis Fails
- Check database has focus areas and issue types initialized
- Verify data source was parsed successfully
- Check logs for error messages

### Frontend Not Loading
- Verify backend is running on port 3011
- Check browser console for errors
- Verify CORS is configured correctly

## Next Steps

After basic testing works:
1. Test with multiple file types
2. Test analysis with different alert/report types
3. Verify findings are created correctly
4. Check risk assessments are calculated
5. Test money loss calculation (requires LLM API key)

## Notes

- Money loss calculation requires LLM API key (OpenAI or Anthropic)
- Without LLM key, system will use fallback calculations
- ML model needs training data before it can make accurate predictions
- Initial database seed creates 6 focus areas and common issue types

