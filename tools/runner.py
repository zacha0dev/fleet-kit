#!/usr/bin/env python3
"""Container entry point for deploy/Dockerfile. It prints the plan for one agent run; it does not run an agent.

    python -m tools.runner --agent triager

What it does:
  1. Checks the agent is on the roster in deploy/agents.json.
  2. Reads .github/agents/<agent>.agent.md and prints the run plan: tools, skills, task, caller, run id.
  3. Exits 2 with a message naming what is missing, because no agent CLI is installed in this image.

This is deliberate. The image carries the fleet's definitions, not a model runtime. To make it run
agents, install the CLI you use (Claude Code or GitHub Copilot CLI) in the Dockerfile and replace
step 3 with a call to it. Until then this exits non-zero so nothing reads as a finished run.
"""
import argparse
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def plan(agent):
    roster = {a["name"] for a in json.loads((ROOT / "deploy" / "agents.json").read_text(encoding="utf-8"))["agents"]}
    if agent not in roster:
        sys.exit(f"refusing to run: {agent!r} is not in deploy/agents.json")
    text = (ROOT / ".github" / "agents" / f"{agent}.agent.md").read_text(encoding="utf-8")
    tools = re.findall(r'"([^"]+)"', (re.search(r"^tools:\s*(\[.*\])", text, re.M) or [None, ""])[1])
    skills = re.findall(r"(?:[Ll]oad|[Ii]nvoke)(?: the)? `([a-z0-9-]+)`", text)
    return {
        "agent": agent,
        "definition": f".github/agents/{agent}.agent.md",
        "tools": tools,
        "skills": skills,
        "task": os.environ.get("FLEET_TASK", ""),
        "caller": os.environ.get("FLEET_CALLER_ID", ""),
        "run_id": os.environ.get("FLEET_RUN_ID", ""),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--agent", required=True)
    args = ap.parse_args(argv)
    print(json.dumps(plan(args.agent), indent=2))
    print("not run: no agent CLI is installed in this image. Install Claude Code or GitHub Copilot CLI "
          "and replace this step in tools/runner.py.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
