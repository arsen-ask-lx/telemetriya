@echo off
REM Script to stop Docker containers (Windows)

REM Change to script directory
cd /d "%~dp0.."

REM Stop containers
echo Stopping Docker containers...
docker-compose -f infra/docker/docker-compose.yml down

echo.
echo Containers stopped successfully!
echo Note: Volumes are preserved. To remove volumes, run: docker-compose -f infra/docker/docker-compose.yml down -v
pause
