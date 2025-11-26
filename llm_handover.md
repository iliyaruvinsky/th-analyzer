# LLM Handover Document - Treasure Hunt Analyzer (THA)

**Last Updated**: 2025-11-26 (Session End)
**Project Status**: Development - Content Analyzer WORKING, Scoring Rules IN PROGRESS
**Current Version**: 1.2.0

---

## Purpose

This document provides comprehensive project context for AI agents working on the Treasure Hunt Analyzer. It's systematically updated after each verified milestone, significant change, or project state update to ensure new agents can quickly understand the project and continue development.

---

## CRITICAL: Current Work in Progress

### Active Development Focus: Content Analyzer Scoring Rules

The user is working on defining **Focus Area-specific scoring rules** for the Content Analyzer. Each of the 5 Focus Areas will have its own scoring principles.

**Currently discussing:** BUSINESS_PROTECTION focus area scoring

**Key Context the User Provided:**

1. **Severity Base Scores (UPDATED - not yet implemented)**:
   - Critical: 90 (was 85)
   - High: 75 (was 65)
   - Medium: 60 (was 45)
   - Low: 50 (was 25)

2. **Count Adjustment must consider BACKDAYS parameter**:
   - Alert parameters are in `Metadata_*` file
   - BACKDAYS = history depth (e.g., BACKDAYS=1 means yesterday+today)
   - Raw count alone is MISLEADING - must normalize by BACKDAYS
   - Example: 1,943 vendors in 1 day vs 1,943 vendors in 30 days = VERY different risk

3. **Money Adjustment thresholds** - User wants explanation/refinement:
   - $1M+: +20 points
   - $100K+: +15 points
   - $10K+: +10 points

4. **Missing Documentation**: User mentioned `docs/about_skywind/TXT` folder with Skywind alert parameter documentation - THIS FOLDER DOES NOT EXIST IN THE REPO. Ask user to provide.

---

## Project Overview

**Name**: Treasure Hunt Analyzer (THA)
**Purpose**: Enterprise system for analyzing Skywind platform alerts (4C) and reports (SoDA), providing insights across 5 focus areas with risk assessment and financial impact analysis.

**Tech Stack**:
- **Backend**: FastAPI (Python 3.11), PostgreSQL 15, SQLAlchemy 2.0
- **Frontend**: React 18, TypeScript, Vite, Bootstrap 5, Recharts
- **Infrastructure**: Docker Compose (dev), AWS (prod)
- **AI/ML**: OpenAI/Anthropic LLMs (optional), Pattern-based fallback

---

## Current Project State (VERIFIED 2025-11-26)

### Working Features ✅

1. **Multi-File Artifact Upload (UI)**
   - Upload page at http://localhost:3010/upload
   - Add files one-by-one (Code, Explanation, Metadata, Summary)
   - Color-coded file categorization (green=found, yellow=pending)
   - Flexible file name matching (handles spaces after prefix)
   - Auto-analyze after upload

2. **Content Analyzer (Pattern-Based)**
   - Reads 4 artifact files from uploaded directory
   - Extracts text from .txt, .docx, .xlsx files
   - Classifies into 5 Focus Areas (keyword matching)
   - Extracts counts (handles comma-separated: "1,943")
   - Extracts monetary amounts (handles $45M format)
   - Calculates risk score with breakdown

3. **End-to-End Flow WORKING**
   - Upload 4 artifacts via UI → Analyze → Dashboard shows results
   - Example tested: "Rarely Used Vendors" alert
   - Result: BUSINESS_CONTROL, 1,943 vendors, $45,000,000 exposure, Risk Score 80

4. **Dashboard (VERIFIED)**
   - KPI cards: Total Findings, Risk Score, Financial Exposure, Analysis Runs
   - Focus Area distribution chart
   - Risk Level analysis chart
   - Filters (Focus Area, Severity, Status, Date Range)

