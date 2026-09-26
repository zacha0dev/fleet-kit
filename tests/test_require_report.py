"""The Stop hook blocks once when no report is dated today, and is silent otherwise."""
import datetime
import json
import os
import pathlib
import subprocess
import sys

HOOK = pathlib.Path(__file__).resolve().parents[1] / "tools" / "hooks" / "require_report.py"


def run(project, payload):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
    out = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, env=env, check=True)
    return out.stdout.strip()


def test_blocks_without_a_report(tmp_path):
    (tmp_path / "reports").mkdir()
    out = json.loads(run(tmp_path, {"hook_event_name": "Stop"}))
    assert out["decision"] == "block" and "reports/" in out["reason"]


def test_silent_with_a_report(tmp_path):
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / f"{datetime.date.today().isoformat()}-triager-x.md").write_text("r")
    assert run(tmp_path, {"hook_event_name": "Stop"}) == ""


def test_does_not_loop(tmp_path):
    (tmp_path / "reports").mkdir()
    assert run(tmp_path, {"hook_event_name": "Stop", "stop_hook_active": True}) == ""
