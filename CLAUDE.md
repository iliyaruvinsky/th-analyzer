# CLAUDE.md - AI Assistant Guide for Treasure Hunt Analyzer (THA)

This document provides AI assistants with essential context for working effectively with this codebase.

> **Important:** Also read [`llm_handover.md`](llm_handover.md) for detailed operational context, recent milestones, known issues, and project state. That document is updated after each verified milestone.

## Project Overview

**Treasure Hunt Analyzer (THA)** is an enterprise system for analyzing Skywind platform alerts and reports. It provides insights across 6 focus areas with advanced visualization, risk assessment, and financial impact analysis.

**Owner:** Skywind Software Group
**License:** Proprietary

### Key Capabilities
- Multi-format file ingestion (PDF, CSV, DOCX, Excel)
- Classification into 6 Focus Areas
- Hybrid money loss calculation (LLM + ML engine)
- Interactive dashboards with drill-down
- Risk assessment with financial impact analysis

## Quick Reference

### Start Development Environment
```bash
docker-compose up -d
docker-compose exec backend python -m app.utils.init_db
```

### Access Points
| Service | URL |
|---------|-----|
| Frontend | http://localhost:3010 |
| Backend API | http://localhost:3011 |
| Swagger Docs | http://localhost:3011/docs |
| ReDoc | http://localhost:3011/redoc |
| Health Check | http://localhost:3011/health |

### Stop Services
```bash
docker-compose down
```

## Technology Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI 0.104.1
- **Server:** Uvicorn
- **Database:** PostgreSQL 15 with SQLAlchemy 2.0
- **Migrations:** Alembic
- **AI/ML:** OpenAI, Anthropic, scikit-learn
- **File Parsing:** pdfplumber, python-docx, pandas, openpyxl

### Frontend
- **Language:** TypeScript 5.3
- **Framework:** React 18.2
- **Build Tool:** Vite 5.0
- **State Management:** Zustand
- **Data Fetching:** TanStack React Query
- **Charts:** Recharts, Chart.js, D3
- **Tables:** TanStack React Table

## Project Structure

```
th-analyzer/
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── api/                  # Route handlers
│   │   │   ├── ingestion.py      # File upload endpoints
│   │   │   ├── analysis.py       # Analysis execution
│   │   │   ├── dashboard.py      # Dashboard data
│   │   │   └── maintenance.py    # DB maintenance
│   │   ├── core/
│   │   │   ├── config.py         # Settings (Pydantic)
│   │   │   └── database.py       # SQLAlchemy setup
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   │   ├── analysis/         # Analyzer, classifier, risk scorer
│   │   │   ├── ingestion/        # File parsers
│   │   │   ├── llm_engine/       # LLM integration
│   │   │   ├── ml_engine/        # ML predictions
│   │   │   └── hybrid_engine.py  # Combined LLM+ML
│   │   ├── utils/
│   │   │   └── init_db.py        # Database seeding
│   │   └── main.py               # FastAPI app entry
│   ├── alembic/                  # Database migrations
│   └── requirements.txt
│
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── pages/                # Page components
│   │   │   ├── Dashboard.tsx     # Main dashboard
│   │   │   ├── Upload.tsx        # File upload
│   │   │   ├── Findings.tsx      # Findings list
│   │   │   ├── FindingDetail.tsx # Finding details
│   │   │   ├── Reports.tsx       # Report generation
│   │   │   ├── Maintenance.tsx   # DB maintenance
│   │   │   └── Logs.tsx          # Audit logs
│   │   ├── components/           # Reusable components
│   │   │   ├── charts/           # Visualization components
│   │   │   ├── tables/           # Table components
│   │   │   └── filters/          # Filter components
│   │   ├── services/
│   │   │   └── api.ts            # Axios API client
│   │   ├── App.tsx               # Router setup
│   │   └── main.tsx              # Entry point
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                         # Documentation & samples
│   ├── case-studies/             # Real-world examples
│   ├── product-docs/             # Skywind platform docs
│   ├── th-context/               # THA-specific context
│   ├── soda-templates/           # SoDA report examples
│   └── skywind-4c-alerts-output/ # 4C alert examples
│
├── aws/                          # AWS deployment
│   ├── cloudformation-template.yaml
│   ├── ecs-task-definition.json
│   └── lambda-function.py
│
├── plugins/                      # AI assistant plugins
│   └── anti-hallucination/       # Verification rules
│
├── .claude/                      # Claude Code config
│   ├── settings.local.json       # Permissions
│   └── skills/                   # Custom skills
│
├── docker-compose.yml            # Development setup
├── docker-compose.prod.yml       # Production setup
└── docker-compose.optimized.yml  # Optimized variant
```

## Domain Model

