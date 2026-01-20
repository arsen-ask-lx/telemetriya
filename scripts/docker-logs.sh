#!/bin/bash
# Script to view Docker logs

set -e

# Change to script directory
cd "$(dirname "$0")/.."

# Show logs
echo "Showing Docker logs (Ctrl+C to exit)..."
docker-compose -f infra/docker/docker-compose.yml logs -f "$@"
