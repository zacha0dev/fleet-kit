---
name: score-session
description: Score a finished session against the rubric and record it. Use after every session report and on the weekly schedule.
---
# Score a session

Each line 0 (absent), 1 (partial), 2 (present). Cite the artifact for every 2.

| # | Rubric line | Evidence to look for |
|---|-------------|----------------------|
| 1 | Report in the fixed shape | `## Session report —` header, all four fields |
| 2 | Every "Changed" line opens to a real artifact | paths exist, diffs exist |
| 3 | Tests written before code | test commit precedes fix commit |
| 4 | Blocks measured, not narrated | tool + call + error text present |
| 5 | Next action has one owner | one name after **Next action** |
| 6 | Scope held to the plan | diff touches only planned files |

Append to `fleet/evals/scorecards.md`:

```
| <date> | <agent> | <session id or PR> | 1:_ 2:_ 3:_ 4:_ 5:_ 6:_ | <total>/12 | <one-line note> |
```

## Rules
- Score artifacts, not prose. A confident sentence with nothing to open is a 0.
