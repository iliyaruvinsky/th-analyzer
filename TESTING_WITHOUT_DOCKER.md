# Testing Without Docker

If you don't have Docker installed, you can test the system manually.

## Prerequisites

1. **Python 3.11+** installed
2. **Node.js 18+** installed  
3. **PostgreSQL 15+** installed and running

## Step 1: Install PostgreSQL

If you don't have PostgreSQL:

1. Download from: https://www.postgresql.org/download/windows/
2. Install with default settings
3. Remember the password you set for `postgres` user
4. PostgreSQL will run on `localhost:5432`

## Step 2: Set Up Backend

```cmd
cd backend

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Create .env file
copy .env.example .env
```

Edit `.env` file:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/treasure_hunt_analyzer
SECRET_KEY=test-secret-key-change-in-production
DEBUG=True
STORAGE_TYPE=local
STORAGE_PATH=./storage
```

Create the database:
```sql
-- Connect to PostgreSQL (use pgAdmin or psql)
CREATE DATABASE treasure_hunt_analyzer;
```

Initialize database:
```cmd
python -m app.utils.init_db
```

Start backend:
```cmd
uvicorn app.main:app --reload
```

Backend will run on http://localhost:3011

## Step 3: Set Up Frontend

Open a NEW terminal window:

```cmd
cd frontend

REM Install dependencies
npm install

REM Start frontend
npm run dev
```

Frontend will run on http://localhost:3010

## Step 4: Test the System

1. **Test Backend:**
   - Open http://localhost:3011/docs
   - Test file upload endpoint
   - Test analysis endpoint

2. **Test Frontend:**
   - Open http://localhost:3010
   - Upload a file
   - View dashboard

## Troubleshooting

**PostgreSQL connection error:**
- Make sure PostgreSQL service is running
- Check password in `.env` file
- Verify database exists

**Port already in use:**
- Backend (3011): Change port in uvicorn command
- Frontend (3010): Vite will suggest alternative port
- PostgreSQL (5432): Check if already running

**Python module not found:**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**npm install fails:**
- Make sure Node.js is installed
- Try `npm install --legacy-peer-deps`