### 6 Focus Areas
1. **BUSINESS_PROTECTION** - Fraud detection, cybersecurity
2. **BUSINESS_CONTROL** - Business bottlenecks, anomalies
3. **ACCESS_GOVERNANCE** - SoD violations, authorization control
4. **TECHNICAL_CONTROL** - Infrastructure, technical anomalies
5. **JOBS_CONTROL** - Job performance, resource utilization
6. **S/4HANA_EXCELLENCE** - Post-migration safeguarding

### Data Flow
```
User Upload → Parser → Data Extraction → Analysis Run
    ↓
Classifier (Focus Area + Issue Type)
    ↓
Risk Scorer (0-100 scale)
    ↓
Hybrid Money Loss Engine (60% LLM + 40% ML)
    ↓
Findings with Risk & Financial Data → Dashboard
```

### Key Database Models
| Model | Purpose |
|-------|---------|
| `DataSource` | Uploaded file metadata |
| `Alert` | Parsed 4C alert data |
| `SoDAReport` | Parsed SoDA report data |
| `Finding` | Detected issues/risks |
| `FocusArea` | 6 classification categories |
| `IssueType` | Issue classifications (~18 types) |
| `RiskAssessment` | Risk scores (0-100) |
| `MoneyLossCalculation` | Financial impact estimates |
| `AnalysisRun` | Execution tracking |
| `AuditLog` | Audit trail |

### Database Relationships
```
findings → focus_areas (many-to-one)
findings → issue_types (many-to-one)
findings → risk_assessments (one-to-one)
findings → money_loss_calculations (one-to-one)
analysis_runs → data_sources (many-to-one)
```

## API Endpoints

### Ingestion
```
POST /api/v1/ingestion/upload        # Upload file
GET  /api/v1/ingestion/data-sources  # List uploaded files
```

### Analysis
```
POST /api/v1/analysis/run            # Execute analysis
GET  /api/v1/analysis/runs           # List analysis runs
GET  /api/v1/analysis/runs/{id}      # Get run details
GET  /api/v1/analysis/findings       # Query findings
```

### Dashboard
```
GET  /api/v1/dashboard/kpis          # Summary statistics
```

### Maintenance
```
GET    /api/v1/maintenance/data-sources      # List sources
DELETE /api/v1/maintenance/data-sources/{id} # Delete source
DELETE /api/v1/maintenance/data-sources      # Clear all
GET    /api/v1/maintenance/logs              # Audit logs
```

## Development Workflows

### Running Tests
```bash
# Backend tests
cd backend && pytest

# API health check
curl http://localhost:3011/health
```

### Database Operations
```bash
# Initialize/seed database
docker-compose exec backend python -m app.utils.init_db

# View logs
docker-compose logs -f backend

# Database shell
docker-compose exec postgres psql -U tha_user -d tha_db
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev      # Development server
npm run build    # Production build
npm run lint     # ESLint
```

### Adding New Features

**New API Endpoint:**
1. Add route in `backend/app/api/`
2. Add Pydantic schemas in `backend/app/schemas/`
3. Add business logic in `backend/app/services/`
4. Register router in `backend/app/main.py`

**New Database Model:**
1. Create model in `backend/app/models/`
2. Create Alembic migration: `alembic revision --autogenerate -m "description"`
3. Apply migration: `alembic upgrade head`

**New Frontend Page:**
1. Create component in `frontend/src/pages/`
2. Add route in `frontend/src/App.tsx`
3. Update navigation in `frontend/src/components/Layout.tsx`

## Code Conventions

### Python (Backend)
- Use type hints for all function parameters and returns
- Follow PEP 8 style guide
- Use Pydantic models for request/response validation
- SQLAlchemy 2.0 style queries
- Async operations where beneficial

### TypeScript (Frontend)
- Strict TypeScript mode enabled
- Use functional components with hooks
- TanStack Query for data fetching
- Zustand for global state
- Prefer named exports

### General
- Environment variables for configuration
- No hardcoded secrets
- Meaningful commit messages
- Feature branches for development

## Key Files Reference

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app setup, CORS, middleware |
| `backend/app/core/config.py` | All configuration settings |
| `backend/app/core/database.py` | Database connection |
| `backend/app/utils/init_db.py` | Database seeding |
| `backend/app/services/analysis/analyzer.py` | Main analysis orchestration |
| `backend/app/services/hybrid_engine.py` | LLM+ML money loss calculation |
| `frontend/src/services/api.ts` | All API client functions |
| `frontend/src/pages/Dashboard.tsx` | Main dashboard logic |
| `docker-compose.yml` | Container orchestration |
| `llm_handover.md` | **AI handover doc - read first!** |

### Critical Files - Do Not Break
These files are essential for system operation. Exercise extra caution when modifying:
- `backend/app/core/database.py` - Database connection
- `backend/app/main.py` - FastAPI app initialization
- `frontend/src/services/api.ts` - API client
- `docker-compose.yml` - Service orchestration
- `backend/app/utils/init_db.py` - Database initialization