5. **API Endpoints (VERIFIED)**
   - `POST /api/v1/ingestion/upload-artifacts` - Multi-file upload
   - `POST /api/v1/content-analysis/analyze-directory` - Analyze without saving
   - `POST /api/v1/content-analysis/analyze-and-save` - Analyze and persist to DB
   - `GET /api/v1/dashboard/kpis` - Dashboard metrics
   - `GET /api/v1/analysis/findings` - Findings list
   - `DELETE /api/v1/maintenance/data-sources?confirm=true` - Clear all data

### Access Points (CURRENT)

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3010 |
| Backend API | http://localhost:3011 |
| Swagger Docs | http://localhost:3011/docs |
| Health Check | http://localhost:3011/health |

---

## 5 Focus Areas (Classification)

| Focus Area | Description | Keywords |
|------------|-------------|----------|
| **BUSINESS_PROTECTION** | Fraud, cybersecurity, vendor manipulation | fraud, theft, unauthorized, manipulation, suspicious |
| **BUSINESS_CONTROL** | Process bottlenecks, vendor/customer management | vendor, customer, master data, invoice, payment, balance |
| **ACCESS_GOVERNANCE** | SoD violations, authorization control | sod, segregation of duties, privilege, authorization |
| **TECHNICAL_CONTROL** | System dumps, infrastructure issues | memory dump, abap dump, cpu usage, system crash |
| **JOBS_CONTROL** | Job performance, resource utilization | job failed, batch job, background job, job runtime |

**Classification Logic**: `backend/app/services/content_analyzer/llm_classifier.py` → `analyze_without_llm()` method

---

## Analysis Principles (User-Defined)

### Core Analyzer Workflow

```
PHASE 1: CONTEXT LOADING
├── Load general TH knowledge (/docs/th-context/readmore/*)
└── Alert-specific context from 4 artifacts

PHASE 2: ARTIFACT READING (Sequential)
├── 1. Code_*       → Alert logic (ABAP/SQL)
├── 2. Explanation_* → Business context (WHY it matters)
├── 3. Metadata_*   → Parameters (BACKDAYS, filters)
└── 4. Summary_*    → ACTUAL OUTPUT TO ANALYZE

PHASE 3: ANALYSIS
├── Summary_* is PRIMARY data source
├── Other artifacts provide CONTEXT
├── Classify into 1 of 5 Focus Areas
└── Perform Qualitative + Quantitative analysis

PHASE 4: SCORING
├── Qualitative: "What happened?" → Event description
└── Quantitative: "How much/many?" → Counts, amounts
```

### Qualitative vs Quantitative Examples

| Type | Alert | Key Indicator |
|------|-------|---------------|
| Qualitative | "Inactive Vendor" | Problem description, cleanup needed |
| Quantitative | "Inactive Vendor with High Balance" | **$6.7M** at risk, specific amounts |

---

## Recent Session Work (2025-11-26)

### Files Modified

1. **backend/app/api/content_analysis.py**
   - Added `analyze-and-save` endpoint
   - Fixed DataSource model fields (file_format, data_type instead of file_type)
   - Uses correct API for persisting findings to database

2. **backend/app/services/content_analyzer/analyzer.py**
   - Fixed `_fallback_analysis()` to extract metrics from ALL artifacts (not just summary)
   - Added `monetary_amount` to quantitative_analysis dict
   - Improved `_fallback_classification()` keywords

3. **backend/app/services/content_analyzer/llm_classifier.py**
   - Updated `analyze_without_llm()` keywords:
     - Added vendor/customer/balance/financial to BUSINESS_CONTROL
     - Made TECHNICAL_CONTROL keywords more specific (avoid generic "system")

4. **backend/app/services/content_analyzer/scoring_engine.py**
   - Fixed count regex to handle comma-separated numbers ("1,943" → 1943)
   - Pattern: `r'([\d,]+)\s+(?:records?|items?|vendors?|...)'`

