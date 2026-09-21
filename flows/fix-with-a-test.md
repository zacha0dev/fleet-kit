---
name: fix-with-a-test
description: Write the failing test, make the smallest change that passes it, and run the suite.
handoff: flows/review-a-change.md
---

1. **Write the failing test** — `test-writer` · `write-tests-first` · shell
   It must fail, and fail for the stated reason. Paste the failure.
2. **Make the smallest change** — `implementer` · shell, edit
   Only the files named in the plan. Match the surrounding style.
3. **Run the whole suite** — `implementer` · shell
   Paste the summary line.
4. **Report** — `implementer` · `session-report`

→ hands off to `flows/review-a-change.md`
