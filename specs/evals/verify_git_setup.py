#!/usr/bin/env python3
"""
Verify Git & GitHub Setup (task-001)

This script verifies that all Git/GitHub setup requirements are met.
It follows the Definition of Done for task-001-git-github-setup.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


def run_command(cmd: List[str], check: bool = True) -> Tuple[bool, str, str]:
    """Run a shell command and return success, stdout, stderr."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        return (result.returncode == 0, result.stdout, result.stderr)
    except subprocess.CalledProcessError as e:
        return (False, e.stdout, e.stderr)


def check_git_initialized() -> Tuple[bool, str]:
    """Check if Git repository is initialized."""
    if not Path(".git").exists():
        return (False, "Git repository not initialized (.git directory missing)")

    success, stdout, stderr = run_command(["git", "status"])
    if not success:
        return (False, f"git status failed: {stderr}")

    return (True, "Git repository initialized successfully")


def check_github_remote() -> Tuple[bool, str]:
    """Check if GitHub remote is configured correctly."""
    success, stdout, stderr = run_command(["git", "remote", "-v"])
    if not success:
        return (False, f"git remote -v failed: {stderr}")

    if "github.com/arsen-ask-lx/telemetriya" not in stdout:
        return (False, "GitHub remote not found or incorrect URL")

    return (True, "GitHub remote configured correctly")


def check_gitignore_exists() -> Tuple[bool, str]:
    """Check if .gitignore exists and contains required exclusions."""
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        return (False, ".gitignore file missing")

    content = gitignore_path.read_text(encoding="utf-8")
    required_patterns = [
        "__pycache__",
        "*.pyc",
        ".env",
        ".venv",
        "node_modules",
        "*.db",
    ]

    missing = [p for p in required_patterns if p not in content]
    if missing:
        return (False, f".gitignore missing patterns: {', '.join(missing)}")

    return (True, ".gitignore contains all required exclusions")


def check_gitattributes_exists() -> Tuple[bool, str]:
    """Check if .gitattributes exists and configures line endings."""
    gitattributes_path = Path(".gitattributes")
    if not gitattributes_path.exists():
        return (False, ".gitattributes file missing")

    content = gitattributes_path.read_text(encoding="utf-8")

    # Check for line ending configuration
    if "text" not in content and "eol" not in content:
        return (False, ".gitattributes doesn't configure line endings")

    # Check for LFS configuration
    has_lfs = "lfs" in content.lower()

    return (True, f".gitattributes configured (LFS: {'yes' if has_lfs else 'no'})")


def check_readme_exists() -> Tuple[bool, str]:
    """Check if README.md exists and contains required sections."""
    readme_path = Path("README.md")
    if not readme_path.exists():
        return (False, "README.md file missing")

    content = readme_path.read_text(encoding="utf-8")

    required_sections = [
        "#",
        "Telemetriya",  # Project name should be mentioned
    ]

    missing = [s for s in required_sections if s not in content]
    if missing:
        return (False, f"README.md missing sections: {', '.join(missing)}")

    return (True, "README.md exists and contains project description")


def check_license_exists() -> Tuple[bool, str]:
    """Check if LICENSE file exists and uses MIT license."""
    license_path = Path("LICENSE")
    if not license_path.exists():
        return (False, "LICENSE file missing")

    content = license_path.read_text(encoding="utf-8")

    # Check for MIT license keywords
    if "MIT" not in content and "MIT License" not in content:
        return (False, "LICENSE doesn't appear to be MIT license")

    return (True, "LICENSE file exists (MIT)")


def check_contributing_exists() -> Tuple[bool, str]:
    """Check if CONTRIBUTING.md exists and contains required sections."""
    contributing_path = Path("CONTRIBUTING.md")
    if not contributing_path.exists():
        return (False, "CONTRIBUTING.md file missing")

    content = contributing_path.read_text(encoding="utf-8")

    required_sections = [
        "Conventional",
        "Commit",
        "TDD",
        "Code of Conduct",
    ]

    missing = [s for s in required_sections if s.lower() not in content.lower()]
    if missing:
        return (False, f"CONTRIBUTING.md missing sections: {', '.join(missing)}")

    return (True, "CONTRIBUTING.md exists and contains required sections")


def check_changelog_exists() -> Tuple[bool, str]:
    """Check if CHANGELOG.md exists and follows Keep a Changelog format."""
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        return (False, "CHANGELOG.md file missing")

    content = changelog_path.read_text(encoding="utf-8")

    # Check for Keep a Changelog format indicators
    required_patterns = [
        "#",  # Title
        "## [",  # Version format
    ]

    missing = [p for p in required_patterns if p not in content]
    if missing:
        return (
            False,
            f"CHANGELOG.md doesn't follow Keep a Changelog format: missing {', '.join(missing)}",
        )

    return (True, "CHANGELOG.md exists and follows Keep a Changelog format")


def check_first_commit() -> Tuple[bool, str]:
    """Check if at least one commit exists."""
    success, stdout, stderr = run_command(["git", "log", "--oneline"])
    if not success:
        return (False, f"git log failed: {stderr}")

    if not stdout.strip():
        return (False, "No commits found")

    commit_count = len(stdout.strip().split("\n"))
    return (True, f"Found {commit_count} commit(s)")


def check_main_branch() -> Tuple[bool, str]:
    """Check if main branch exists and is the current branch."""
    success, stdout, stderr = run_command(["git", "branch", "--show-current"])
    if not success:
        return (False, f"git branch --show-current failed: {stderr}")

    current_branch = stdout.strip()
    if current_branch != "main":
        return (False, f"Current branch is '{current_branch}', expected 'main'")

    return (True, "Main branch is the current branch")


def run_all_checks() -> List[Tuple[str, bool, str]]:
    """Run all verification checks and return results."""
    checks = [
        ("Git initialized", check_git_initialized),
        ("GitHub remote", check_github_remote),
        (".gitignore exists", check_gitignore_exists),
        (".gitattributes exists", check_gitattributes_exists),
        ("README.md exists", check_readme_exists),
        ("LICENSE exists", check_license_exists),
        ("CONTRIBUTING.md exists", check_contributing_exists),
        ("CHANGELOG.md exists", check_changelog_exists),
        ("First commit", check_first_commit),
        ("Main branch", check_main_branch),
    ]

    results = []
    for name, check_func in checks:
        try:
            success, message = check_func()
            results.append((name, success, message))
        except Exception as e:
            results.append((name, False, f"Error: {e}"))

    return results


def main():
    """Main verification function."""
    print("=" * 70)
    print("Git & GitHub Setup Verification (task-001)")
    print("=" * 70)
    print()

    results = run_all_checks()

    # Print results
    passed = 0
    failed = 0

    for name, success, message in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status}: {name}")
        if not success or message:
            print(f"    {message}")
        print()

        if success:
            passed += 1
        else:
            failed += 1

    # Summary
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(results)} checks")
    print("=" * 70)

    if failed > 0:
        print("\n[X] Setup verification FAILED. Some requirements are not met.")
        return 1
    else:
        print("\n[OK] Setup verification PASSED. All requirements are met!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