5. **frontend/src/pages/Upload.tsx**
   - Added multi-file artifact upload section
   - Add files one-by-one workflow
   - Color-coded categorization (Code/Explanation/Metadata/Summary)
   - Fixed API URLs to use `http://localhost:3011/api/v1`
   - Flexible file name matching (handles "Metadata " with space)

### Commits Made (Branch: claude/claude-md-miecwc4mecipjiww-01E2YVoZHeHvYiRZUEUYKn4j)

1. `Fix DataSource model fields in analyze-and-save endpoint`
2. `Improve quantitative extraction and focus area classification`
3. `Fix classification keywords and count regex for comma-separated numbers`
4. `Add multi-file artifact upload to Upload page`
5. `Update Upload page to add artifact files one-by-one`
6. `Fix API URLs in Upload page to use correct backend URL`
7. `Make artifact file categorization more flexible (handle spaces after prefix)`

---

## Testing Commands

### Test Content Analyzer (CLI)

```bash
# Upload artifacts via Swagger UI first, get artifacts_path

# Analyze without saving (see full output)
curl -X POST "http://localhost:3011/api/v1/content-analysis/analyze-directory" \
  -H "Content-Type: application/json" \
  -d '{"directory_path": "/app/storage/artifacts/YOUR_PATH", "use_llm": false}'

# Analyze and save to database
curl -X POST "http://localhost:3011/api/v1/content-analysis/analyze-and-save" \
  -H "Content-Type: application/json" \
  -d '{"directory_path": "/app/storage/artifacts/YOUR_PATH", "use_llm": false}'
```

### Clear Database and Re-test

```bash
# Clear all data
curl -X DELETE "http://localhost:3011/api/v1/maintenance/data-sources?confirm=true"

# Re-initialize with seed data (optional)
docker compose exec backend python -m app.utils.init_db
```

### Rebuild After Code Changes

```bash
# Pull latest code
git pull origin claude/claude-md-miecwc4mecipjiww-01E2YVoZHeHvYiRZUEUYKn4j

# Rebuild backend (fast - uses cache)
docker compose build backend && docker compose up -d backend

# Rebuild frontend (fast - uses cache)
docker compose build frontend && docker compose up -d frontend

# Full rebuild (slow - no cache)
docker compose build --no-cache backend && docker compose up -d backend
```

---

## Current Scoring Logic (TO BE REFINED)

### Risk Score Calculation

```python
# scoring_engine.py

# Base scores by severity
SEVERITY_BASE_SCORES = {
    "Critical": 85,  # USER WANTS: 90
    "High": 65,      # USER WANTS: 75
    "Medium": 45,    # USER WANTS: 60
    "Low": 25,       # USER WANTS: 50
}

# Count adjustment
if count >= 1000: +15
elif count >= 500: +10
elif count >= 100: +5

# Money adjustment
if amount >= 1_000_000: +20
elif amount >= 100_000: +15
elif amount >= 10_000: +10
elif amount >= 1_000: +5

# Focus area multiplier
FOCUS_AREA_MULTIPLIERS = {
    "BUSINESS_PROTECTION": 1.2,
    "BUSINESS_CONTROL": 1.0,
    "ACCESS_GOVERNANCE": 1.15,
    "TECHNICAL_CONTROL": 0.9,
    "JOBS_CONTROL": 0.85,
}

final_score = (base + count_adj + money_adj) * multiplier
```

### PENDING: Normalize Count by BACKDAYS

The user explained that raw count must be normalized by BACKDAYS parameter from Metadata file:

```
Normalized_Count = Raw_Count / BACKDAYS
Risk = f(Normalized_Count, ...)
```

