# fleet-kit

**A reference layout for a bounded, self-improving agent fleet — one source of truth, loaded by both GitHub Copilot and Claude Code.**

Eighteen agents in five teams, ten skills, flows that chain them together, hooks that hold regardless of prompt, a capability register, structural and behavioural evals, and a small sample application for the fleet to work on. Nothing here needs a custom runtime: every piece is a documented extension point of the tools you already use.

## The model, in four parts

| | What it is | Where it lives |
|---|---|---|
| **Agent** | One file that defines a role, the skills it may call, and the limits it works inside. | `.github/agents/*.agent.md` |
| **Skill** | The procedure behind a piece of work: the steps to follow, the tool to use, and what a finished result looks like. An agent may hold one skill or several. | `.claude/skills/<name>/SKILL.md` |
| **Flow** | A path that worked, written down — agents and their skills in the order that gets a job done, ending in a handoff. Flows chain. | `flows/*.md` |
| **Orchestrator** | The agent above the others. It decides which agent takes which task, keeps the right ones engaged, and returns finished work to the human. | `.github/agents/lead.agent.md` |

```
prompt / sweep / schedule
        │
        ▼
   ┌─ the limits ──────────┐   instructions (always-on) + hooks (cannot be talked past)
   │                       │
   │  orchestrator         │
   │       │               │
   │       ▼               │
   │   agent ──▶ skill ────┼─▶ tools (shell, MCP) ──▶ artifacts
   │   (role)   (procedure)│
   └───────────────────────┘
        │
        ▼
   session report ──▶ score ──▶ find the repeat ──▶ reinforce (PR) ──▶ next run starts stronger
                                      │
                                      └──▶ the path that worked becomes a flow, and flows chain
```

## Why this shape

| Problem | What the layout does about it |
|---------|-------------------------------|
| Agents drift and improvise | Each agent is one file: a description (when), a tools allowlist (what), and limits (never). |
| Rules in prose get talked past | Rules that must always hold live in **hooks** (`preToolUse`), which run before the tool does. |
| Work is repeated from scratch every time | A path that worked is written down as a **flow**, and the flow runs it next time. |
| "It's blocked" turns out to be a guess | **Measure before claiming** is a skill, an agent (`claim-auditor`), and a register with evidence per row. |
| Every session starts from zero | The **learning loop**: fixed-shape session reports → scored → repeated patterns moved into agents, skills, flows, instructions or hooks, as pull requests. |
| Two tools, two configs | `.github/agents/` is canonical; `tools/sync_claude.py` generates the `.claude/agents/` mirror, checked in CI. Skills live once in `.claude/skills/`, which both tools read. |

## The guardrails

These hold no matter what a prompt says.

- **Tools allowlist.** Every agent declares its tools in its own file. It cannot reach a tool it was not given.
- **Hooks.** `.github/hooks/guard.json` and `.claude/settings.json` both call `tools/hooks/guard.py`, which denies force-pushes, `reset --hard`, test deselection and outbound sends — before the command runs.
- **Drafts only.** Anything addressed to a person outside the repository is written to `drafts/` for a human to send. Reading is never restricted by this rule.
- **Human gates.** Merge, tag, release and publish are done by a human. Agents prepare the exact commands.
- **Measure before claiming.** Name the command before saying something is missing or blocked.
- **Fleet changes are pull requests.** Enforced by an instruction file and checked in CI.

## Layout

