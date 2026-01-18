#!/bin/bash
# Script to start Docker containers

set -e

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Change to script directory
cd "$(dirname "$0")/.."

# Start containers
echo "Starting Docker containers..."
docker-compose -f infra/docker/docker-compose.yml up -d

echo "Containers started successfully!"
echo "Use 'docker-compose -f infra/docker/docker-compose.yml ps' to check status."
echo "Use 'docker-compose -f infra/docker/docker-compose.yml logs -f' to view logs."
