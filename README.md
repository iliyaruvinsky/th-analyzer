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
├── ml_models/        # Trained ML models
├── docs/             # Documentation and context
├── scripts/          # Utility scripts
└── docker-compose.yml
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local frontend development)

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Documentation

Once the backend is running, visit:
- API: http://localhost:3011
- Swagger UI: http://localhost:3011/docs
- ReDoc: http://localhost:3011/redoc
- Frontend: http://localhost:3010

## Documentation

- [Quick Start Guide](QUICK_START.md)
- [Quick Test Guide](QUICK_TEST.md) - **Start here for testing!**
- [Testing Checklist](TESTING_CHECKLIST.md) - Comprehensive testing
- [Testing Summary](TESTING_SUMMARY.md) - Testing overview
- [Next Steps](NEXT_STEPS.md) - Roadmap and enhancements
- [Deployment Guide](DEPLOYMENT.md)
- [Validation Report](VALIDATION_REPORT.md)
- [Merge Strategy](MERGE_STRATEGY.md)

## Related Projects

This repository also contains the [Skywind Plugin Marketplace](plugins/) - a collection of AI coding assistant plugins for Cursor, Claude Code, and Windsurf.

## License

Proprietary - Skywind Software Group
