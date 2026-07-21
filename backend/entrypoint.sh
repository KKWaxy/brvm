#!/usr/bin/env bash
set -e

# Wait for Postgres to be ready using the helper script (scripts/wait-for-postgres.py)
if [ -n "${DATABASE_URL}" ]; then
  echo "Waiting for Postgres (DATABASE_URL set)"
  if python3 /app/scripts/wait-for-postgres.py; then
    echo "Postgres ready"
  else
    echo "Postgres did not become ready in time" >&2
    exit 1
  fi
else
  echo "No DATABASE_URL set, skipping Postgres wait"
fi

# Run alembic migrations (if alembic.ini is present)
if command -v alembic >/dev/null 2>&1; then
  echo "Running alembic upgrade head"
  if alembic upgrade head; then
    echo "Alembic migrations applied successfully"
  else
    echo "Alembic migrations failed" >&2
    exit 1
  fi
else
  echo "alembic not found, skipping migrations"
fi

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port 8000
