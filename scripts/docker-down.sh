#!/bin/bash
# Script to stop Docker containers

set -e

# Change to script directory
cd "$(dirname "$0")/.."

# Stop containers
echo "Stopping Docker containers..."
docker-compose -f infra/docker/docker-compose.yml down

echo "Containers stopped successfully!"
echo "Note: Volumes are preserved. To remove volumes, run: docker-compose -f infra/docker/docker-compose.yml down -v"
