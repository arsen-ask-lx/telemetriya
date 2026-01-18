"""Tests for Docker management scripts."""

import os

import pytest

SCRIPTS_DIR = "scripts"


def test_docker_up_script_exists():
    """Test that docker-up.sh script exists."""
    script_path = os.path.join(SCRIPTS_DIR, "docker-up.sh")
    assert os.path.exists(script_path), f"docker-up.sh not found at {script_path}"


def test_docker_down_script_exists():
    """Test that docker-down.sh script exists."""
    script_path = os.path.join(SCRIPTS_DIR, "docker-down.sh")
    assert os.path.exists(script_path), f"docker-down.sh not found at {script_path}"


def test_docker_logs_script_exists():
    """Test that docker-logs.sh script exists."""
    script_path = os.path.join(SCRIPTS_DIR, "docker-logs.sh")
    assert os.path.exists(script_path), f"docker-logs.sh not found at {script_path}"


def test_docker_exec_script_exists():
    """Test that docker-exec.sh script exists."""
    script_path = os.path.join(SCRIPTS_DIR, "docker-exec.sh")
    assert os.path.exists(script_path), f"docker-exec.sh not found at {script_path}"


def test_docker_up_script_executable():
    """Test that docker-up.sh is executable (on Unix)."""
    if os.name == "posix":  # Linux/Mac
        script_path = os.path.join(SCRIPTS_DIR, "docker-up.sh")
        assert os.access(script_path, os.X_OK), "docker-up.sh is not executable"
    else:
        pytest.skip("Test only applicable on Unix systems")


def test_docker_down_script_executable():
    """Test that docker-down.sh is executable (on Unix)."""
    if os.name == "posix":  # Linux/Mac
        script_path = os.path.join(SCRIPTS_DIR, "docker-down.sh")
        assert os.access(script_path, os.X_OK), "docker-down.sh is not executable"
    else:
        pytest.skip("Test only applicable on Unix systems")
