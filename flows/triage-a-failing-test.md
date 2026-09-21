---
name: triage-a-failing-test
description: Reproduce a reported failure, classify it, locate it, and hand it on without fixing it.
handoff: flows/fix-with-a-test.md
---

1. **Reproduce the failure** — `triager` · `triage-issue` · shell
   Run the exact command from the report and paste the output. No reproduction, no triage.
2. **Classify it** — `triager` · `triage-issue`
   One of: bug, regression, expectation, environment.
3. **Locate it** — `triager` · `triage-issue`
   The smallest function the evidence points to, cited as `path:line`.
4. **Report** — `triager` · `session-report`
   What was touched, what was found, and the one next action.

→ hands off to `flows/fix-with-a-test.md`