```
.github/
  copilot-instructions.md          repo-wide rules (Copilot; Claude reads it via CLAUDE.md)
  instructions/*.instructions.md   path-scoped rules (applyTo globs)
  agents/*.agent.md                18 agents — canonical
  prompts/*.prompt.md              reusable prompts (VS Code)
  hooks/guard.json                 preToolUse / agentStop → tools/hooks/*.py
  mcp.json                         MCP servers
  workflows/validate-fleet.yml     structural evals + tests in CI
.claude/
  agents/*.md                      generated mirror of .github/agents (do not edit)
  skills/<name>/SKILL.md           10 skills — read by Copilot and Claude Code
  settings.json                    Claude Code hooks → the same tools/hooks/*.py
flows/*.md                         paths that worked, chained by their handoffs
docs/hosted-runners.md             how the same files would run without a laptop (a design)
deploy/                            the v2 template — federated MCP, one container per agent
AGENTS.md · CLAUDE.md              shared agent instructions (CLAUDE.md imports both)
fleet/
  README.md                        the fleet map
  corpus/                          facts with sources
  registers/capabilities.md        what agents may do, measured
  evals/                           rubric, scorecards, cases
  learning/                        a worked reinforcement PR
  board.md                         current state, rebuilt by every sweep
reports/  drafts/                  session reports · outbound messages a human sends
sample_app/  tests/                the thing the fleet works on (Python, pytest)
tools/                             sync_claude.py · validate_fleet.py · hooks/guard.py
```

## Try it

```bash
pip install pytest
python tools/validate_fleet.py      # structural evals: agents, skills, hooks, instructions
python tools/sync_claude.py --check # the .claude/agents mirror is current
python -m pytest -q                 # sample app (one xfail: the seeded bug KI-1)
```

Then, in Copilot CLI or Claude Code, from the repo root:

- `triage: tests are failing on pricing` — `triager` reproduces KI-1, classifies it, locates `sample_app/pricing.py`, and hands on with a session report. It does not fix it. That path is written down as [`flows/triage-a-failing-test.md`](flows/triage-a-failing-test.md).
- `sweep` — `lead`, the orchestrator, runs the master sweep and rebuilds `fleet/board.md`. See [`flows/sweep-the-board.md`](flows/sweep-the-board.md).
- `reinforce` — `pattern-miner` reads recent reports and scorecards and proposes one change; `skill-smith` opens it as a pull request. A worked example is in [`fleet/learning/`](fleet/learning/example-reinforcement.md).

## The five teams

| Team | Agents |
|------|--------|
| Orchestration | `lead` (the orchestrator) · `planner` · `reporter` |
| Delivery | `triager` · `implementer` · `test-writer` · `reviewer` · `release-manager` |
| Quality + Learning | `quality-auditor` · `pattern-miner` · `skill-smith` · `claim-auditor` |
| Knowledge | `docs-writer` · `corpus-librarian` · `changelog-keeper` |
| Safety + Ops | `security-scanner` · `dependency-steward` · `capability-registrar` |

Full one-liners in [`fleet/README.md`](fleet/README.md).

## Built on

- [Custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration) · [Agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) ([open standard](https://github.com/agentskills/agentskills)) · [Custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) · [Hooks](https://docs.github.com/en/copilot/reference/hooks-reference) · [MCP servers](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers) · [Copilot CLI customization](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/overview) · [Customization cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)
- [Claude Code](https://docs.claude.com/en/docs/claude-code) — sub-agents, skills, hooks, `CLAUDE.md`
- [AGENTS.md](https://github.com/agentsmd/agents.md) · [Model Context Protocol](https://modelcontextprotocol.io)

## Scaling it, and running it without a laptop

The layout scales by adding files, not machinery: more agents, more skills, more flows, more corpus.

Running it unattended is a different question, and the answer is in [`deploy/`](deploy/) as a template rather than a claim. The agents, skills, flows and limits do not change at all; what changes is where they run and how each run proves who it is. One container per agent, reached only on a private network, with the caller's identity forwarded to every source through a federated MCP configuration and a log kept per run. [`deploy/mcp-hosted.json`](deploy/mcp-hosted.json) is the interesting file — it is where an agent's declared tools allowlist stops being a suggestion and becomes a network boundary.

The reasoning, including what would have to be true before any of it ships, is in [`docs/hosted-runners.md`](docs/hosted-runners.md). Nothing in either file is deployed anywhere today, and both say so.

## About this repository

fleet-kit is a personal side project by [@zacha0dev](https://github.com/zacha0dev), published as an open reference for anyone building their own agent fleet. It is not affiliated with, endorsed by, or connected to any employer, and it contains no proprietary, customer or production data. The sample application and the agents around it are a generic software development workflow, written from scratch for this repository.

MIT licensed — clone it, strip it, rebuild it for your own domain.

## License

MIT
