#!/bin/bash
# Create a new Alembic migration revision with autogenerate

# Check if message parameter is provided
if [ -z "$1" ]; then
    echo "Error: Migration message is required"
    echo "Usage: $0 \"<migration message>\""
    echo "Example: $0 \"Add email column to users\""
    exit 1
fi

MESSAGE="$1"

echo "Creating new Alembic migration..."
alembic revision --autogenerate -m "$MESSAGE"

echo "Migration created successfully!"
echo "Review the generated migration file and adjust if needed."
