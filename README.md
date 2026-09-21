# fleet-kit

**A reference layout for a bounded, self-improving agent fleet.** One source of truth, loaded by both GitHub Copilot and Claude Code.

Eighteen agents, ten skills, flows that chain them, hooks that hold whatever the prompt says, and a small sample project for the fleet to work on. No custom runtime — every piece is a documented extension point of tools you already have.

## The model, in four parts

| | What it is | Where it lives |
|---|---|---|
| **Agent** | A role. One file: what it is for, which skills it may call, what it must never do. | `.github/agents/*.agent.md` |
| **Skill** | A procedure. The steps, the tool, and what finished looks like. An agent holds one or several. | `.claude/skills/<name>/SKILL.md` |
| **Flow** | A path that worked, written down. Agents and skills in the order that gets a job done. Flows chain. | `flows/*.md` |
| **Orchestrator** | The agent above the rest. It routes each task and returns finished work to you. | `.github/agents/lead.agent.md` |

## How work moves

No agent carries a whole job. Each one does its part and hands off to the role that comes next.

```
you ──▶ orchestrator ──▶ triager ──▶ test-writer ──▶ implementer ──▶ reviewer ──▶ you
                              └── every handoff leaves a written artifact ──┘
```

**Every handoff is written down, not held in context.** The triager leaves a reproduction. The test-writer leaves a failing test. The implementer leaves a diff and a test run. Each agent reads what the last one wrote.

That is what makes the fleet debuggable. When a result is wrong, the step that produced it is a file you can open — not a transcript you have to scroll.

## Work runs in parallel

One prompt sweeps everything open and dispatches one agent per item. You read the reports instead of opening the items.

```bash
sweep        # lead dispatches, collects, and rebuilds fleet/board.md
```

Every session ends with a report in one fixed shape. A session without a report is a failed session, not a quiet one.

## The guardrails

These hold regardless of what a prompt asks for.

- **Tools allowlist.** Each agent declares its tools in its own file. It cannot reach one it was not given.
- **Hooks.** `tools/hooks/guard.py` runs before the tool does — called by both `.github/hooks/guard.json` and `.claude/settings.json`. It denies force-pushes, `reset --hard`, test deselection and outbound sends.
- **Drafts only.** Anything addressed to a person outside the repo goes to `drafts/` for a human to send. Reading is never restricted by this.
- **Human gates.** Merge, tag, release, publish. Agents prepare the commands; people run them.
- **Fleet changes are pull requests.** Checked in CI.

## It gets better with use

Reports get scored. Repeats get found. The repeat gets written into the agent that should have known it — as a pull request. The next run starts from the better version.

A worked example is in [`fleet/learning/`](fleet/learning/example-reinforcement.md).

## Try it

```bash
pip install pytest
python tools/validate_fleet.py      # 18 agents, 10 skills, hooks, instructions
python tools/sync_claude.py --check # the .claude/agents mirror is current
python -m pytest -q                 # 6 passed, 1 xfailed — the seeded bug
```

Then, from the repo root in Copilot CLI or Claude Code:

- `triage: tests are failing on pricing` — the triager reproduces the seeded bug, classifies it, locates it, and hands on. It does not fix it. That path is [`flows/triage-a-failing-test.md`](flows/triage-a-failing-test.md).
- `sweep` — the orchestrator rebuilds the board. See [`flows/sweep-the-board.md`](flows/sweep-the-board.md).
- `reinforce` — the pattern-miner proposes one change and the skill-smith opens it as a PR.

## Layout

```
.github/agents/          18 agents — canonical
.github/instructions/    path-scoped rules
.github/hooks/           deny rules, enforced before the tool runs
.claude/agents/          generated mirror (do not edit)
.claude/skills/          10 skills — both tools read these
flows/                   paths that worked, chained by handoff
fleet/                   corpus · capability register · evals · board
deploy/                  the v2 template — hosted runners, federated MCP
docs/hosted-runners.md   how this runs without a laptop
tools/                   sync · validate · hooks
sample_app/  tests/      the thing the fleet works on
```

`.github/agents/` is canonical; `tools/sync_claude.py` generates the `.claude/` mirror and CI checks it. Skills live once and both tools read them.

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

The agents, skills, flows and limits do not change. What changes is where they run and how each run proves who it is: one container per agent, a private network, the caller's identity forwarded to every source, a log per run.

[`deploy/mcp-hosted.json`](deploy/mcp-hosted.json) is the file worth reading — it is where an agent's declared allowlist stops being a suggestion and becomes a network boundary. The reasoning, and what would have to be true before it ships, is in [`docs/hosted-runners.md`](docs/hosted-runners.md). Neither is deployed anywhere today, and both say so.

## Built on

[Custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration) · [Agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) · [Custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) · [Hooks](https://docs.github.com/en/copilot/reference/hooks-reference) · [MCP](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers) · [Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/overview) · [Claude Code](https://docs.claude.com/en/docs/claude-code) · [AGENTS.md](https://github.com/agentsmd/agents.md)

## About this repository

fleet-kit is a personal side project by [@zacha0dev](https://github.com/zacha0dev), published as an open reference for anyone building their own agent fleet. It is not affiliated with, endorsed by, or connected to any employer, and contains no proprietary, customer or production data. The sample project and the agents around it are a generic software development workflow, written from scratch for this repository.

MIT — clone it, strip it, rebuild it for your own domain.
