# Deployment Guide

## Local Deployment

### Using Docker Compose (Recommended)

1. **Start all services:**
```bash
docker compose up -d
```

2. **Initialize database:**
```bash
docker compose exec backend python -m app.utils.init_db
```

3. **Access the application:**
- Frontend: http://localhost:3010
- Backend API: http://localhost:3011
- API Docs: http://localhost:3011/docs

4. **View logs:**
```bash
docker compose logs -f
```

5. **Stop services:**
```bash
docker compose down
```

### Manual Local Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your PostgreSQL connection

# Initialize database
python -m app.utils.init_db

# Run migrations (if needed)
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install

# Create .env file (optional)
echo "VITE_API_BASE_URL=http://localhost:3011/api/v1" > .env

# Start development server
npm run dev
```

## Production Deployment

### Docker Production Build

```bash
# Build production images
docker build -t tha-backend:latest ./backend
docker build -t tha-frontend:latest ./frontend

# Run with production settings
docker compose -f docker compose.prod.yml up -d
```

### AWS Deployment

See [aws/README.md](aws/README.md) for detailed AWS deployment instructions.

Key components:
- **ECS Fargate**: Container orchestration
- **RDS PostgreSQL**: Managed database
- **S3**: File storage
- **Application Load Balancer**: Traffic distribution
- **CloudWatch**: Logging and monitoring

### Environment Variables

#### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here
DEBUG=False
ENVIRONMENT=production
STORAGE_TYPE=s3  # or 'local' for on-premises
STORAGE_PATH=./storage  # or S3 bucket name
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret

# LLM Configuration (optional)
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
LLM_PROVIDER=openai
```

#### Frontend (.env)

```env
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
```

## Health Checks

### Backend Health Endpoint

```bash
curl http://localhost:3011/health
```

Expected response:
```json
{"status": "healthy"}
```

### Database Connection Check

```bash
docker compose exec backend python -c "from app.core.database import engine; engine.connect(); print('Database connected')"
```

## Docker Setup and Configuration

### Docker Architecture

The optimized Docker setup includes:
- ✅ Health checks for all services
- ✅ Auto-restart on failure (`unless-stopped`)
- ✅ Named volumes for data persistence
- ✅ Isolated network for security
- ✅ Separate dev and production configs

### Environment Variables

Create `.env` file in project root (optional - defaults work):

```env
# Database
POSTGRES_USER=tha_user
POSTGRES_PASSWORD=tha_password
POSTGRES_DB=treasure_hunt_analyzer

# Backend
SECRET_KEY=your-secret-key-here
DEBUG=True

# Frontend
VITE_API_BASE_URL=http://localhost:3011/api/v1

# Optional: LLM for money loss calculation
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
```

### Rebuilding Containers

After code changes:

```bash
# Rebuild backend
docker compose build backend && docker compose up -d backend

# Rebuild frontend
docker compose build frontend && docker compose up -d frontend

# Rebuild all (no cache)
docker compose build --no-cache
docker compose up -d
```

### Frontend Rebuild

After CSS/TSX changes:

**In Docker:**
```bash
docker compose build frontend && docker compose up -d frontend
```

**Local dev server:**
```bash
cd frontend
npm run dev  # Restart if running
```

**Clear browser cache:**
- Hard refresh: `Ctrl+Shift+R` or `Ctrl+F5`
- Clear cache: `Ctrl+Shift+Delete`

---

## Troubleshooting

### Docker Issues

#### Docker Command Not Recognized

**Quick Fix:**
1. Check Docker Desktop is running (system tray icon)
2. **Close and reopen terminal** (PATH updated when Docker starts)
3. Try `docker --version` in new terminal
4. If still failing, restart computer

**Verification:**
```bash
docker --version
docker compose version
```

**Still Not Working:**
- Reinstall Docker Desktop
- Enable WSL 2 and Virtual Machine Platform (Windows Features)
- Enable virtualization in BIOS
- Check Windows version (Windows 10/11 64-bit Pro/Enterprise/Education)

#### Port Already in Use

```bash
# Stop all containers
docker compose down

# Or change ports in docker-compose.yml
# Frontend: 3010 → 3020
# Backend: 3011 → 3021
# PostgreSQL: 5433 → 5444
```

#### Containers Won't Start

```bash
# View logs
docker compose logs backend
docker compose logs frontend
docker compose logs postgres

# Full rebuild
docker compose down -v  # WARNING: Deletes volumes
docker compose build --no-cache
docker compose up -d
docker compose exec backend python -m app.utils.init_db
```

#### Health Check Fails

```bash
# Wait longer (services need time to start)
sleep 30

# Check specific service logs
docker compose logs -f backend

# Restart unhealthy service
docker compose restart backend
```

### Database Connection Issues

1. **Verify PostgreSQL is running:**
```bash
docker compose ps postgres
```

2. **Check connection string in `.env`:**
   - Host should be `postgres` (not `localhost`) in Docker
   - Port is `5432` internally (5433 is external)

3. **Re-initialize database:**
```bash
docker compose exec backend python -m app.utils.init_db
```

4. **Check database logs:**
```bash
docker compose logs postgres
```

### Frontend Not Loading

1. **Check backend is running:**
```bash
curl http://localhost:3011/health
```

2. **Check browser console** (F12) for errors

3. **Verify CORS settings:** Backend `main.py` should allow `http://localhost:3010`

4. **Clear browser cache:**
   - Hard refresh: `Ctrl+Shift+R`
   - Or: `Ctrl+Shift+Delete` → Clear cached images and files

5. **Rebuild frontend:**
```bash
docker compose build frontend && docker compose up -d frontend
```

### File Upload Issues

1. **Check storage directory permissions:**
```bash
docker compose exec backend ls -la /app/storage
```

2. **Verify file size limits** in backend configuration

3. **Check disk space:**
```bash
docker compose exec backend df -h
```

4. **View upload errors:**
```bash
docker compose logs -f backend | grep upload
```

### Performance Issues

**Slow uploads:**
- Check file size (very large files take time)
- Verify disk space: `docker system df`
- Clean up unused data: `docker system prune`

**Slow analysis:**
- Normal for first run (database warming up)
- Check CPU: `docker stats`
- Check memory: `docker stats`

**High memory usage:**
```bash
# Check container stats
docker stats

# Restart containers
docker compose restart
```

## Scaling

### Horizontal Scaling (ECS)

Update ECS service desired count:
```bash
aws ecs update-service \
  --cluster tha-cluster \
  --service tha-service \
  --desired-count 4
```

### Database Scaling

- **Read Replicas**: For read-heavy workloads
- **Multi-AZ**: For high availability
- **Instance Size**: Upgrade RDS instance class

## Backup and Recovery

### Database Backup

```bash
# Manual backup
docker compose exec postgres pg_dump -U tha_user treasure_hunt_analyzer > backup.sql

# Restore
docker compose exec -T postgres psql -U tha_user treasure_hunt_analyzer < backup.sql
```

### File Storage Backup

For S3:
- Enable versioning
- Configure lifecycle policies
- Use cross-region replication

## Security

1. **Use secrets management** (AWS Secrets Manager, HashiCorp Vault)
2. **Enable HTTPS** (ALB with SSL certificate)
3. **Restrict database access** (security groups, VPC)
4. **Regular security updates** (Docker images, dependencies)
5. **Monitor access logs** (CloudWatch, application logs)

