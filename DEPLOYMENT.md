# Deployment Guide

## Local Deployment

### Using Docker Compose (Recommended)

1. **Start all services:**
```bash
docker-compose up -d
```

2. **Initialize database:**
```bash
docker-compose exec backend python -m app.utils.init_db
```

3. **Access the application:**
- Frontend: http://localhost:3010
- Backend API: http://localhost:3011
- API Docs: http://localhost:3011/docs

4. **View logs:**
```bash
docker-compose logs -f
```

5. **Stop services:**
```bash
docker-compose down
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
docker-compose -f docker-compose.prod.yml up -d
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
docker-compose exec backend python -c "from app.core.database import engine; engine.connect(); print('Database connected')"
```

## Troubleshooting

### Database Connection Issues

1. Verify PostgreSQL is running:
```bash
docker-compose ps postgres
```

2. Check connection string in `.env`

3. Verify network connectivity:
```bash
docker-compose exec backend ping postgres
```

### Frontend Not Loading

1. Check backend is running:
```bash
curl http://localhost:3011/health
```

2. Verify CORS settings in backend
3. Check browser console for errors
4. Verify API base URL in frontend `.env`

### File Upload Issues

1. Check storage directory permissions:
```bash
ls -la storage/
```

2. Verify file size limits in backend
3. Check disk space:
```bash
df -h
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
docker-compose exec postgres pg_dump -U tha_user treasure_hunt_analyzer > backup.sql

# Restore
docker-compose exec -T postgres psql -U tha_user treasure_hunt_analyzer < backup.sql
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

