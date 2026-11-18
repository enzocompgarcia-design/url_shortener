# Backend

FastAPI backend for the URL Shortener project. It exposes the endpoints used to
create short links, redirect to the original URLs and report dependency
health/readiness (`/health`, `/ready`), using Cassandra for persistence and
Redis for caching and ID generation.

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
```

## Configuration

The application reads its settings from environment variables. Create your local
env file from the example:

```bash
cp .env.example .env
```

Adjust the values as needed. See the root [`README.md`](../README.md) for the
full list of variables.

`uv run` executes the command inside the project environment, so there is no
need to activate `.venv` manually. If you prefer, you can still activate it:

```bash
source .venv/bin/activate
```

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
```