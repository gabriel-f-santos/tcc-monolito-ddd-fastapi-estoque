#!/bin/sh
# Run Alembic migrations

echo "Waiting for postgres..."
alembic upgrade head

echo "Postgres started"
# Start the FastAPI application with Uvicorn
exec uvicorn src.main:app --host 0.0.0.0 --port 8080 --proxy-headers --forwarded-allow-ips "*"
