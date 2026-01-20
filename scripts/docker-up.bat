@echo off
REM Script to start Docker containers (Windows)

REM Change to script directory
cd /d "%~dp0.."

REM Start containers
echo Starting Docker containers...
docker-compose -f infra/docker/docker-compose.yml up -d

echo.
echo Containers started successfully!
echo Use 'docker-compose -f infra/docker/docker-compose.yml ps' to check status.
echo Use 'docker-compose -f infra/docker/docker-compose.yml logs -f' to view logs.
pause
