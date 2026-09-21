# Evals

Two kinds.

**Structural** — `python tools/validate_fleet.py`. Every agent has a description, a tools allowlist, and bounds; every skill has a matching name and steps; every hook parses; every instruction has `applyTo`. Runs in CI on every push.

**Behavioral** — `rubric.md` scored by `quality-auditor` after each session into `scorecards.md`. The scorecards are the input to `pattern-miner`, which is how the fleet learns.

`cases/` holds prompts with expected outcomes for spot-checking an agent after a change to its file.
