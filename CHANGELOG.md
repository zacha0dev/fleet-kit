# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: semantic.

Two things are versioned here: the **fleet** (the agents, skills, flows, hooks and tools in this repository) and the **sample application** the fleet works on. Each has its own `[Unreleased]` block.

## Fleet

### [Unreleased]

### [0.2.0] — 2026-09-26
#### Added
- `tools/hooks/guard.py`, the PreToolUse guard the README describes: denies force-push (DENY[0]), `reset --hard` (DENY[1]), test deselection (DENY[2]) and outbound sends (DENY[3]). Reads both Claude Code and GitHub Copilot hook input.
- `.github/hooks/guard.json`, the Copilot hook configuration that calls it.
- `tests/test_guard.py` and `tests/test_require_report.py`.
- `tools/runner.py`, the container entry point. It prints the plan for one run and exits 2, because the image has no agent CLI yet.
- Claude Code commands `/sweep`, `/triage` and `/reinforce` in `.claude/commands/`, and the Copilot prompt `.github/prompts/reinforce.prompt.md`.
- Validator checks: agent name matches filename, loaded skills exist, flow steps and handoffs resolve, `.claude/settings.json` hook scripts exist, each prompt has a matching command, README agent and skill counts match the tree.
- `.gitattributes`, `llms.txt`, `CITATION.cff`, `SECURITY.md`, `CONTRIBUTING.md`.
#### Changed
- Handoff order is `triager` → `test-writer` → `implementer` everywhere (agent, skill, eval case, report, board).
- `lead`, `quality-auditor`, `reporter` and `triager` have the `edit` tool, each bounded to the one file or folder it writes.
- The Stop hook uses the Claude Code contract: blocks once with a reason when no report is dated today, otherwise silent.
- `.claude/settings.json` calls `python "$CLAUDE_PROJECT_DIR"/tools/hooks/...`, so hooks run from any working directory on Windows and Linux.
- `.github/mcp.json`: GitHub server uses the read-only endpoint; `@playwright/mcp` pinned to 0.0.82 with a named tool list.
- `deploy/run-once.sh` runs from the repo root, names runs like `reports/`, and refuses to run with unset or `REPLACE_ME` values.
- The KI-1 demo tells the truth about the `xfail` marker: triage uses `--runxfail` to see the failure.
- The worked reinforcement example and the seed scorecard rows are labelled as illustrations.
#### Fixed
- CI failed on `main`: the validator required `.github/hooks/` files and `guard.py`, which were missing.
- `tools/validate_fleet.py` crashed on Windows paths; `tools/sync_claude.py --check` reported drift on Windows because of CRLF and the default code page.

### [0.1.0] — 2026-09-21
- `3be9cac` Reference layout: agents, skills, instructions, corpus, evals, sample app.
- `aa62079` Flows, the fourth part of the model.
- `3ae380f` The deploy template and the hosted-runners design.
- `1367a65` README rewritten around agents, skills, flows and the orchestrator.
- `d6a2100` The validator fails when the hook files are missing.

## Sample application

### [Unreleased]

### [0.1.0] — 2026-09-21
#### Added
- Pricing with flat and percent discounts.
- Inventory with reservations.

Known issue KI-1 (percent discounts applied as flat amounts) is open on purpose for the triage demo; see `fleet/corpus/known-issues.md`.
