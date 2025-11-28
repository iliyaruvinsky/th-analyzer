# How to Start/Initialize the Treasure Hunt Analyzer Servers

## Quick Start (3 Steps)

### Step 1: Navigate to Project Directory

Open PowerShell or Command Prompt and run:

```powershell
cd path\to\treasure-hunt-analyzer
```

**Note:** Replace with your actual project path, or skip if already in the directory.

### Step 2: Start All Services

Run one of these commands (depending on your Docker version):

**For newer Docker versions (recommended):**
```powershell
docker compose up -d
```

**For older Docker versions:**
```powershell
docker-compose up -d
```

**What this does:**
- Starts PostgreSQL database
- Starts Backend API server (port 3011)
- Starts Frontend web server (port 3010)
- Runs everything in the background (`-d` flag)

### Step 3: Wait and Verify (30-60 seconds)

Wait about 30-60 seconds for services to start, then check status:

```powershell
docker compose ps
```

**Expected output:**
- `tha-postgres`: Status should show `Up` and `(healthy)`
- `tha-backend`: Status should show `Up` and `(healthy)`
- `tha-frontend`: Status should show `Up`

## Access Your Application

Once all services show "Up":

- **Frontend (Web UI)**: http://localhost:3010
- **Backend API**: http://localhost:3011
- **API Documentation**: http://localhost:3011/docs
- **Health Check**: http://localhost:3011/health

## Troubleshooting

### If services don't start:

1. **Check Docker is running:**
   ```powershell
   docker --version
   ```
   If this fails, start Docker Desktop.

2. **Check for port conflicts:**
   - Port 3011 (backend) or 3010 (frontend) might be in use
   - Check what's using them: `netstat -ano | findstr :3011`

3. **View logs for errors:**
   ```powershell
   docker compose logs backend
   docker compose logs frontend
   ```

4. **Rebuild if needed:**
   ```powershell
   docker compose up -d --build
   ```

### If you see "unhealthy" status:

Wait a bit longer (up to 2 minutes). Health checks need time to pass.

### To stop all services:

```powershell
docker compose down
```

### To restart services:

```powershell
docker compose restart
```

## Initialize Database (First Time Only)

If this is your first time running the system, initialize the database:

```powershell
docker compose exec backend python -m app.utils.init_db
```

This creates all necessary database tables.

## Common Commands Reference

| Command | Purpose |
|---------|---------|
| `docker compose up -d` | Start all services |
| `docker compose down` | Stop all services |
| `docker compose ps` | Check service status |
| `docker compose logs` | View all logs |
| `docker compose logs backend` | View backend logs only |
| `docker compose restart` | Restart all services |
| `docker compose up -d --build` | Rebuild and start |

## Need Help?

- Check logs: `docker compose logs`
- Check status: `docker compose ps`
- Verify Docker: `docker --version`
- Verify ports: Open http://localhost:3011/health in browser