**This is NOT YET IMPLEMENTED.**

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `backend/app/api/content_analysis.py` | Content analysis endpoints |
| `backend/app/services/content_analyzer/analyzer.py` | Main analysis orchestrator |
| `backend/app/services/content_analyzer/llm_classifier.py` | Focus area classification |
| `backend/app/services/content_analyzer/scoring_engine.py` | Risk scoring logic |
| `backend/app/services/content_analyzer/artifact_reader.py` | File parsing (txt, docx, xlsx) |
| `frontend/src/pages/Upload.tsx` | Multi-file upload UI |
| `frontend/src/pages/Dashboard.tsx` | Dashboard display |
| `docs/th-context/readmore/*.md` | Focus Area definitions |

---

## Next Steps (Prioritized)

### Immediate

1. **Implement updated severity base scores** (90/75/60/50)
2. **Add BACKDAYS parameter extraction** from Metadata_* file
3. **Normalize count by BACKDAYS** for meaningful risk scoring
4. **Define BUSINESS_PROTECTION specific scoring rules**

### Short-term

5. **Create rules database structure** for storing scoring logic
6. **Define scoring rules for each Focus Area** (5 total)
7. **Improve qualitative analysis** (severity reasoning, what_happened)

### Medium-term

8. **Enable LLM mode** for better classification (requires API key)
9. **Add SoDA report support** (different artifact structure)
10. **Create feedback loop** for iterative improvement

---

## Known Issues

1. **Metadata parameter extraction not implemented** - BACKDAYS not used
2. **Severity always defaults to "Medium"** - not derived from content
3. **Money adjustment thresholds are arbitrary** - need business input
4. **LLM mode disabled** - no API key configured in Docker env

---

## Context Documents (User Mentioned but NOT in Repo)

- `docs/about_skywind/TXT/*` - Skywind alert parameter documentation
- `Core Principles of THA Analysis.md` - On user's Windows machine

**Ask user to provide these documents or copy to repo.**

---

## Git Branch

**Working Branch**: `claude/claude-md-miecwc4mecipjiww-01E2YVoZHeHvYiRZUEUYKn4j`

All commits from this session are on this branch. To continue:

```bash
git checkout claude/claude-md-miecwc4mecipjiww-01E2YVoZHeHvYiRZUEUYKn4j
git pull origin claude/claude-md-miecwc4mecipjiww-01E2YVoZHeHvYiRZUEUYKn4j
```

---

## Changelog

### 2025-11-26 (Session End)
- **WORKING**: End-to-end flow: Upload 4 artifacts → Analyze → Dashboard shows results
- **WORKING**: Multi-file upload UI (add files one-by-one)
- **WORKING**: Content Analyzer with pattern-based classification
- **FIXED**: Quantitative extraction ($45M, 1,943 vendors from text)
- **FIXED**: Focus area classification (vendor alerts → BUSINESS_CONTROL)
- **FIXED**: Comma-separated number parsing (1,943 not 943)
- **FIXED**: API URLs in Upload page (port 3011)
- **FIXED**: File categorization (handles "Metadata " with space)
- **TESTED**: "Rarely Used Vendors" alert → $45M exposure, Risk 80
- **IN PROGRESS**: Defining BUSINESS_PROTECTION scoring rules
- **PENDING**: BACKDAYS parameter extraction and normalization
- **PENDING**: Updated severity base scores (90/75/60/50)

### 2025-11-26 (Earlier)
- **ADDED**: Intelligent Content Analyzer module
- **ADDED**: Content Analysis API endpoints
- **ADDED**: Multi-file upload endpoint
- **FIXED**: Content analyzer `__init__.py` missing exports

### 2025-11-25
- **UPDATED**: Frontend port 3010, Backend port 3011
- **UPDATED**: Docker Compose with VITE_API_BASE_URL

### 2025-11-23
- **FIXED**: Docker environment setup
- **FIXED**: Database schema mismatch
- **VERIFIED**: Dashboard fully functional

---

**END OF HANDOVER DOCUMENT**

*This document should be updated after each verified milestone. Keep it accurate for seamless AI agent collaboration.*
