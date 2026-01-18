#!/bin/bash
# Script to connect to PostgreSQL using psql

set -e

# Change to script directory
cd "$(dirname "$0")/.."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set defaults
POSTGRES_USER=${POSTGRES_USER:-telemetriya}
POSTGRES_DB=${POSTGRES_DB:-telemetriya}

# Connect to PostgreSQL
echo "Connecting to PostgreSQL as user '$POSTGRES_USER' to database '$POSTGRES_DB'..."
docker-compose -f infra/docker/docker-compose.yml exec -T postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" "$@"
