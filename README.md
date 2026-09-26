# fleet-kit

**A reference layout for a bounded agent fleet, designed to improve from scored sessions.** One source of truth, loaded by both GitHub Copilot and Claude Code.

**Why.** For people who use Copilot or Claude Code and want multi-agent work they can repeat and check. The problem it addresses: agents that forget what the last session learned, claim things they did not measure, or act without limits. Here every role, procedure and limit is a file, every session leaves a report, and a hook refuses the few actions that must never happen.

Eighteen agents, ten skills, flows that chain them, hooks that hold whatever the prompt says, and a small sample project for the fleet to work on. No custom runtime — every piece is a documented extension point of tools you already have.

## Quickstart (about five minutes)

```bash
git clone https://github.com/zacha0dev/fleet-kit && cd fleet-kit
pip install pytest
python tools/validate_fleet.py         # ok - 18 agents, 10 skills, 4 flows, hooks, prompts and instructions valid
python tools/sync_claude.py --check    # ok - the .claude/agents mirror is current
python -m pytest -q                    # 49 passed, 1 xfailed
python -m pytest -q --runxfail         # 1 failed, 49 passed - the seeded bug, KI-1
```

Then open the folder in Claude Code and run `/triage KI-1`, or in VS Code Copilot Chat run the `/triage` prompt with `KI-1`. The triager reproduces the failure, classifies it, locates it at `sample_app/pricing.py:22`, writes a report to `reports/`, and hands on to `test-writer`. It does not fix it.

## The model, in four parts

| | What it is | Where it lives |
|---|---|---|
| **Agent** | A role. One file: what it is for, which skills it may call, what it must never do. | `.github/agents/*.agent.md` |
| **Skill** | A procedure. The steps, the tool, and what finished looks like. An agent loads a skill when its role has a written procedure; some roles need none. | `.claude/skills/<name>/SKILL.md` |
| **Flow** | A path that worked, written down. Agents and skills in the order that gets a job done. Flows chain. | `flows/*.md` |
| **Orchestrator** | The agent above the rest. It routes each task and returns finished work to you. | `.github/agents/lead.agent.md` |

## How work moves

No agent carries a whole job. Each one does its part and hands off to the role that comes next.

```
you ──▶ lead ──▶ triager ──▶ test-writer ──▶ implementer ──▶ reviewer ──▶ you
          │   (a problem)        ▲
          └──▶ planner ──────────┘
              (a change to make)
          every handoff leaves a written artifact
```

`lead` is the orchestrator. A report of something wrong goes to `triager`; a request for a change goes to `planner`, whose plan names the tests `test-writer` writes first.

**Every handoff is written down, not held in context.** The triager leaves a reproduction. The test-writer leaves a failing test. The implementer leaves a diff and a test run. Each agent reads what the last one wrote.

That is what makes the fleet debuggable. When a result is wrong, the step that produced it is a file you can open — not a transcript you have to scroll.

## Work runs in parallel

One prompt sweeps everything open and dispatches one agent per item. You read the reports instead of opening the items.

```
/sweep       # lead dispatches, collects, and rebuilds fleet/board.md
```

`/sweep`, `/triage` and `/reinforce` are slash commands, not shell commands: Claude Code reads them from `.claude/commands/`, and VS Code Copilot Chat reads the same prompts from `.github/prompts/`.

Every session ends with a report in one fixed shape. A session without a report is a failed session, not a quiet one.

## The guardrails

These hold regardless of what a prompt asks for.

- **Tools allowlist.** Each agent declares its tools in its own file. It cannot reach one it was not given.
- **Hooks.** `tools/hooks/guard.py` runs before a shell command does — called by both `.github/hooks/guard.json` (Copilot) and `.claude/settings.json` (Claude Code). It denies force-pushes, `reset --hard`, test deselection and outbound sends, and `tests/test_guard.py` checks each rule. It matches command lines, so it stops the ordinary way of doing each thing, not every possible workaround.
- **Drafts only.** Anything addressed to a person outside the repo goes to `drafts/` for a human to send. Reading is never restricted by this.
- **Human gates.** Merge, tag, release, publish. Agents prepare the commands; people run them.
- **Fleet changes are pull requests.** Checked in CI.

## How it is meant to improve

Reports get scored. Repeats get found. The repeat gets written into the agent that should have known it — as a pull request. The next run starts from the better version.

