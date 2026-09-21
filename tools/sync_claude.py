#!/usr/bin/env python3
"""Mirror .github/agents/*.agent.md (canonical) into .claude/agents/*.md (Claude Code subagents).

Copilot CLI reads both directories and dedupes by name, so the mirror is harmless there;
Claude Code reads only .claude/agents/. One source, one generated copy, checked in CI.
"""
import glob, os, re, sys

TOOL_MAP = {"read": "Read", "search": "Grep, Glob", "edit": "Edit, Write", "execute": "Bash", "agent": "Task", "web": "WebFetch, WebSearch"}

def convert(text):
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    fm, body = m.group(1), m.group(2)
    name = re.search(r"^name:\s*(.+)$", fm, re.M).group(1).strip()
    desc = re.search(r"^description:\s*(.+)$", fm, re.M).group(1).strip()
    tools = re.search(r"^tools:\s*(\[.*\])$", fm, re.M)
    claude_tools = ""
    if tools:
        names = re.findall(r'"([^"]+)"', tools.group(1))
        claude_tools = ", ".join(dict.fromkeys(t for n in names for t in TOOL_MAP.get(n, n).split(", ")))
    out = f"---\nname: {name}\ndescription: {desc}\n"
    if claude_tools: out += f"tools: {claude_tools}\n"
    out += "---\n<!-- generated from .github/agents/" + name + ".agent.md by tools/sync_claude.py — do not edit -->\n" + body
    return name, out

def main():
    check = "--check" in sys.argv
    os.makedirs(".claude/agents", exist_ok=True)
    drift = []
    for src in sorted(glob.glob(".github/agents/*.agent.md")):
        name, out = convert(open(src).read())
        dst = f".claude/agents/{name}.md"
        cur = open(dst).read() if os.path.exists(dst) else None
        if cur != out:
            if check: drift.append(dst)
            else: open(dst, "w").write(out)
    if check and drift:
        print("mirror out of date:", *drift, sep="\n  "); sys.exit(1)
    print("ok" if check else f"synced {len(glob.glob('.github/agents/*.agent.md'))} agents")

if __name__ == "__main__":
    main()
