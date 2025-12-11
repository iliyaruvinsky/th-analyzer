# Treasure Hunt Analyzer (THA)

Comprehensive system for analyzing Skywind platform alerts and reports, providing insights across 6 focus areas with advanced visualization and reporting capabilities.

## Features

- **Multi-format ingestion**: PDF, CSV, DOCX, Skywind 4C Excel, Skywind SoDA Excel
- **6 Focus Area classification**: Business Protection, Business Control, Access Governance, Technical Control, Jobs Control, S/4HANA Excellence
- **Issue grouping**: Automatic grouping of findings by issue types
- **Hybrid money loss calculation**: LLM reasoning + ML learning
- **Interactive dashboards**: Charts, tables, and drill-down capabilities
- **Risk assessment**: Detailed risk explanations and financial impact analysis

## Project Structure

```
treasure-hunt-analyzer/
├── backend/          # FastAPI backend
├── frontend/          # React frontend
├── docs/             # Documentation and context
├── scripts/          # Utility scripts
├── plugins/          # AI assistant plugins
├── aws/              # AWS deployment configs
└── docker compose.yml
```

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (to clone the repository)

### 5-Minute Setup

```bash
# 1. Start all services
docker compose up -d

# 2. Initialize database
docker compose exec backend python -m app.utils.init_db

# 3. Verify services
curl http://localhost:3011/health
```

### Access the Application

- **Frontend**: http://localhost:3010
- **Backend API**: http://localhost:3011
- **API Documentation**: http://localhost:3011/docs

### Test with Sample File

**Using Swagger UI:**
1. Open http://localhost:3011/docs
2. Find `POST /api/v1/ingestion/upload`
3. Upload a Skywind alert file
4. Run analysis with the returned `data_source_id`

**Using curl:**
```bash
# Upload file
curl -X POST "http://localhost:3011/api/v1/ingestion/upload" \
  -F "file=@path/to/alert.xlsx"

# Run analysis (use data_source_id from upload response)
curl -X POST "http://localhost:3011/api/v1/analysis/run" \
  -H "Content-Type: application/json" \
  -d '{"data_source_id": 1}'
```

### Stopping Services

```bash
docker compose down
```

## API Documentation

Once the backend is running, visit:
- API: http://localhost:3011
- Swagger UI: http://localhost:3011/docs
- ReDoc: http://localhost:3011/redoc
- Frontend: http://localhost:3010

## Documentation

- [Testing Guide](TESTING.md) - **Start here for testing!** (Quick test + comprehensive checklist)
- [Deployment Guide](DEPLOYMENT.md) - Production deployment and Docker troubleshooting
- [AI Assistant Guide](CLAUDE.md) - For AI agents working on the project
- [Development Handover](llm_handover.md) - Current project state and changelog
- [Docker Setup Guide](DOCKER_SETUP_GUIDE.md) - Docker configuration
- [Docker Troubleshooting](DOCKER_TROUBLESHOOTING.md) - Container issues

## Related Projects

This repository also contains the [Skywind Plugin Marketplace](plugins/) - a collection of AI coding assistant plugins for Cursor, Claude Code, and Windsurf.

## License

Proprietary - Skywind Software Group
