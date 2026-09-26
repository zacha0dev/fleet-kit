# Contributing

Issues and pull requests are welcome.

Before opening a pull request, run the same three checks CI runs:

```bash
python tools/validate_fleet.py
python tools/sync_claude.py --check
python -m pytest -q
```

- **Agents** are edited in `.github/agents/`. Run `python tools/sync_claude.py` afterwards; never edit `.claude/agents/` by hand.
- **Fleet changes** (agents, skills, instructions, hooks, flows) use a title starting `fleet:` or `reinforce:`, as `.github/copilot-instructions.md` asks.
- **Tests first.** A change to `sample_app/` or `tools/` comes with a test in `tests/`. Do not skip or deselect tests to get green.
- **Claims.** Say what you ran. A statement about behavior outside the repo names the command that shows it.
- **KI-1** is a seeded bug kept open for the triage demo. Please do not send a fix for it.

By contributing you agree your contribution is released under the MIT license in `LICENSE`.
