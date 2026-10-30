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
- **Automated Tests:** Unit tests for URL validation and rate limiting.

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

## 📁 Project Structure

```text
.
├── backend/
│   ├── DockerFile
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── src/
│   │   └── app/
│   │       ├── api/
│   │       │   ├── dependencies.py
│   │       │   └── routers/
│   │       │       └── links.py
│   │       ├── core/
│   │       │   └── id_generator.py
│   │       ├── database/
│   │       │   ├── cache/
│   │       │   └── cassandra/
│   │       ├── errors/
│   │       │   ├── exceptions.py
│   │       │   └── handlers.py
│   │       ├── repositories/
│   │       │   └── link_repository.py
│   │       ├── schemas/
│   │       │   └── links.py
│   │       ├── services/
│   │       │   └── shorten_url_service.py
│   │       ├── config.py
│   │       └── main.py
│   └── tests/
│       └── unit/
│           ├── rate_limitter.py
│           └── test_url_validator.py
│
├── frontend/
│   ├── DockerFile
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── package.json
│
├── nginx/
│   ├── default.conf
│   └── nginx.conf
│
├── test/
│   ├── package.json
│   ├── read.js
│   └── write.js
│
└── docker-compose.yml
```

## 🏗️ Architecture

The application follows a modular architecture, separating responsibilities between the frontend, backend, databases, and infrastructure.

### Backend

Built with FastAPI, the backend is organized into different layers:

- **API:** Handles HTTP requests and exposes the application endpoints.
- **Services:** Contains the business logic for shortening URLs.
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

A lightweight interface built with HTML, CSS, and JavaScript that allows users to submit long URLs and retrieve their shortened versions.

## ⚡ Getting Started

### Requirements

Make sure you have the following installed:

- Docker
- Docker Compose

### Running Locally

To start the entire application locally, simply execute the following command from the project root:

```bash
docker compose up --build -d
```

This command builds the required Docker images and starts all services in detached mode.

To check the running containers:

```bash
docker compose ps
```

To inspect application logs:

```bash
docker compose logs -f
```

To stop all services:

```bash
docker compose down
```

## 🧪 Load Testing

The project includes JavaScript-based load tests to evaluate API performance under concurrent requests.

The `test/` directory contains:

- `read.js`: Tests URL redirection and retrieval performance.
- `write.js`: Tests URL creation performance.

Run the tests from the `test/` directory using:

```bash
npm install
```

Then execute the desired test:

```bash
npm run test:read
```

```bash
npm run test:write
```

## 🧩 API Documentation

FastAPI automatically generates interactive API documentation.

Once the application is running, access:

- Swagger UI: `http://localhost/docs`
- ReDoc: `http://localhost/redoc`

*The actual access URL depends on the Nginx configuration.*

## 📌 Future Improvements

- Improve distributed ID generation.
- Add monitoring and observability.
- Expand automated testing.
- Optimize database and cache performance.

## 📄 License

This project is intended for educational purposes and as a portfolio project demonstrating backend development, distributed systems, containerization, and performance testing.