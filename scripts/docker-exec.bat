@echo off
REM Script to connect to PostgreSQL using psql (Windows)

setlocal enabledelayedexpansion

REM Change to script directory
cd /d "%~dp0.."

REM Load environment variables from .env file (if exists)
if exist .env (
    for /f "tokens=*" %%a in ('type .env ^| findstr /v "^#"') do (
        set "%%a"
    )
)

REM Set defaults
if "%POSTGRES_USER%"=="" set POSTGRES_USER=telemetriya
if "%POSTGRES_DB%"=="" set POSTGRES_DB=telemetriya

REM Connect to PostgreSQL
echo Connecting to PostgreSQL as user '%POSTGRES_USER%' to database '%POSTGRES_DB%'...
docker-compose -f infra/docker/docker-compose.yml exec postgres psql -U !POSTGRES_USER! -d !POSTGRES_DB! %*

pause
