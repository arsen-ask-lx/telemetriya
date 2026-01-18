"""Tests for docker-compose configuration."""

import os

import pytest
import yaml

DOCKER_COMPOSE_PATH = "infra/docker/docker-compose.yml"
INIT_SQL_PATH = "infra/postgres/init.sql"


def test_docker_compose_file_exists():
    """Test that docker-compose.yml file exists."""
    assert os.path.exists(DOCKER_COMPOSE_PATH), (
        f"docker-compose.yml not found at {DOCKER_COMPOSE_PATH}"
    )


def test_docker_compose_valid_yaml():
    """Test that docker-compose.yml is valid YAML."""
    assert os.path.exists(DOCKER_COMPOSE_PATH), "docker-compose.yml not found"

    with open(DOCKER_COMPOSE_PATH, "r") as f:
        try:
            compose = yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML: {e}")

    assert compose is not None, "docker-compose.yml is empty"
    assert "services" in compose, "No 'services' section in docker-compose.yml"


def test_postgres_service_configured():
    """Test that postgres service is properly configured."""
    assert os.path.exists(DOCKER_COMPOSE_PATH), "docker-compose.yml not found"

    with open(DOCKER_COMPOSE_PATH, "r") as f:
        compose = yaml.safe_load(f)

    assert "postgres" in compose["services"], "No 'postgres' service in docker-compose.yml"

    postgres = compose["services"]["postgres"]

    # Check image (pgvector/pgvector:pg16 is PostgreSQL 16 with pgvector extension)
    assert "image" in postgres, "No 'image' in postgres service"
    assert "pg16" in postgres["image"].lower(), (
        f"PostgreSQL image should be version 16, got: {postgres['image']}"
    )

    # Check environment variables
    assert "environment" in postgres, "No 'environment' in postgres service"
    env = postgres["environment"]
    assert "POSTGRES_USER" in env, "POSTGRES_USER not set"
    assert "POSTGRES_PASSWORD" in env, "POSTGRES_PASSWORD not set"
    assert "POSTGRES_DB" in env, "POSTGRES_DB not set"

    # Check volumes
    assert "volumes" in postgres, "No 'volumes' in postgres service"
    volumes = postgres["volumes"]
    assert any("init.sql" in str(v) for v in volumes), "init.sql not mounted to postgres service"


def test_pgvector_extension_in_init_sql():
    """Test that pgvector extension is in init.sql."""
    assert os.path.exists(INIT_SQL_PATH), f"init.sql not found at {INIT_SQL_PATH}"

    with open(INIT_SQL_PATH, "r") as f:
        content = f.read()

    assert "CREATE EXTENSION" in content.upper(), "No CREATE EXTENSION in init.sql"
    assert "vector" in content.lower() or "pgvector" in content.lower(), (
        "pgvector extension not mentioned in init.sql"
    )


def test_health_checks_configured():
    """Test that health checks are configured for postgres."""
    assert os.path.exists(DOCKER_COMPOSE_PATH), "docker-compose.yml not found"

    with open(DOCKER_COMPOSE_PATH, "r") as f:
        compose = yaml.safe_load(f)

    postgres = compose["services"]["postgres"]
    assert "healthcheck" in postgres, "No 'healthcheck' in postgres service"

    healthcheck = postgres["healthcheck"]
    assert "test" in healthcheck, "No 'test' in healthcheck"
    assert "interval" in healthcheck, "No 'interval' in healthcheck"
    assert "timeout" in healthcheck, "No 'timeout' in healthcheck"
    assert "retries" in healthcheck, "No 'retries' in healthcheck"

    # Check that test uses pg_isready
    test_cmd = healthcheck["test"]
    assert "pg_isready" in test_cmd or "pg_isready" in str(test_cmd), (
        "Health check should use pg_isready"
    )


def test_volumes_configured():
    """Test that volumes are configured."""
    assert os.path.exists(DOCKER_COMPOSE_PATH), "docker-compose.yml not found"

    with open(DOCKER_COMPOSE_PATH, "r") as f:
        compose = yaml.safe_load(f)

    assert "volumes" in compose, "No 'volumes' section in docker-compose.yml"
    assert len(compose["volumes"]) > 0, "No volumes defined"


def test_network_configured():
    """Test that network is configured."""
    assert os.path.exists(DOCKER_COMPOSE_PATH), "docker-compose.yml not found"

    with open(DOCKER_COMPOSE_PATH, "r") as f:
        compose = yaml.safe_load(f)

    assert "networks" in compose, "No 'networks' section in docker-compose.yml"
    assert len(compose["networks"]) > 0, "No networks defined"
