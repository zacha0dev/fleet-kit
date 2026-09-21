# fleet-kit — working instructions

This repository is a small agent fleet and the sample application it works on. Read this file, then `AGENTS.md`, then `fleet/README.md`.

## How work moves
- Any request without a named agent goes to `lead`, who routes it.
- Every session ends with a session report (`.claude/skills/session-report/SKILL.md`). No report, no session.
- Tests are written before code (`write-tests-first`). A fix without a preceding failing test is incomplete.
- Changes to the fleet itself (agents, skills, instructions, hooks) ship only as pull requests titled `reinforce: …` or `fleet: …`.

## Bounds that hold everywhere
- **Drafts only.** Anything addressed to a person outside this repository — an issue comment on another project, an email, a message — is written to `drafts/` for a human to send. Reading messages is never restricted by this rule.
- **Human gates.** Merging, tagging, releasing, and publishing are done by a human. Agents prepare the exact commands.
- **Measure before claiming.** Before stating that something is missing, blocked, or impossible, name the command that shows it. If you did not run it, say you are inferring.
- **Never** skip, disable, or delete a test to get green; never rewrite history on a shared branch; never store a secret in the repo.

## Where things live
- Agents: `.github/agents/*.agent.md` (canonical) → mirrored to `.claude/agents/` by `tools/sync_claude.py`
- Skills: `.claude/skills/<name>/SKILL.md` (read by both Copilot and Claude Code)
- Path rules: `.github/instructions/*.instructions.md`
- Hooks: `.github/hooks/*.json` (Copilot) and `.claude/settings.json` (Claude Code) — both call `tools/hooks/guard.py`
- Corpus, registers, evals, board: `fleet/`
