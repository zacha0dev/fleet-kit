---
name: reinforce-pattern
description: Turn a pattern that repeated across sessions into one change to the fleet, as a pull request. Use when the same fix, mistake, or check appears twice.
---
# Reinforce a pattern

This is the learning loop: report → score → find the repeat → move it into the fleet → every next session starts with it.

## Steps
1. Read the last ten session reports and the scorecards. List every fix, mistake, or manual check that appears **at least twice**. Cite both occurrences.
2. Pick the most frequent one. Decide where it belongs:
   - a rule an agent should always follow → that agent's **Bounds**
   - a procedure → the relevant **skill's Steps**
   - a fact about this repo → `.github/copilot-instructions.md` or a corpus file
   - something that must never happen regardless of prompt → a **hook** in `.github/hooks/`
3. Write the change as the smallest edit to that one file.
4. Run `python tools/validate_fleet.py` and `python tools/sync_claude.py`.
5. Open a pull request titled `reinforce: <pattern>` with the two citations in the body.

## Rules
- One pattern per pull request.
- A rule that can be stated as a check goes in a hook, not in prose. Prose can be talked past; a hook cannot.
- Worked example: `fleet/learning/example-reinforcement.md`.
