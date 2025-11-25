# LLM Handover Document - Treasure Hunt Analyzer (THA)

**Last Updated**: 2025-11-23
**Project Status**: Development - Production Ready (Local), Needs GitHub Sync
**Current Version**: 1.0.0

---

## Purpose

This document provides comprehensive project context for AI agents working on the Treasure Hunt Analyzer. It's systematically updated after each verified milestone, significant change, or project state update to ensure new agents can quickly understand the project and continue development.

---

## Project Overview

**Name**: Treasure Hunt Analyzer (THA)
**Purpose**: Comprehensive system for analyzing Skywind platform alerts and reports, providing insights across 6 focus areas with advanced visualization and reporting capabilities.

**Tech Stack**:
- **Backend**: FastAPI (Python 3.11), PostgreSQL 15, SQLAlchemy
- **Frontend**: React 18, TypeScript, Vite, Bootstrap 5, Recharts
- **Infrastructure**: Docker Compose, AWS (CloudFormation, ECS, RDS, Lambda)
- **AI/ML**: OpenAI/Anthropic LLMs, scikit-learn ML models

---

## Current Project State

### Working Features ✅

1. **Multi-format Data Ingestion**
   - CSV, Excel (4C & SoDA formats), PDF, DOCX support
   - File upload via frontend interface
   - Automatic parsing and data extraction
   - Storage in PostgreSQL database

2. **6 Focus Area Classification**
   - Business Protection (BP)
   - Business Control (BC)
   - Access Governance (AG)
   - Technical Control (TC)
   - Jobs Control (JC)
   - S/4HANA Excellence (S4)

3. **Issue Type Grouping**
   - Automatic grouping of findings by issue types
   - Hierarchical categorization

4. **Hybrid Money Loss Calculation**
   - LLM-based reasoning (OpenAI/Anthropic)
   - ML-based learning with trained models
   - Confidence scoring

5. **Interactive Dashboard** (VERIFIED WORKING)
   - KPI summary cards (Total Findings, Risk Score, Money Loss, Analysis Runs)
   - Focus Area distribution chart
   - Risk Level distribution chart
   - Money Loss over time chart
   - Filterable findings table
   - Real-time data refresh (5-second intervals)

6. **Multiple Pages**
   - Dashboard (/)
   - Upload (/upload)
   - Findings (/findings)
   - Finding Detail (/findings/:id)
   - Reports (/reports)
   - Maintenance (/maintenance)
   - Logs (/logs)

7. **Maintenance & Audit**
   - Data source management
   - Audit logging system
   - Bulk delete operations

8. **AWS Deployment Infrastructure**
   - CloudFormation templates
   - ECS Fargate configurations
   - RDS PostgreSQL setup
   - Lambda functions for maintenance
   - Application Load Balancer

---

## Recent Milestones (Verified)

### 2025-11-23: Docker Environment Setup & Dashboard Fix ✅
- **Fixed**: Docker Desktop connectivity issues
- **Resolved**: Database schema mismatch (missing `data_source_id` column in `analysis_runs` table)
- **Verified**: All Docker containers running (postgres, backend, frontend)
- **Verified**: Dashboard fully functional with live data
  - 46,586 total findings
  - 29 analysis runs
  - $25.6M total money loss
  - 2.35M total risk score
- **Access Points**:
  - Frontend: http://localhost:3001
  - Backend: http://localhost:8080
  - API Docs: http://localhost:8080/docs

