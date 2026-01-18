# Lessons Learned (what went wrong/right)

## 2026-01-18 (Task-001: Git & GitHub Setup)
**What went well:**
- TDD approach applied successfully (RED → GREEN → REFINEMENT)
- Created verification script `verify_git_setup.py` for all DoD checks
- All checks passed (10/10, 100%)
- Documentation quality: well-structured README, LICENSE, CONTRIBUTING, CHANGELOG

**What could be improved:**
- Verification scripts should be included in task allowlist (currently not specified)
- Builder agent tried to start task-002 before task-001 was fully reviewed → added constraint: one task per session

**Lessons:**
- Always create verification scripts before implementation (TDD approach)
- Add verification scripts to task allowlist explicitly
- Update agent constraints to prevent task jumping
- Git line ending issues on Windows: solved with .gitattributes (LF normalization)

## 2026-01-18 (Task-002: Virtual Environment Setup)
**What went well:**
- Python 3.12.10 successfully found and used for venv
- All dependencies installed correctly (production + dev)
- Tool configs created properly (ruff, pytest, mypy, coverage in pyproject.toml)
- Issue caught by reviewer and fixed promptly

**What went wrong:**
- Initial venv created with Python 3.10.11 instead of 3.11+ (DoD requirement)
- Builder didn't check Python version before creating venv → first review returned CHANGES_REQUESTED
- pyproject.toml initially configured for py311, had to update to py312 after venv recreation

**What could be improved:**
- Builder should verify Python version explicitly before creating venv (Step 1 of task plan)
- Add Python version check to verification commands in task DoD

**Lessons:**
- Always verify Python version matches DoD requirements before creating venv
- Sync pyproject.toml python_version with actual venv Python version
- Document fixes properly in commit messages (e.g., "fix: recreate venv with Python 3.12.10 (DoD requires 3.11+)")

## 2026-01-18 (Task-003: Project Structure Setup)
**What went well:**
- Full project structure created correctly (37 directories)
- All 26 __init__.py files created
- All 9 .gitkeep files created and committed
- .env.example template created with all required sections
- Python imports verified working

**What went wrong:**
- Initial commit (d4351aa) failed review because .gitkeep files were not tracked by git
- Issue: .gitignore rules `secrets/` and `temp/` blocked files even with exceptions `!infra/secrets/.gitkeep` and `!storage/temp/.gitkeep`
- Builder didn't verify that .gitkeep files were actually in git commit

**What was fixed:**
- Removed broad rule `secrets/` (was blocking infra/secrets/.gitkeep)
- Changed `temp/` to `/temp` (only root temp directory)
- Changed `storage/` to `storage/*` with proper exceptions
- Added exceptions: `!storage/pdf/`, `!storage/voice/`, `!storage/temp/`
- Added `!storage/temp/.gitkeep` before `/temp` rule (order matters in .gitignore)
- Re-added all .gitkeep files to git and amended commit (d4351aa → 21c9d46)

**What could be improved:**
- Builder should verify that .gitkeep files are actually tracked by git before committing
- Add explicit check: `git check-ignore <file>` to verify exclusions work
- Add verification of git commit contents: `git show --name-only HEAD | grep gitkeep`

**Lessons:**
- Order matters in .gitignore: exclusions (!) should come before broader rules that block them
- Broad directory rules like `secrets/` block subdirectories even with exclusions
- Use `/*` for directory contents while allowing specific files via exclusions
- Always verify .gitkeep files are tracked: `git ls-tree -r HEAD | grep gitkeep`
- Amended commits change hash - important to know if not yet pushed
- Use `git check-ignore -v <file>` to debug .gitignore issues

## 2026-01-18 (Task-004: Configuration Management)
**What went well:**
- Pydantic Settings v2 implementation successful with all config fields
- @lru_cache for singleton get_settings() implemented correctly
- All environment variables supported via validation_alias
- 10 unit tests created, initial coverage 100%
- mypy passed without errors
- Reviewer feedback addressed promptly

**What went wrong:**
- Initial implementation didn't include SECRET_KEY validation (identified as risk in task.md)
- Tests were not isolated from local .env file → reviewer CHANGES_REQUESTED
  - Pydantic Settings loads .env automatically even when using patch.dict(os.environ, ..., clear=True)
  - Tests would fail if .env existed locally with different values
- Initial review returned CHANGES_REQUESTED with 2 critical findings
  - Required fix: isolate_from_env_file fixture
  - Required fix: SECRET_KEY validation (min 16 chars)
  - Required fix: update all SECRET_KEY values in tests to be >=16 chars

**What was fixed:**
- Added `@field_validator("secret_key")` to validate minimum length (16 chars)
- Added `isolate_from_env_file()` fixture with autouse=True:
  - Temporarily renames .env → .env.backup before tests
  - Restores .env.backup → .env after tests (in finally block)
- Added `test_settings_secret_key_min_length` test
- Updated all SECRET_KEY values in tests to be >=16 chars
- Fixed fixture error (removed duplicate yield in isolate_from_env_file)
- Updated .env.example with SECRET_KEY min length comment

**What could be improved:**
- Builder should anticipate that Pydantic Settings loads .env file automatically
- Test isolation fixtures should be added proactively for any environment-dependent code
- Validation for critical fields (SECRET_KEY, tokens) should be implemented in initial implementation, not as a follow-up

**Lessons:**
- Pydantic Settings loads .env file automatically via model_config, even with os.environ patching
- For test isolation from .env: temporarily rename .env or use _env_file=None parameter
- Validation of security-critical fields (SECRET_KEY, API tokens) should be implemented from the start
- Test fixtures for environment isolation are essential for deterministic test results
- Review cycle: initial implementation → CHANGES_REQUESTED → fixes → APPROVED is normal workflow
