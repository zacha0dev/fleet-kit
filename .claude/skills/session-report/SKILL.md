---
name: session-report
description: Write the fixed end-of-session report. Use at the end of every session, before any summary or sign-off.
---
# Session report

The report is the unit of trust between sessions. Same shape every time, so the next session — or the human — can read ten of them in a minute.

```
## Session report — <agent> — <ISO timestamp>
**Changed:** <one artifact per line, with path; or "nothing">
**Touched but unchanged:** <files read, tools called, commands run>
**Blocked:** <tool + call + error text, or "none">
**Next action:** <one line, one owner>
```

## Rules
- Every line under **Changed** is something a reader can open. A narrated action is not a change.
- **Blocked** names the measurement. "No access" without the call that returned the error is not a block; it is a guess.
- **Next action** has one owner. Two owners is no owner.