That loop is designed, not yet demonstrated: the scorecards hold seed rows, and the example in [`fleet/learning/`](fleet/learning/example-reinforcement.md) is illustrative, not a recorded run. `/reinforce` starts it.

## Try it

The seeded bug, KI-1, is a real failing test marked `xfail(strict=True)` so CI stays green. A plain `pytest` run reports it as `xfailed`; `--runxfail` shows the failure the triager works from.

- `/triage KI-1` — the triager reproduces the bug, classifies it, locates it, and hands on to `test-writer`. It does not fix it. That path is [`flows/triage-a-failing-test.md`](flows/triage-a-failing-test.md).
- `/sweep` — the orchestrator rebuilds the board. See [`flows/sweep-the-board.md`](flows/sweep-the-board.md).
- `/reinforce` — the pattern-miner proposes one change and the skill-smith opens it as a PR.

In Copilot CLI, which reads the agents but not these prompt files, ask for the agent by name: "use the triager agent to triage KI-1".

## Layout

```
.github/agents/          18 agents — canonical
.github/instructions/    path-scoped rules
.github/hooks/           Copilot hook config, calls tools/hooks/guard.py
.github/prompts/         /sweep · /triage · /reinforce for Copilot Chat
.github/mcp.json         MCP servers for Copilot CLI (see below)
.claude/agents/          generated mirror (do not edit)
.claude/commands/        /sweep · /triage · /reinforce for Claude Code
.claude/settings.json    Claude Code hooks: guard.py before shell, require_report.py at stop
.claude/skills/          10 skills — both tools read these
flows/                   paths that worked, chained by handoff
fleet/                   corpus · capability register · evals · board
deploy/                  a template for hosted runners (not deployed)
docs/hosted-runners.md   how this runs without a laptop
tools/                   sync · validate · hooks · runner stub
sample_app/  tests/      the thing the fleet works on
```

`.github/agents/` is canonical; `tools/sync_claude.py` generates the `.claude/` mirror and CI checks it. Skills live once and both tools read them.

`.github/mcp.json` uses the `mcpServers` format that Copilot CLI reads from that path. The Copilot coding agent takes the same JSON pasted into the repository's Copilot settings, not from this file. VS Code reads `.vscode/mcp.json` with a `servers` key, and Claude Code reads `.mcp.json`; neither is included here. The GitHub server points at its read-only endpoint, and `@playwright/mcp` is pinned (0.0.82, the current version on 2026-09-26) with a named tool list.

## The teams

| Team | Agents |
|------|--------|
| Orchestration | `lead` · `planner` · `reporter` |
| Delivery | `triager` · `implementer` · `test-writer` · `reviewer` · `release-manager` |
| Quality + Learning | `quality-auditor` · `pattern-miner` · `skill-smith` · `claim-auditor` |
| Knowledge | `docs-writer` · `corpus-librarian` · `changelog-keeper` |
| Safety + Ops | `security-scanner` · `dependency-steward` · `capability-registrar` |

One-liners for each in [`fleet/README.md`](fleet/README.md).

## Running it without a laptop

The agents, skills, flows and limits do not change. What changes is where they run and how each run proves who it is: one container per agent, a private network, the caller's identity forwarded to every source, a log per run. The container's entry point, `tools/runner.py`, prints the run plan and stops: no agent CLI is installed in the image yet.

[`deploy/mcp-hosted.json`](deploy/mcp-hosted.json) is the file worth reading — it is where an agent's declared allowlist stops being a suggestion and becomes a network boundary. The reasoning, and what would have to be true before it ships, is in [`docs/hosted-runners.md`](docs/hosted-runners.md). Neither is deployed anywhere today, and both say so.

## Built on

[Custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration) · [Agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) · [Custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) · [Hooks](https://docs.github.com/en/copilot/reference/hooks-reference) · [MCP](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers) · [Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/overview) · [Claude Code](https://docs.claude.com/en/docs/claude-code) · [AGENTS.md](https://github.com/agentsmd/agents.md)

## About this repository

fleet-kit is a personal side project by [@zacha0dev](https://github.com/zacha0dev), published as an open reference for anyone building their own agent fleet. It is not affiliated with, endorsed by, or connected to any employer, and contains no proprietary, customer or production data. The sample project and the agents around it are a generic software development workflow, written from scratch for this repository.

MIT — clone it, strip it, rebuild it for your own domain. See [CONTRIBUTING.md](CONTRIBUTING.md) to send changes and [SECURITY.md](SECURITY.md) to report a problem privately.
