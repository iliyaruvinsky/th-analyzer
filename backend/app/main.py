from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import router
from app.api.maintenance import router as maintenance_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
)

# CORS middleware - MUST be first, before any routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3010",
        "http://localhost:3001",
        "http://localhost:3000",
        "http://127.0.0.1:3010",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include routers
app.include_router(router, prefix=settings.API_V1_PREFIX)
app.include_router(maintenance_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return {"message": "Treasure Hunt Analyzer API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from app.core.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

