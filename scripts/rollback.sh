#!/bin/bash
# Run Alembic migrations to downgrade database schema (one version down)

set -e  # Exit on error

echo "Rolling back last Alembic migration..."
alembic downgrade -1

echo "Rollback completed successfully!"
