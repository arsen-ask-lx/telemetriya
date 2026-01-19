#!/bin/bash
# Run Alembic migrations to upgrade the database schema

set -e  # Exit on error

echo "Running Alembic migrations..."
alembic upgrade head

echo "Migrations completed successfully!"
