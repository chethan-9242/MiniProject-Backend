# 🐳 Docker Guide for SwasthVedha - Complete Beginner Tutorial

## What is Docker?
Docker packages your application and all its dependencies into a "container" that runs the same way on any computer. Think of it like a shipping container for software!

## 📋 Prerequisites

### 1. Install Docker Desktop
- **Windows**: Download from [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- **Mac**: Download from [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- **Linux**: Follow [Docker Engine installation guide](https://docs.docker.com/engine/install/)

### 2. Verify Installation
Open Command Prompt/PowerShell and run:
```bash
docker --version
docker-compose --version
```
You should see version numbers.

## 🚀 Quick Start (3 Commands!)

### Step 1: Navigate to your project
```bash
cd C:\Users\Chethan\OneDrive\Desktop\SwasthVedha
```

### Step 2: Build and start everything
```bash
docker-compose up --build
```

### Step 3: Open your browser
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 📁 What Each File Does

| File | Purpose |
|------|---------|
| `Dockerfile` | Instructions to build backend container |
| `Dockerfile.frontend` | Instructions to build frontend container |
| `docker-compose.yml` | Orchestrates all services together |
| `nginx.conf` | Web server configuration |
| `.dockerignore` | Files to exclude from Docker build |

## 🛠️ Common Commands

### Start everything
```bash
docker-compose up
```

### Start in background (detached)
```bash
docker-compose up -d
```

### Stop everything
```bash
docker-compose down
```

### Rebuild after code changes
```bash
docker-compose up --build
```

### View logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
```

### Access container shell
```bash
# Backend container
docker-compose exec backend bash

# Frontend container
docker-compose exec frontend sh
```

## 🔧 Troubleshooting

### Problem: "Port already in use"
**Solution**: Stop other services using ports 3000 or 8000
```bash
# Windows - find what's using port 8000
netstat -ano | findstr :8000
# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Problem: "Docker daemon not running"
**Solution**: Start Docker Desktop application

### Problem: "Build failed"
**Solution**: Check logs and rebuild
```bash
docker-compose logs backend
docker-compose up --build --no-cache
```

### Problem: "Out of memory"
**Solution**: Increase Docker memory limit in Docker Desktop settings

## 📊 What's Running

After `docker-compose up`, you'll have:

| Service | URL | Purpose |
|---------|-----|---------|
| Backend API | http://localhost:8000 | FastAPI server |
| Frontend | http://localhost:3000 | React app |
| Database | localhost:5432 | PostgreSQL (optional) |
| Redis | localhost:6379 | Caching (optional) |

## 🎯 Development Workflow

### 1. Make code changes
Edit your files normally in VS Code/IDE

### 2. Rebuild containers
```bash
docker-compose up --build
```

### 3. View changes
Refresh your browser

### 4. Check logs if issues
```bash
docker-compose logs backend
```

## 🔄 Environment Variables

Create `.env` file in project root:
```env
# Backend
FLAN_T5_DEVICE=cpu
DEBUG_MODE=false

# Frontend
REACT_APP_API_URL=http://localhost:8000

# Database
POSTGRES_DB=swasthvedha
POSTGRES_USER=swasthvedha
POSTGRES_PASSWORD=swasthvedha123
```

## 🚀 Production Deployment

### Build production images
```bash
docker-compose -f docker-compose.prod.yml up --build
```

### Push to registry
```bash
docker tag swasthvedha-backend your-registry/swasthvedha-backend
docker push your-registry/swasthvedha-backend
```

## 📚 Next Steps

1. **Learn Docker basics**: [Docker Tutorial](https://docs.docker.com/get-started/)
2. **Understand containers**: [Container vs VM](https://www.docker.com/resources/what-container)
3. **Docker Compose**: [Multi-container apps](https://docs.docker.com/compose/)

## ❓ Need Help?

- Check logs: `docker-compose logs`
- Restart everything: `docker-compose down && docker-compose up --build`
- Google the error message
- Ask in Docker community forums

---

**🎉 Congratulations!** You now have SwasthVedha running in Docker containers!
