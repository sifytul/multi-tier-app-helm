# Multi-Tier Application Stack

A production-ready microservices architecture deployed on Kubernetes via Helm, featuring a Node.js API Gateway, Python FastAPI backend, MySQL database, and Redis caching layer.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ API Gateway │────▶│  Backend    │────▶│   MySQL     │
│  (Node.js)  │     │  (Python)   │     │  Database   │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Redis    │
                    │   Cache     │
                    └─────────────┘
```

## Tech Stack

| Component               | Technology        | Port |
| ----------------------- | ----------------- | ---- |
| API Gateway             | Node.js + Express | 5000 |
| Backend API             | Python + FastAPI  | 6000 |
| Database                | MySQL 8.0         | 3306 |
| Cache                   | Redis 7.2         | 6379 |
| Container Orchestration | Kubernetes + Helm | -    |

## Key Features

- **Connection Pooling** - MySQL and Redis connection pools for efficient resource utilization
- **Redis Caching** - 5-minute TTL caching with cache invalidation on writes
- **Horizontal Pod Autoscaling** - HPA configured for auto-scaling based on CPU metrics
- **gRPC & REST** - Modern async APIs with proper error handling
- **Container Optimizations** - Multi-stage builds, non-root users, production NODE_ENV

## Getting Started

### Docker Compose (Local Development)

```bash
docker-compose up --build
```

### Kubernetes (Helm Deployment)

```bash
cd helm-charts/app-stack
helm install app-stack .
```

## API Endpoints

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | `/health`        | Gateway health check |
| GET    | `/api/health`    | Full stack health    |
| GET    | `/api/items`     | List all items       |
| GET    | `/api/items/:id` | Get item by ID       |
| POST   | `/api/items`     | Create new item      |

## Performance Optimizations

- Connection pooling for database and cache (reduces connection overhead)
- Axios request timeouts (5s) to prevent hanging requests
- gzip compression on API Gateway
- Production-ready resource limits in Helm charts

## Project Structure

```
.
├── api-gateway/           # Node.js API Gateway
│   ├── src/index.js      # Express app with proxy routes
│   └── Dockerfile        # Alpine-based container
├── backend-api/           # Python FastAPI Backend
│   ├── app/main.py       # REST API with Redis caching
│   └── Dockerfile        # Slim Python container
├── helm-charts/          # Kubernetes Helm charts
│   └── app-stack/       # Umbrella chart (4 subcharts)
├── mysql/                # Database initialization
├── redis/                # Redis configuration
└── docker-compose.yaml   # Local development setup
```

## Environment Variables

### API Gateway

- `PORT` - Server port (default: 5000)
- `BACKEND_URL` - Backend API URL

### Backend API

- `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`
- `CACHE_TTL` - Cache time-to-live in seconds (default: 300)

## Build & Deploy

```bash
# Build images
docker build -t api-gateway ./api-gateway
docker build -t backend-api ./backend-api

# Tag and push to registry
docker tag api-gateway myregistry/api-gateway:1.0.0
docker push myregistry/api-gateway:1.0.0
```

## Monitoring

Health checks are available at:

- Gateway: `GET /health`
- Backend: `GET /health` (includes DB and Redis status)
- Combined: `GET /api/health`

---

Built with Kubernetes, Helm, Docker, Node.js, Python, MySQL & Redis
