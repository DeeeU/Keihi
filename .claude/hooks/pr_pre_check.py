#!/usr/bin/env python3
import json
import sys
import subprocess
from pathlib import Path

try:
    input_data = json.load(sys.stdin)
except:
    sys.exit(0)

prompt = input_data.get("prompt", "").lower()

# PR関連キーワード検出
pr_keywords = ["pr", "pull request", "プルリクエスト", "プル リクエスト"]
if not any(kw in prompt for kw in pr_keywords):
    sys.exit(0)

# git diff 実行
try:
    result = subprocess.run(
        ["git", "diff", "--name-only"], capture_output=True, text=True, timeout=5
    )
    files = result.stdout.strip().split("\n") if result.stdout else []
except:
    sys.exit(0)

# ファイル変更検出
backend_changed = any(f.startswith("backend/") for f in files if f)
frontend_changed = any(f.startswith("frontend/") for f in files if f)

if not (backend_changed or frontend_changed):
    sys.exit(0)

# コンテキスト追加
context = "\n## Pre-PR Checks Required\n"
if backend_changed:
    context += "- **Backend files changed**: Use backend-tester agent to run pytest\n"
if frontend_changed:
    context += "- **Frontend files changed**: Use frontend-tester agent to run vitest\n"
context += "\nEnsure all tests pass and CI/CD pipeline will succeed before creating the PR.\n"
context += "\n💡 Tip: Linters already ran during commit, focus on tests and CI/CD checks.\n"

# JSON形式で追加コンテキストを返す
output = {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": context}}

print(json.dumps(output))
sys.exit(0)
