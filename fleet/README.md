# The fleet

Eighteen agents in five teams. Each agent is one file with a description (when to use it), a tools allowlist (what it may touch), and bounds (what it never does). Skills are the procedures agents load when relevant. Hooks are the rules that hold regardless of prompt.

| Team | Agent | Does |
|------|-------|------|
| Orchestration | `lead` | Routes incoming work to the right agent, runs the master sweep, and keeps one next action visible per item. |
| Orchestration | `planner` | Turns a request into a short, ordered plan with files to touch, tests to write first, and the stop condition. |
| Orchestration | `reporter` | Writes the end-of-session report in the fixed format: what changed, what was touched, what is next. |
| Delivery | `triager` | Reproduces a reported problem, classifies it, and hands it on with evidence. |
| Delivery | `implementer` | Makes the code change a plan calls for, smallest diff first, with the tests already in place. |
| Delivery | `test-writer` | Writes the failing test that pins the behavior before any code changes. |
| Delivery | `reviewer` | Reviews a diff for correctness, scope, and test coverage, and posts findings with severity. |
| Delivery | `release-manager` | Prepares a release: version, changelog, checklist, and the exact commands, as a draft for a human to run. |
| Quality + Learning | `quality-auditor` | Scores a finished session against the fleet's rubric and files the score. |
| Quality + Learning | `pattern-miner` | Reads recent session reports and scorecards, finds the pattern that repeats, and proposes exactly one reinforcement. |
| Quality + Learning | `skill-smith` | Writes or revises an agent, skill, instruction, or hook from a pattern-miner proposal, as a pull request. |
| Quality + Learning | `claim-auditor` | Audits any statement about the world outside the repo for a measurement, and marks the ones that lack one. |
| Knowledge | `docs-writer` | Updates user-facing documentation to match a change, in the same pull request. |
| Knowledge | `corpus-librarian` | Answers 'what do we already know about X' from `fleet/corpus/`, with citations, and files new facts back in. |
| Knowledge | `changelog-keeper` | Adds the changelog entry for a change in the Keep a Changelog format. |
| Safety + Ops | `security-scanner` | Checks a diff for secrets, unsafe patterns, and dependency risks, and blocks with evidence. |
| Safety + Ops | `dependency-steward` | Reviews dependency changes: why the bump, what changed upstream, and what it breaks. |
| Safety + Ops | `capability-registrar` | Keeps `fleet/registers/capabilities.md` true: what each agent may do, which tool does it, and whether a reported block was measured. |

## How a run flows
```
trigger ──▶ bounds ──▶ agent ──▶ skill ──▶ tools ──▶ session report
 prompt     instructions  .github/   .claude/   MCP,      reports/ + board
 sweep      + hooks       agents     skills     shell
 schedule
```
Every session ends with a report in one fixed shape. The `quality-auditor` scores it; the `pattern-miner` finds what repeats; the `skill-smith` moves the repeat into an agent, a skill, an instruction, or a hook — as a pull request. That is the learning loop, and it is the only way the fleet changes.

## Where the knowledge lives
- `corpus/` — facts about this project, each with a source
- `registers/capabilities.md` — what agents may do, measured
- `evals/` — the rubric, the scorecards, and structural evals (`tools/validate_fleet.py`)
- `learning/` — worked example of a reinforcement pull request
- `board.md` — the current state, rebuilt by every sweep
