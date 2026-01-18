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
