#!/usr/bin/env python3
"""Structural evals for the fleet itself. Exit 1 on any failure.

Every agent: valid frontmatter, description, tools list, a Bounds section.
Every skill: frontmatter name matches folder, description, a Steps or Rules section.
Every hook file: valid JSON with version 1. Every instruction: applyTo present.
"""
import glob, json, os, re, sys

fails = []
def check(cond, msg):
    if not cond: fails.append(msg)

for p in glob.glob(".github/agents/*.agent.md"):
    t = open(p).read(); m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    check(m, f"{p}: no frontmatter"); 
    if not m: continue
    fm, body = m.groups()
    check(re.search(r"^description:\s*\S", fm, re.M), f"{p}: missing description")
    check(re.search(r"^tools:\s*\[", fm, re.M), f"{p}: missing tools allowlist")
    check("## Bounds" in body or "## Rules" in body, f"{p}: no Bounds section")
    check(len(body) < 30000, f"{p}: body over 30k chars")

for p in glob.glob(".claude/skills/*/SKILL.md"):
    t = open(p).read(); m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    check(m, f"{p}: no frontmatter")
    if not m: continue
    fm, body = m.groups(); folder = p.split("/")[2]
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    check(name and name.group(1).strip() == folder, f"{p}: name != folder")
    check(re.search(r"^description:\s*\S", fm, re.M), f"{p}: missing description")
    check("## Steps" in body or "## Rules" in body or "## When" in body, f"{p}: no Steps/Rules section")
    check(len(body.splitlines()) <= 150, f"{p}: over 150 lines — split it")

hook_files = glob.glob(".github/hooks/*.json")
check(hook_files, ".github/hooks/: no hook files — the guardrails the README promises are not here")
for p in hook_files:
    try:
        d = json.load(open(p)); check(d.get("version") == 1 and isinstance(d.get("hooks"), dict), f"{p}: bad shape")
    except Exception as e: check(False, f"{p}: {e}")

# A hook that points at a script which does not exist is worse than no hook:
# it reads as enforcement and enforces nothing.
for p in hook_files:
    try: d = json.load(open(p))
    except Exception: continue
    for event, entries in (d.get("hooks") or {}).items():
        for e in entries if isinstance(entries, list) else []:
            for field in ("bash", "powershell", "command"):
                cmd = e.get(field) or ""
                for token in cmd.split():
                    if token.endswith(".py"):
                        check(os.path.exists(token), f"{p}: {event} points at {token}, which does not exist")

for p in glob.glob(".github/instructions/*.instructions.md"):
    check(re.search(r"^applyTo:", open(p).read(), re.M), f"{p}: missing applyTo")

agents = len(glob.glob(".github/agents/*.agent.md")); skills = len(glob.glob(".claude/skills/*/SKILL.md"))
if fails:
    print("\n".join(fails)); print(f"FAIL — {len(fails)} problem(s)"); sys.exit(1)
print(f"ok — {agents} agents, {skills} skills, hooks and instructions valid")
