# Backend

FastAPI backend for the URL Shortener project. It exposes the endpoints used to
create short links and redirect to the original URLs, using Cassandra for
persistence and Redis for caching and ID generation.

> This README is also referenced by `readme = "README.md"` in `pyproject.toml`.
> Keep it in place so `uv sync`/`uv build` do not fail with a missing README
> error.

## Requirements

- [uv](https://docs.astral.sh/uv/) (Python package and project manager)
- Python 3.14 (managed automatically by uv, see `.python-version`)

You do not need to install Python or create a virtual environment manually: uv
downloads the required Python version and creates/manages the `.venv` for you.

## Setup

All commands below are meant to be run from the `backend/` directory.

```bash
cd backend
uv sync
```

`uv sync` does the following:

1. Installs the Python version pinned in `.python-version` (if needed).
2. Creates a local virtual environment in `.venv/`.
3. Installs every dependency from `pyproject.toml`/`uv.lock`, including the
   `dev` dependency group (pytest, pyinstrument).
4. Installs the project itself in editable mode.

Useful variations:

```bash
# Install exactly what is locked in uv.lock (ideal for CI)
uv sync --frozen

# Install only production dependencies (skip the dev group)
uv sync --no-dev

# Recreate the environment from scratch
rm -rf .venv && uv sync
```

> The Docker image uses `uv sync --frozen --no-install-project` because the
> source code is copied afterwards and the app runs from `src/`.

## Configuration

The application reads its settings from environment variables. Create your local
env file from the example:

```bash
cp .env.example .env
```

Adjust the values as needed. See the root [`README.md`](../README.md) for the
full list of variables.

## Running locally

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

`uv run` executes the command inside the project environment, so there is no
need to activate `.venv` manually. If you prefer, you can still activate it:

```bash
source .venv/bin/activate
```

The API will be available at `http://localhost:8000` (Swagger UI at `/docs`).
Cassandra and Redis must be reachable using the hosts/URLs set in `.env`; the
easiest way to start them is `docker compose up -d redis cassandra` from the
project root.

## Tests

```bash
uv run pytest
```

## Managing dependencies

```bash
# Add a runtime dependency
uv add <package>

# Add a dev-only dependency
uv add --dev <package>

# Remove a dependency
uv remove <package>

# Update the lock file (and installed packages)
uv lock --upgrade

# Run any tool installed in the environment
uv run pytest
```

`uv add`/`uv remove` update both `pyproject.toml` and `uv.lock`, so commit both
files together.
