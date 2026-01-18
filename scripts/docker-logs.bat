@echo off
REM Script to view Docker logs (Windows)

REM Change to script directory
cd /d "%~dp0.."

REM Show logs
echo Showing Docker logs (Ctrl+C to exit)...
docker-compose -f infra/docker/docker-compose.yml logs -f %*
