#!/usr/bin/env python3
"""Structural evals for the fleet itself. Exit 1 on any failure.

Every agent: valid frontmatter, name matches its filename, description, tools allowlist, a Bounds
section, and every skill it loads exists.
Every skill: frontmatter name matches folder, description, a Steps or Rules section, under 150 lines.
Every flow: frontmatter, each step's agent and skill exist, the handoff target exists (or is "none").
Every hook file (Copilot .github/hooks/*.json and Claude Code .claude/settings.json): valid JSON,
and every script it calls exists.
Every instruction: applyTo present. Every Copilot prompt has a Claude Code command of the same name.
README counts of agents and skills match the tree.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FRONTMATTER = re.compile(r"---\n(.*?)\n---\n(.*)", re.S)
NUMBERS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
    "sixteen seventeen eighteen nineteen twenty".split())}

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


def read(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rel(p):
    return p.relative_to(ROOT).as_posix()


def script_paths(command):
    """The .py files a hook command runs, with $CLAUDE_PROJECT_DIR resolved to the repo root."""
    for token in command.split():
        token = token.strip("\"'").replace('"', "").replace("$CLAUDE_PROJECT_DIR", ".").replace("${CLAUDE_PROJECT_DIR}", ".")
        if token.endswith(".py"):
            yield token


agent_files = sorted((ROOT / ".github" / "agents").glob("*.agent.md"))
skill_files = sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md"))
agent_names = {p.name.removesuffix(".agent.md") for p in agent_files}
skill_names = {p.parent.name for p in skill_files}

for p in agent_files:
    m = FRONTMATTER.match(read(p))
    check(m, f"{rel(p)}: no frontmatter")
    if not m:
        continue
    fm, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    check(name and name.group(1).strip() == p.name.removesuffix(".agent.md"), f"{rel(p)}: name does not match filename")
    check(re.search(r"^description:\s*\S", fm, re.M), f"{rel(p)}: missing description")
    check(re.search(r"^tools:\s*\[", fm, re.M), f"{rel(p)}: missing tools allowlist")
    check("## Bounds" in body or "## Rules" in body, f"{rel(p)}: no Bounds section")
    check(len(body) < 30000, f"{rel(p)}: body over 30k chars")
    for s in re.findall(r"(?:[Ll]oad|[Ii]nvoke)(?: the)? `([a-z0-9-]+)`", body):
        check(s in skill_names, f"{rel(p)}: loads skill `{s}`, which does not exist")

for p in skill_files:
    m = FRONTMATTER.match(read(p))
    check(m, f"{rel(p)}: no frontmatter")
    if not m:
        continue
    fm, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    check(name and name.group(1).strip() == p.parent.name, f"{rel(p)}: name != folder")
    check(re.search(r"^description:\s*\S", fm, re.M), f"{rel(p)}: missing description")
    check("## Steps" in body or "## Rules" in body or "## When" in body, f"{rel(p)}: no Steps/Rules section")
    check(len(body.splitlines()) <= 150, f"{rel(p)}: over 150 lines - split it")

for p in sorted((ROOT / "flows").glob("*.md")):
    if p.name == "README.md":
        continue
    m = FRONTMATTER.match(read(p))
    check(m, f"{rel(p)}: no frontmatter")
    if not m:
        continue
    fm, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    check(name and name.group(1).strip() == p.stem, f"{rel(p)}: name does not match filename")
    handoff = re.search(r"^handoff:\s*(.+)$", fm, re.M)
    check(handoff, f"{rel(p)}: missing handoff (write 'none' for a leaf)")
    if handoff and not handoff.group(1).strip().startswith("none"):
        check((ROOT / handoff.group(1).strip()).exists(), f"{rel(p)}: handoff {handoff.group(1).strip()} does not exist")
    for step in re.findall(r"^\d+\. \*\*.*$", body, re.M):
        m2 = re.search(r"— `([a-z0-9-]+)`(?: · `([a-z0-9-]+)`)?", step)
        check(m2, f"{rel(p)}: step names no agent: {step[:60]}")
        if m2:
            check(m2.group(1) in agent_names, f"{rel(p)}: agent `{m2.group(1)}` does not exist")
            if m2.group(2):
                check(m2.group(2) in skill_names, f"{rel(p)}: skill `{m2.group(2)}` does not exist")

hook_files = sorted((ROOT / ".github" / "hooks").glob("*.json"))
check(hook_files, ".github/hooks/: no hook files - the guardrails the README promises are not here")
for p in hook_files:
    try:
        d = json.loads(read(p))
    except ValueError as e:
        check(False, f"{rel(p)}: {e}")
        continue
    check(d.get("version") == 1 and isinstance(d.get("hooks"), dict), f"{rel(p)}: bad shape")
    # A hook that points at a script which does not exist is worse than no hook:
    # it reads as enforcement and enforces nothing.
    for event, entries in (d.get("hooks") or {}).items():
        for e in entries if isinstance(entries, list) else []:
            for field in ("bash", "powershell", "command"):
                for script in script_paths(e.get(field) or ""):
                    check((ROOT / script).exists(), f"{rel(p)}: {event} points at {script}, which does not exist")

settings = ROOT / ".claude" / "settings.json"
check(settings.exists(), ".claude/settings.json: missing - Claude Code would run without the guard")
if settings.exists():
    try:
        d = json.loads(read(settings))
        commands = [h.get("command", "") for entries in (d.get("hooks") or {}).values()
                    for e in entries for h in e.get("hooks", [])]
        check(any("guard.py" in c for c in commands), ".claude/settings.json: no hook calls guard.py")
        for c in commands:
            for script in script_paths(c):
                check((ROOT / script).exists(), f".claude/settings.json: hook points at {script}, which does not exist")
    except (ValueError, AttributeError, TypeError) as e:
        check(False, f".claude/settings.json: {e}")

for p in sorted((ROOT / ".github" / "instructions").glob("*.instructions.md")):
    check(re.search(r"^applyTo:", read(p), re.M), f"{rel(p)}: missing applyTo")

for p in sorted((ROOT / ".github" / "prompts").glob("*.prompt.md")):
    m = FRONTMATTER.match(read(p))
    agent = m and re.search(r"^agent:\s*(.+)$", m.group(1), re.M)
    check(agent and agent.group(1).strip() in agent_names, f"{rel(p)}: agent missing or unknown")
    cmd = ROOT / ".claude" / "commands" / (p.name.removesuffix(".prompt.md") + ".md")
    check(cmd.exists(), f"{rel(p)}: no matching Claude Code command at {rel(cmd) if cmd.is_relative_to(ROOT) else cmd}")

counts = {"agents": len(agent_files), "skills": len(skill_files)}
for doc in (ROOT / "README.md", ROOT / "fleet" / "README.md"):
    if not doc.exists():
        continue
    for num, kind in re.findall(r"\b(\d+|[A-Za-z]+) (agents|skills)\b", read(doc)):
        n = int(num) if num.isdigit() else NUMBERS.get(num.lower())
        if n is not None and n > 1:
            check(n == counts[kind], f"{rel(doc)}: says {num} {kind}, the tree has {counts[kind]}")

if fails:
    print("\n".join(fails))
    print(f"FAIL - {len(fails)} problem(s)")
    sys.exit(1)
print(f"ok - {counts['agents']} agents, {counts['skills']} skills, "
      f"{len(list((ROOT / 'flows').glob('*.md'))) - 1} flows, hooks, prompts and instructions valid")
