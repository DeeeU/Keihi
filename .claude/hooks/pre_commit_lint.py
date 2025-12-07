#!/usr/bin/env python3
"""
Pre-commit hook: Run linters before git commit
"""

import json
import sys
import subprocess

try:
    input_data = json.load(sys.stdin)
except:
    # Allow if no input
    sys.exit(0)

# Check if this is a git commit command
tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

if tool_name != "Bash":
    sys.exit(0)

command = tool_input.get("command", "")

# Check if it's a git commit command
if not ("git commit" in command or "git add" in command and "git commit" in command):
    sys.exit(0)

print("\n🔍 Running pre-commit linters...\n", file=sys.stderr)

# Get list of staged/modified files
try:
    # Check both staged and unstaged files
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"], capture_output=True, text=True, timeout=5
    )

    # Also check staged files
    staged_result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, timeout=5
    )

    all_files = set()
    if result.stdout:
        all_files.update(result.stdout.strip().split("\n"))
    if staged_result.stdout:
        all_files.update(staged_result.stdout.strip().split("\n"))

    files = [f for f in all_files if f]
except:
    # If git commands fail, allow the commit
    sys.exit(0)

# Check if backend or frontend files are modified
backend_changed = any(f.startswith("backend/") for f in files)
frontend_changed = any(f.startswith("frontend/") for f in files)

if not (backend_changed or frontend_changed):
    # No relevant files changed
    sys.exit(0)

errors = []

# Run backend linter if needed
if backend_changed:
    print("📦 Backend files changed - Running Ruff...\n", file=sys.stderr)

    try:
        # Ruff check
        check_result = subprocess.run(
            ["ruff", "check", "backend/"], capture_output=True, text=True, timeout=30
        )

        if check_result.returncode != 0:
            errors.append(f"❌ Ruff check failed:\n{check_result.stdout}")
        else:
            print("✅ Ruff check passed\n", file=sys.stderr)

        # Ruff format (auto-fix)
        format_result = subprocess.run(
            ["ruff", "format", "backend/"], capture_output=True, text=True, timeout=30
        )

        if format_result.returncode == 0:
            print("✅ Ruff format completed\n", file=sys.stderr)

    except subprocess.TimeoutExpired:
        errors.append("❌ Backend linting timed out")
    except FileNotFoundError:
        errors.append("❌ Ruff not found. Install with: pip install ruff")

# Run frontend linter if needed
if frontend_changed:
    print("🎨 Frontend files changed - Running ESLint and Prettier...\n", file=sys.stderr)

    try:
        # Type check
        type_result = subprocess.run(
            ["npm", "run", "type-check"], cwd="frontend", capture_output=True, text=True, timeout=60
        )

        if type_result.returncode != 0:
            errors.append(
                f"❌ TypeScript type check failed:\n{type_result.stdout}\n{type_result.stderr}"
            )
        else:
            print("✅ Type check passed\n", file=sys.stderr)

        # ESLint
        lint_result = subprocess.run(
            ["npm", "run", "lint"], cwd="frontend", capture_output=True, text=True, timeout=60
        )

        if lint_result.returncode != 0:
            errors.append(f"❌ ESLint failed:\n{lint_result.stdout}\n{lint_result.stderr}")
        else:
            print("✅ ESLint passed\n", file=sys.stderr)

        # Prettier (auto-fix)
        format_result = subprocess.run(
            ["npm", "run", "format"], cwd="frontend", capture_output=True, text=True, timeout=60
        )

        if format_result.returncode == 0:
            print("✅ Prettier format completed\n", file=sys.stderr)

    except subprocess.TimeoutExpired:
        errors.append("❌ Frontend linting timed out")
    except FileNotFoundError:
        errors.append("❌ npm not found")

# If there are errors, block the commit
if errors:
    print("\n⛔ Pre-commit checks failed:\n", file=sys.stderr)
    for error in errors:
        print(error, file=sys.stderr)
    print("\nPlease fix the linting errors before committing.\n", file=sys.stderr)

    output = {
        "decision": "block",
        "message": "Linting errors detected. Please fix before committing.\n\n" + "\n".join(errors),
    }
    print(json.dumps(output))
    sys.exit(0)

print("✅ All pre-commit linting checks passed!\n", file=sys.stderr)

# Allow the commit
output = {"decision": "approve"}
print(json.dumps(output))
sys.exit(0)
