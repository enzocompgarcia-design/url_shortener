# 🔗 URL Shortener

A URL Shortener built with **FastAPI**, designed to create short links from long URLs. The project uses a containerized architecture with Nginx as a reverse proxy and load balancer, Cassandra for data persistence, and Redis for caching and ID generation.

## 🚀 Features

- **URL Shortening:** Convert long URLs into short, easy-to-share links.
- **Redirection:** Automatically redirect users to the original URL.
- **Unique ID Generation:** Generate compact identifiers for shortened URLs.
- **Caching:** Redis integration to improve lookup performance.
- **Load Balancing:** Nginx distributes incoming requests across multiple API instances.
- **Rate Limiting:** Protect the API against excessive requests.
- **Containerization:** Docker-based environment for easier deployment and scalability.
- **Automated Tests:** Unit and API tests for URL validation, dependency failures and health checks.

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend API framework |
| Redis | Caching and ID management |
| Cassandra | Data persistence |
| Nginx | Reverse proxy and load balancing |
| Docker | Containerization |
| JavaScript | Frontend and load testing |
| HTML / CSS | Frontend interface |
| Pytest | Backend testing |

## 🏗️ Architecture

The application follows a modular architecture, separating responsibilities between the frontend, backend, databases, and infrastructure.

### Backend

Built with FastAPI, the backend is organized into different layers:

- **API:** Handles HTTP requests and exposes the application endpoints.
- **Services:** Contains the business logic for shortening URLs and for checking dependency health/readiness.
- **Repositories:** Responsible for data access operations.
- **Database:** Manages connections to Cassandra and Redis.
- **Core:** Contains the ID generator.
- **Schemas:** Defines request and response data structures.
- **Errors:** Centralizes custom exceptions and exception handlers.

### Infrastructure

- **Nginx:** Acts as a reverse proxy and distributes incoming requests between API instances.
- **Redis:** Provides caching and supports ID management.
- **Cassandra:** Stores shortened URLs and their corresponding original URLs.
- **Docker Compose:** Orchestrates the application containers.

### Frontend

A lightweight interface built with HTML, CSS, and JavaScript that allows users to submit long URLs and retrieve their shortened versions. Nginx serves these static files directly from `frontend/`.

## ⚡ Getting Started

### Requirements

Make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2+)

### Environment Variables

Before running the project, configure the required environment variables. Example files are provided:

- `.env.example` (project root): variables used by Docker Compose.
- `backend/.env.example`: variables used by the FastAPI backend.

Create your local env files from the examples:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
```

Then update the values as needed (especially secrets/passwords).

#### Root `.env` (Docker Compose)

| Variable | Description | Example |
|---|---|---|
| `REDIS_PASSWORD` | **Required** password for Redis; `docker compose` fails if unset or empty | `change_me_redis_password` |

#### `backend/.env` (API)

| Variable | Description | Example |
|---|---|---|
| `CASSANDRA_HOST` | Cassandra hostname/service name | `cassandra` |
| `CASSANDRA_PORT` | Cassandra port | `9042` |
| `REDIS_URL` | Redis connection URL (password must match `REDIS_PASSWORD`) | `redis://:change_me_redis_password@redis:6379/0` |
| `SECRET_KEY` | Secret/salt used for ID generation (Hashids) | `change_me_secret_key` |
| `ALPHABET` | Alphabet used to encode generated short IDs | `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789` |
| `NAME_CACHE_ID` | Redis key name for the ID counter | `url_shortener:id_counter` |
| `ID_START` | Initial value for the ID counter | `1000` |
| `ORIGINS` | Allowed CORS origins (JSON array) | `["http://localhost"]` |
| `RATE_LIMIT_WRITE` | Rate limit for `POST /link/` (slowapi format) | `10/minute` |
| `RATE_LIMIT_READ` | Rate limit for `GET /link/{code}` (slowapi format) | `120/minute` |
| `CACHE_CHECK_TIMEOUT` | Timeout in seconds for the Redis ping in `/ready` | `2.0` |
| `DATABASE_CHECK_TIMEOUT` | Timeout in seconds for the Cassandra check in `/ready` | `2.0` |

### Running Locally

Start the entire application from the project root:

```bash
docker compose up --build -d
```

This command builds the required Docker images and starts all services in detached mode.

Check the running containers:

```bash
docker compose ps
```

Inspect application logs:

```bash
docker compose logs -f
```

Stop all services:

```bash
docker compose down
```

## 🧪 Load Testing

The project includes JavaScript-based load tests to evaluate API performance under concurrent requests.

The `test/` directory contains:

- `read.js`: Creates a short link and then tests redirection performance against it.
- `write.js`: Tests URL creation performance.
- `hybrid.js`: Tests URL redirection with 80% valid and 20% invalid links

> **Important:** the load tests hit a running instance of the application. Start the stack first with `docker compose up --build -d`.

> **Rate limiting:** by default `POST /link/` allows `10/minute` and `GET /link/{code}` allows `120/minute`. High-concurrency load tests will quickly hit these limits and report HTTP `429` responses. To measure real throughput, raise `RATE_LIMIT_WRITE` and `RATE_LIMIT_READ` in `backend/.env` (for example `100000/minute`), then recreate the containers:
>
> ```bash
> docker compose up -d --force-recreate
> ```

Install the dependencies from the `test/` directory:

```bash
cd test
npm install
```

Then execute the desired test:

```bash
npm run test:read
npm run test:write
npm run test:hybrid
```

## 🧩 API Documentation

FastAPI automatically generates interactive API documentation.

Once the application is running, access:

- Swagger UI: `http://localhost/docs`
- ReDoc: `http://localhost/redoc`

### Health checks

Each API instance also exposes two endpoints hidden from the OpenAPI schema:

- `GET /health`: liveness probe; returns `200 {"status": "ok"}`.
- `GET /ready`: checks Redis and Cassandra; returns `200 {"status": "ok"}` when both respond, or `503` with `detail` and `error_code` from the global exception handler. Docker Compose uses this endpoint for the API healthchecks.

Nginx does not proxy these paths (port 80 requests fall back to the frontend), so call them directly on an API instance, e.g. `http://localhost:8000/ready` when running the API locally.

## 📌 Future Improvements

- Improve distributed ID generation.
- Add monitoring and observability.
- Expand automated testing.
- Optimize database and cache performance.

## 📄 License

This project is intended for educational purposes and as a portfolio project demonstrating backend development, distributed systems, containerization, and performance testing.