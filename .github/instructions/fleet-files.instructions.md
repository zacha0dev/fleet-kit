---
applyTo: ".github/agents/**,.claude/skills/**,.github/instructions/**,.github/hooks/**,fleet/**"
---
# Fleet files

These files are the fleet. Edit them only through a pull request titled `reinforce: …` or `fleet: …`. After editing agents, run `python tools/sync_claude.py`. Before opening the pull request, run `python tools/validate_fleet.py` and paste its summary in the description.
