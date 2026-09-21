# fleet-kit

**A reference layout for a bounded, self-improving agent fleet — one set of files, loaded by both GitHub Copilot and Claude Code.**

Eighteen agents in five teams, ten skills, hooks that hold regardless of prompt, a capability register, structural and behavioral evals, and a small sample application for the fleet to work on. Nothing here needs a custom runtime: every piece is a documented extension point of the tools you already use.

```
prompt / sweep / schedule
        │
        ▼
   ┌─ bounds ──────────────┐   instructions (always-on) + hooks (cannot be talked past)
   │                       │
   │   agent ──▶ skill ────┼─▶ tools (shell, MCP) ──▶ artifacts
   │   (role)   (procedure)│
   └───────────────────────┘
        │
        ▼
   session report ──▶ score ──▶ find the repeat ──▶ reinforce (PR) ──▶ next run starts stronger
```

## Why this shape

| Problem | What the layout does about it |
|---------|-------------------------------|
| Agents drift and improvise | Each agent is one file: a description (when), a tools allowlist (what), and **Bounds** (never). |
| Rules in prose get talked past | Rules that must always hold live in **hooks** (`preToolUse`), which run before the tool does. |
| "It's blocked" turns out to be a guess | **Measure before claiming** is a skill, an agent (`claim-auditor`), and a register with evidence per row. |
| Every session starts from zero | The **learning loop**: fixed-shape session reports → scored → repeated patterns moved into agents, skills, instructions or hooks, as pull requests. |
| Two tools, two configs | `.github/agents/` is canonical; `tools/sync_claude.py` generates `.claude/agents/`. Skills live once in `.claude/skills/`, which both tools read. |

## Layout

```
.github/
  copilot-instructions.md      repo-wide rules (Copilot; Claude reads it via CLAUDE.md)
  instructions/*.instructions.md   path-scoped rules (applyTo globs)
  agents/*.agent.md            18 agents — canonical
  prompts/*.prompt.md          reusable prompts (VS Code)
  hooks/guard.json             preToolUse / agentStop → tools/hooks/*.py
  mcp.json                     MCP servers
  workflows/validate-fleet.yml structural evals + tests in CI
.claude/
  agents/*.md                  generated mirror of .github/agents (do not edit)
  skills/<name>/SKILL.md       10 skills — read by Copilot and Claude Code
  settings.json                Claude Code hooks → the same tools/hooks/*.py
AGENTS.md · CLAUDE.md          shared agent instructions (CLAUDE.md imports both)
fleet/
  README.md                    the fleet map
  corpus/                      facts with sources
  registers/capabilities.md    what agents may do, measured
  evals/                       rubric, scorecards, cases
  learning/                    a worked reinforcement PR
  board.md                     current state, rebuilt by every sweep
reports/  drafts/              session reports · outbound messages a human sends
sample_app/  tests/            the thing the fleet works on (Python, pytest)
tools/                         sync_claude.py · validate_fleet.py · hooks/guard.py
```

## Try it

```bash
pip install pytest
python tools/validate_fleet.py      # structural evals: agents, skills, hooks, instructions
python tools/sync_claude.py --check # .claude/agents mirror is current
python -m pytest -q                 # sample app (one xfail: the seeded bug KI-1)
```

Then, in Copilot CLI or Claude Code, from the repo root:

- `triage: tests are failing on pricing` — `triager` reproduces KI-1, classifies it, locates `sample_app/pricing.py`, and hands on with a session report. It does not fix it.
- `sweep` — `lead` runs the master sweep and rebuilds `fleet/board.md`.
- `reinforce` — `pattern-miner` reads recent reports and scorecards and proposes one change; `skill-smith` opens it as a PR. A worked example is in `fleet/learning/`.

## The five teams

| Team | Agents |
|------|--------|
| Orchestration | `lead` · `planner` · `reporter` |
| Delivery | `triager` · `implementer` · `test-writer` · `reviewer` · `release-manager` |
| Quality + Learning | `quality-auditor` · `pattern-miner` · `skill-smith` · `claim-auditor` |
| Knowledge | `docs-writer` · `corpus-librarian` · `changelog-keeper` |
| Safety + Ops | `security-scanner` · `dependency-steward` · `capability-registrar` |

Full one-liners in [`fleet/README.md`](fleet/README.md).

## The bounds that hold everywhere

- **Drafts only.** Anything addressed to a person outside the repo is written to `drafts/` for a human to send. Reads are never restricted by this rule.
- **Human gates.** Merge, tag, release, publish — humans do these; agents prepare the exact commands.
- **Measure before claiming.** Name the command before saying something is missing or blocked.
- **Fleet changes are pull requests.** Enforced by an instruction file and checked in CI.

## Built on

- [Custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration) · [Agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) ([open standard](https://github.com/agentskills/agentskills)) · [Custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) · [Hooks](https://docs.github.com/en/copilot/reference/hooks-reference) · [MCP servers](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers) · [Copilot CLI customization](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/overview) · [Customization cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)
- [Claude Code](https://docs.claude.com/en/docs/claude-code) — sub-agents, skills, hooks, `CLAUDE.md`
- [AGENTS.md](https://github.com/agentsmd/agents.md) · [Model Context Protocol](https://modelcontextprotocol.io)

## Scaling it

The same layout scales by adding files, not machinery: more agents in `.github/agents/`, more skills, more corpus. To run the fleet unattended, the agent definitions deploy unchanged into containers (for example Azure Container Apps) as triggerable runners, with identity verified per call and sources reached through MCP.

## License

MIT
