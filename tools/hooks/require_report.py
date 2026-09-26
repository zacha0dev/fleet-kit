#!/usr/bin/env python3
"""Claude Code Stop hook: keep the session open once if no session report was written today.

Neither runtime passes the transcript in a stable way, so this checks the one durable artifact:
a file in reports/ whose name contains today's date (reports/README.md sets the naming,
YYYY-MM-DD-<agent>-<slug>.md).

Contract (Claude Code Stop hook):
  - a report exists            -> exit 0, no output; the session stops normally
  - no report                  -> print {"decision": "block", "reason": "..."}; Claude continues and
                                  is told to write the report
  - stop_hook_active is true   -> exit 0; the hook already blocked once, so it does not loop
"""
import datetime
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or pathlib.Path(__file__).resolve().parents[2])


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        payload = {}
    if isinstance(payload, dict) and payload.get("stop_hook_active"):
        return 0
    today = datetime.date.today().isoformat()
    if any(today in p.name for p in (ROOT / "reports").glob("*.md")):
        return 0
    print(json.dumps({
        "decision": "block",
        "reason": f"No session report in reports/ dated {today}. Write one in the fixed shape "
                  "(.claude/skills/session-report/SKILL.md) as reports/YYYY-MM-DD-<agent>-<slug>.md, then stop.",
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