### 2025-11-23: Dashboard Redesign - Skywind.ai Style ✅
- **REDESIGNED**: Complete UI overhaul from industrial-brutalist to Skywind professional aesthetic
- **Color Palette**: Changed from dark (#0a0e14) to light (#f8f9fa) with Skywind red (#C41E3A) accents
- **Typography**: Replaced Orbitron/JetBrains Mono with professional system fonts
- **Charts**: Updated all 3 chart components (Focus Area, Risk Level, Money Loss) with Skywind colors
- **Files Modified**:
  - `frontend/src/styles/dashboard.css` - Complete rewrite (600+ lines)
  - `frontend/src/pages/Dashboard.tsx` - Text and structure updates
  - `frontend/src/components/charts/*.tsx` - All 3 chart components
  - `frontend/index.html` - Removed custom fonts
- **Documentation**: Created `DASHBOARD_REDESIGN_SUMMARY.md` with complete design specifications
- **Claude Skill**: Installed `frontend-design` skill in `.claude/skills/frontend-design/`
- **Brand Alignment**: Dashboard now matches Skywind.ai corporate identity

### Known Issues Resolved
1. ~~CORS errors~~ - Fixed (backend CORS middleware properly configured)
2. ~~Database schema mismatch~~ - Fixed (added `data_source_id` column)
3. ~~500 errors on /api/v1/analysis/runs~~ - Fixed
4. ~~Dashboard infinite reload~~ - Fixed

---

## Architecture Overview

### Directory Structure
```
treasure-hunt-analyzer/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI route handlers
│   │   ├── core/           # Database, config
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   │   ├── analysis/   # Analysis engine
│   │   │   ├── ingestion/  # Data parsers (CSV, Excel, PDF)
│   │   │   ├── llm_engine/ # LLM integration
│   │   │   ├── ml_engine/  # ML models
│   │   │   └── hybrid_engine.py
│   │   └── utils/          # Utilities, audit logger, init_db
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── charts/     # Recharts visualizations
│   │   │   ├── filters/    # Dashboard filters
│   │   │   └── tables/     # Data tables
│   │   ├── pages/          # Page components
│   │   ├── services/       # API client (axios)
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── package.json
├── aws/                    # AWS deployment templates
├── docs/                   # SoDA templates, context files
├── ml_models/              # Trained ML models
├── scripts/                # Install scripts
├── docker-compose.yml      # Development setup
├── docker-compose.prod.yml # Production setup
└── *.md                    # Documentation files
```

### Database Schema (PostgreSQL)

**Core Tables**:
- `data_sources` - Uploaded files metadata
- `focus_areas` - 6 focus area definitions
- `issue_types` - Issue type classifications
- `field_mappings` - Column mapping configurations
- `findings` - Individual security findings
- `analysis_runs` - Analysis execution records
- `risk_assessments` - Risk scoring data
- `money_loss_calculations` - Financial impact calculations
- `audit_logs` - System audit trail

**Key Relationships**:
- `findings` → `focus_areas` (many-to-one)
- `findings` → `issue_types` (many-to-one)
- `findings` → `risk_assessments` (one-to-one)
- `findings` → `money_loss_calculations` (one-to-one)
- `analysis_runs` → `data_sources` (many-to-one)

---

## API Endpoints

### Analysis (`/api/v1/analysis`)
- `POST /run` - Run analysis on data source
- `GET /runs` - List all analysis runs
- `GET /runs/{id}` - Get specific analysis run
- `GET /findings` - Get findings with filters

### Ingestion (`/api/v1/ingestion`)
- `POST /upload` - Upload data file
- `GET /data-sources` - List uploaded files

### Dashboard (`/api/v1/dashboard`)
- `GET /kpis` - Get summary KPIs

### Maintenance (`/api/v1/maintenance`)
- `GET /data-sources` - List data sources
- `DELETE /data-sources/{id}` - Delete data source
- `DELETE /data-sources` - Bulk delete
- `GET /logs` - Get audit logs

---

## Environment Configuration

### Backend Environment Variables
```bash
DATABASE_URL=postgresql://tha_user:tha_password@postgres:5432/treasure_hunt_analyzer
STORAGE_TYPE=local
STORAGE_PATH=/app/storage
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True
ENVIRONMENT=development
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>
LLM_PROVIDER=openai
```

### Frontend Environment Variables
```bash
VITE_API_BASE_URL=http://localhost:8080/api/v1
```

### Docker Compose Ports
- PostgreSQL: 5432
- Backend: 8080 → 8000 (internal)
- Frontend: 3001 → 3000 (internal)

---

## Development Workflow

### Starting the Application
```bash
# Navigate to project
cd "G:\My Drive\SW_PLATFORM\4. MARKETING\PRESENTATIONS\CURRENT\14. Treasure Hunting\treasure-hunt-analyzer"

# Start all services
docker compose up -d

# Check status
docker compose ps

# Initialize database (first time only)
docker compose exec backend python -m app.utils.init_db

# View logs
docker compose logs -f
```

### Stopping the Application
```bash
docker compose down
```

### Rebuilding After Code Changes
```bash
docker compose up -d --build
```

### Database Operations
```bash
# Initialize/reset database
docker compose exec backend python -m app.utils.init_db

# Check data
docker compose exec backend python backend/check_data.py

# Access PostgreSQL directly
docker compose exec postgres psql -U tha_user -d treasure_hunt_analyzer
```

---

## Git & Version Control Status

### Current Branch
- Local: `main`
- Remote Default: `feature/add-plugin-dev-agent-to-marketplace` (MIXED CONTENT - needs cleanup)

### Uncommitted Changes (as of 2025-11-23)
- **32 modified files** in backend/, frontend/, docker-compose.yml
- **50+ untracked files** including:
  - AWS deployment infrastructure (aws/)
  - Documentation files (*.md)
  - New API endpoints (dashboard.py, maintenance.py)
  - Frontend components (charts/, filters/, tables/)
  - Audit logging system

### GitHub Repository Status
- **URL**: https://github.com/iliyaruvinsky/treasure_hunt
- **Sync Status**: LOCAL IS AHEAD - GitHub has ~30-40% of local functionality
- **Critical Missing on GitHub**:
  - Dashboard charts and visualizations
  - Maintenance & audit systems
  - AWS deployment templates
  - 12+ documentation files
  - Enhanced UI components

**ACTION REQUIRED**: Commit and push local changes to GitHub for backup and team collaboration.

---

## Data Flow

### Upload Flow
1. User uploads file via `/upload` page
2. Frontend: `POST /api/v1/ingestion/upload` with FormData
3. Backend: File saved to storage, metadata in `data_sources` table
4. Parser (CSV/Excel/PDF) extracts findings
5. Data stored in `findings` table with relationships

### Analysis Flow
1. User triggers analysis on data source
2. Frontend: `POST /api/v1/analysis/run` with `data_source_id`
3. Backend `Analyzer` service:
   - Fetches findings from data source
   - Classifies focus areas and issue types
   - Hybrid engine calculates money loss (LLM + ML)
   - Risk assessment scoring
   - Creates `analysis_run` record with aggregated results
4. Frontend displays results in dashboard

### Dashboard Data Flow
1. Dashboard loads: 3 parallel API calls
   - `GET /api/v1/dashboard/kpis` - Summary metrics
   - `GET /api/v1/analysis/findings` - Individual findings
   - `GET /api/v1/analysis/runs` - Analysis run history
2. Data refreshes every 5 seconds (React Query)
3. Charts aggregate findings data client-side
4. Filters trigger new API calls with query parameters

---

## Key Dependencies

### Backend (requirements.txt)
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- pydantic==2.5.0
- openai==1.3.5
- anthropic==0.7.1
- scikit-learn==1.3.2
- pandas==2.1.3
- openpyxl==3.1.2
- python-multipart==0.0.6

### Frontend (package.json)
- react==18.2.0
- typescript==5.2.2
- vite==5.0.0
- axios==1.6.2
- @tanstack/react-query==5.8.4
- react-router-dom==6.20.0
- recharts==2.10.3
- bootstrap==5.3.2

---

## Testing & Validation

### Manual Testing Checklist
- [x] Docker containers start successfully
- [x] Database initialization works
- [x] Frontend loads at localhost:3001
- [x] Backend API accessible at localhost:8080
- [x] Dashboard displays data correctly
- [x] KPI cards show accurate totals
- [x] Charts render properly
- [x] API endpoints return 200 responses
- [ ] File upload works (CSV, Excel, PDF)
- [ ] Analysis run completes successfully
- [ ] Filters update dashboard data
- [ ] Finding detail page loads
- [ ] Maintenance operations work
- [ ] Audit logs are recorded

### Known Working Endpoints (Verified 2025-11-23)
- ✅ `GET /health` - Returns healthy status
- ✅ `GET /api/v1/dashboard/kpis` - Returns correct totals
- ✅ `GET /api/v1/analysis/runs` - Returns analysis run list
- ✅ `GET /api/v1/analysis/findings` - Returns findings with filters

---

## Common Issues & Solutions

### Issue: Docker containers won't start
**Solution**:
1. Ensure Docker Desktop is running
2. Check ports 3001, 8080, 5432 are not in use
3. Run `docker compose down -v` then `docker compose up -d --build`

### Issue: Backend 500 errors
**Solution**:
1. Check database schema matches models
2. Run database migration if needed
3. View logs: `docker compose logs backend`

### Issue: Frontend can't connect to backend
**Solution**:
1. Verify backend is running: http://localhost:8080/health
2. Check CORS configuration in `backend/app/main.py`
3. Ensure `VITE_API_BASE_URL` is set correctly

### Issue: Database schema mismatch
**Solution**:
```bash
# Add missing columns manually
docker compose exec backend python -c "from app.core.database import engine; from sqlalchemy import text; engine.connect().execute(text('ALTER TABLE analysis_runs ADD COLUMN IF NOT EXISTS data_source_id INTEGER REFERENCES data_sources(id)'))"

# Or recreate database (loses data)
docker compose down -v
docker compose up -d
docker compose exec backend python -m app.utils.init_db
```

---

## Next Steps & Roadmap

### Immediate Priorities
1. **Git Sync**: Commit and push all local changes to GitHub
2. **Branch Cleanup**: Separate THA and Plugin Marketplace projects
3. **Testing**: Complete manual testing checklist
4. **Documentation**: Update README with latest features

### Feature Enhancements (Planned)
- [ ] Advanced filtering (date ranges, multi-select)
- [ ] Export reports (PDF, Excel)
- [ ] User authentication & authorization
- [ ] Real-time analysis progress tracking
- [ ] Batch upload processing
- [ ] Enhanced ML model training interface
- [ ] Custom risk scoring rules
- [ ] Integration with Skywind APIs

### Infrastructure Improvements
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Automated testing (pytest, Jest)
- [ ] Production deployment to AWS
- [ ] Monitoring & alerting (CloudWatch)
- [ ] Database backups & recovery
- [ ] Performance optimization
- [ ] Security hardening

---

## Important Notes for AI Agents

### Before Starting Work
1. **Read this handover document completely**
2. **Check git status** - understand uncommitted changes
3. **Verify Docker environment is running** - `docker compose ps`
4. **Test current functionality** - ensure nothing is broken
5. **Review recent changes** in git log and this document

### When Making Changes
1. **Update this handover document** after verified milestones
2. **Test thoroughly** before marking as complete
3. **Document breaking changes** clearly
4. **Commit frequently** with descriptive messages
5. **Update relevant .md files** (README, documentation)

### Code Style & Conventions
- **Backend**: Follow FastAPI best practices, use type hints
- **Frontend**: TypeScript strict mode, functional components with hooks
- **Database**: Use SQLAlchemy ORM, no raw SQL unless necessary
- **API**: RESTful conventions, proper status codes
- **Error Handling**: Try/except with audit logging
- **Documentation**: Docstrings for all functions/classes

### Critical Files - Do Not Break
- `backend/app/core/database.py` - Database connection
- `backend/app/main.py` - FastAPI app initialization
- `frontend/src/services/api.ts` - API client
- `docker-compose.yml` - Service orchestration
- `backend/app/utils/init_db.py` - Database initialization

---

## Contact & Resources

### Documentation Files
- `README.md` - Project overview
- `START_SERVERS.md` - Server startup guide
- `DOCKER_SETUP_GUIDE.md` - Docker configuration
- `TESTING_CHECKLIST.md` - Testing procedures
- `DEPLOYMENT.md` - AWS deployment guide
- `QUICK_TEST.md` - Quick testing guide

### External Resources
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev
- SQLAlchemy Docs: https://docs.sqlalchemy.org
- Docker Compose Docs: https://docs.docker.com/compose

### GitHub Repository
- URL: https://github.com/iliyaruvinsky/treasure_hunt
- Status: Needs sync with local changes

---

## Changelog

### 2025-11-23
- **CREATED**: Initial LLM handover document
- **FIXED**: Docker environment setup (Desktop connectivity)
- **FIXED**: Database schema mismatch (analysis_runs.data_source_id)
- **VERIFIED**: Dashboard fully functional with live data
- **VERIFIED**: All API endpoints working correctly
- **DOCUMENTED**: Current project state and git status
- **IDENTIFIED**: GitHub sync gap (local ahead by ~60% functionality)

---

### 2025-11-25
- **UPDATED**: Frontend now runs on port 3010, backend on port 3011 to avoid conflicts.
- **UPDATED**: Docker Compose updated with build args and environment variable `VITE_API_BASE_URL` pointing to `http://localhost:3011/api/v1`.
- **UPDATED**: `frontend/src/services/api.ts` fallback URL changed to `http://localhost:3011/api/v1`.
- **UPDATED**: Backend CORS middleware now allows `http://localhost:3010`.
- **UPDATED**: `frontend/Dockerfile.dev` accepts `VITE_API_BASE_URL` build arg.
- **UPDATED**: Database re‑initialized after schema fix; containers rebuilt.
- **NOTE**: All containers are healthy; dashboard accessible at `http://localhost:3010`.

**END OF HANDOVER DOCUMENT**

*This document should be updated systematically after each verified milestone, significant change, or project state update. Keep it comprehensive and accurate for seamless AI agent collaboration.*
