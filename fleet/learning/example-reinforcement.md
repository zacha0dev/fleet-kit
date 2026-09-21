# Worked example: one reinforcement pull request

**Pattern found by `pattern-miner`** (two citations):
- Session report 2026-09-14, `implementer`: "Changed: sample_app/pricing.py" — but the diff also touched `tests/conftest.py`, which was not in the plan.
- Session report 2026-09-18, `implementer`: same shape — an unplanned edit to `tests/conftest.py`.

**Where it belongs:** this is a rule the agent should always follow, so it goes in `implementer`'s **Bounds**, not in a skill.

**The change** (`reinforce: implementer edits only planned files`):
```diff
 ## Bounds
 - Do not widen the change. A refactor you noticed goes in the session report as a next action, not in this diff.
+- Before running the suite, `git diff --name-only` must list only files named in the plan. Anything else is reverted or added to the plan first.
 - Never skip, disable, or delete a test to get green.
```

**Why a bound and not a hook:** the rule needs the plan to judge it, and hooks do not read plans. If the pattern were "never edit `conftest.py`", that would be a hook.

**Result:** scorecard line 6 (scope held) went from 1 to 2 on the next three `implementer` sessions.
