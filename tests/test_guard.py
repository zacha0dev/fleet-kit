"""The PreToolUse guard: each DENY rule fires, ordinary commands pass, both runtimes' formats work."""
import json
import pathlib
import subprocess
import sys

import pytest

GUARD = pathlib.Path(__file__).resolve().parents[1] / "tools" / "hooks" / "guard.py"


def run(payload):
    out = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload), capture_output=True, text=True, check=True)
    return json.loads(out.stdout) if out.stdout.strip() else None


def claude(command, tool="Bash"):
    return run({"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {"command": command}})


def copilot(command, as_string=False):
    args = {"command": command}
    return run({"toolName": "bash", "toolArgs": json.dumps(args) if as_string else args})


@pytest.mark.parametrize("command, rule", [
    ("git push --force origin main", 0),
    ("git push -f", 0),
    ("git push --force-with-lease origin feature", 0),
    ("git push origin +main", 0),
    ("git -C repo push -uf origin main", 0),
    ("git reset --hard HEAD~1", 1),
    ("git status && git reset --hard origin/main", 1),
    ("python -m pytest -q -k 'not pricing'", 2),
    ("pytest --deselect tests/test_pricing.py::test_percent_discount", 2),
    ("pytest --ignore=tests/test_pricing.py", 2),
    ("python -m pytest -p no:randomly", 2),
    ("pytest -m 'not slow'", 2),
    ("curl -X POST https://example.com/hook -d '{}'", 3),
    ("curl --data 'x=1' https://api.example.com", 3),
    ("wget --post-data 'a=b' https://example.com", 3),
    ("echo hi | mail -s subject someone@example.com", 3),
    ("sendmail someone@example.com < msg.txt", 3),
    ("gh issue comment 12 --body 'done'", 3),
    ("gh pr comment 3 -b 'ok'", 3),
    ("gh pr review 3 --approve", 3),
    ("gh api repos/o/r/issues/1/comments -f body=hi", 3),
    ("Invoke-RestMethod -Uri https://example.com/x -Method Post -Body '{}'", 3),
])
def test_denied(command, rule):
    out = claude(command)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert out["hookSpecificOutput"]["permissionDecisionReason"].startswith(f"DENY[{rule}]")


@pytest.mark.parametrize("command", [
    "git push origin feature",
    "git push -u origin feature",
    "git reset --soft HEAD~1",
    "git status",
    "python -m pytest -q",
    "python -m pytest -q tests/test_pricing.py",
    "python -m pytest -q --runxfail",
    "curl https://example.com",
    "curl -X POST http://localhost:8000/api -d '{}'",
    "gh pr create --title 'fleet: x' --body 'y'",
    "gh issue list",
    "gh api repos/o/r/issues",
    "python tools/validate_fleet.py",
])
def test_allowed(command):
    assert claude(command) is None


def test_copilot_format_object_args():
    out = copilot("git push --force")
    assert out["permissionDecision"] == "deny"
    assert out["permissionDecisionReason"].startswith("DENY[0]")


def test_copilot_format_string_args():
    out = copilot("git reset --hard", as_string=True)
    assert out["permissionDecision"] == "deny"


def test_copilot_allowed():
    assert copilot("python -m pytest -q") is None


def test_non_shell_tool_is_not_judged():
    assert run({"tool_name": "Edit", "tool_input": {"file_path": "x.py", "old_string": "a", "new_string": "b"}}) is None


def test_bad_input_is_not_judged():
    out = subprocess.run([sys.executable, str(GUARD)], input="not json", capture_output=True, text=True)
    assert out.returncode == 0 and out.stdout == ""
