Before creating a pull request:

1. Run `git diff --name-only` to see which files changed
2. Detect if backend/ or frontend/ files were modified:
   - Backend: Files under `backend/` directory
   - Frontend: Files under `frontend/` directory
3. If backend files changed:
   - Use **backend-tester** agent to run `pytest`
   - Verify CI/CD pipeline will pass (check GitHub Actions workflow)
4. If frontend files changed:
   - Use **frontend-tester** agent to run `npm run test`
   - Verify CI/CD pipeline will pass (check GitHub Actions workflow)
5. Ensure all tests pass (linters already ran during commit)
6. Create comprehensive PR description including:
   - Summary of changes
   - Test results
   - CI/CD status
   - Checklist for testing
7. Create the pull request

**IMPORTANT**:
- Linters already ran during commit (pre-commit hook)
- Focus on tests and CI/CD checks
- Always verify tests pass before creating PR