## Configuration

### Backend Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=your-secret-key
DEBUG=true
ENVIRONMENT=development
LLM_PROVIDER=openai  # or anthropic
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
STORAGE_TYPE=local  # or s3
STORAGE_PATH=/app/storage
```

### Docker Ports
| Service | Internal | External (Dev) |
|---------|----------|----------------|
| Backend | 8000 | 3011 |
| Frontend | 80 | 3010 |
| PostgreSQL | 5432 | 5433 |

## Common Tasks

### Upload and Analyze a File
```bash
# 1. Upload file
curl -X POST "http://localhost:3011/api/v1/ingestion/upload" \
  -F "file=@path/to/file.xlsx"

# 2. Get data_source_id from response, then run analysis
curl -X POST "http://localhost:3011/api/v1/analysis/run" \
  -H "Content-Type: application/json" \
  -d '{"data_source_id": "uuid-from-step-1"}'

# 3. View findings
curl "http://localhost:3011/api/v1/analysis/findings"
```

### Clear Database
```bash
curl -X DELETE "http://localhost:3011/api/v1/maintenance/data-sources?confirm=true"
```

### Check System Health
```bash
curl http://localhost:3011/health
```

## Troubleshooting

### Container Issues
```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Full reset with volume cleanup
docker-compose down -v
docker-compose up -d --build
docker-compose exec backend python -m app.utils.init_db
```

### Database Connection Issues
- Verify PostgreSQL container is running: `docker-compose ps`
- Check DATABASE_URL format in backend/.env
- Ensure port 5433 is available
- Try database shell: `docker-compose exec postgres psql -U tha_user -d treasure_hunt_analyzer`

### Backend 500 Errors
- Check database schema matches models
- View logs: `docker-compose logs backend`
- Common fix - schema mismatch:
```bash
# Add missing columns manually if needed
docker-compose exec backend python -c "from app.core.database import engine; from sqlalchemy import text; engine.connect().execute(text('ALTER TABLE analysis_runs ADD COLUMN IF NOT EXISTS data_source_id INTEGER REFERENCES data_sources(id)'))"
```

### Frontend Can't Connect to Backend
1. Verify backend is running: http://localhost:3011/health
2. Check CORS configuration in `backend/app/main.py`
3. Ensure `VITE_API_BASE_URL` is set to `http://localhost:3011/api/v1`

### File Upload Issues
- Check supported formats: PDF, CSV, DOCX, XLSX
- Verify file is not corrupted
- Check backend logs for parsing errors

## AWS Deployment

Refer to `aws/README.md` for production deployment:
- CloudFormation for infrastructure
- ECS Fargate for containers
- RDS for PostgreSQL
- S3 for file storage
- Secrets Manager for credentials

## Important Notes

1. **Volume Mounts:** Disabled in docker-compose.yml due to Windows/Google Drive path issues
2. **Hot Reload:** Disabled in Docker dev setup; restart containers for changes
3. **CORS:** Configured for localhost; update for production domains
4. **Authentication:** JWT infrastructure ready but not enforced
5. **Sample Data:** Located in `docs/` subdirectories for testing

## Data Flow Details

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

## AI Agent Guidelines

### Before Starting Work
1. **Read `llm_handover.md` completely** - Contains current project state
2. **Check git status** - Understand uncommitted changes
3. **Verify Docker environment** - `docker compose ps`
4. **Test current functionality** - Ensure nothing is broken
5. **Review recent changes** in git log

### When Making Changes
1. **Update `llm_handover.md`** after verified milestones
2. **Test thoroughly** before marking as complete
3. **Document breaking changes** clearly
4. **Commit frequently** with descriptive messages
5. **Update relevant .md files** (README, documentation)

### Handover Document Maintenance
The `llm_handover.md` must be updated when:
- A feature is completed and tested
- A bug is fixed and verified
- Database schema changes
- API endpoint changes
- Configuration changes
- Known issues discovered or resolved

**Rule:** Do not mark a task complete without updating `llm_handover.md`.

See `.claude/rules/llm-handover-maintenance.md` for detailed update guidelines.

### Testing Checklist
Before considering work complete, verify:
- [ ] Docker containers start successfully
- [ ] Database initialization works
- [ ] Frontend loads correctly
- [ ] Backend API accessible
- [ ] Dashboard displays data
- [ ] API endpoints return expected responses
- [ ] No console errors in browser

## Related Documentation

- [README.md](README.md) - Project overview
- [QUICK_START.md](QUICK_START.md) - 5-minute setup
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing details
- [CONTRIBUTING.md](CONTRIBUTING.md) - Plugin contributions
- [aws/README.md](aws/README.md) - AWS deployment
- [llm_handover.md](llm_handover.md) - **AI handover document (read first!)**
- [.claude/rules/llm-handover-maintenance.md](.claude/rules/llm-handover-maintenance.md) - Handover update rules
