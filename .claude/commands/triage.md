---
description: Reproduce, classify, and locate a reported problem.
argument-hint: <bug report, failing test name, command, or known-issue id>
---
Use the `triager` subagent. Triage this: $ARGUMENTS

Reproduce it first and paste the actual output. Classify it. Locate it as path:line. Hand on to `test-writer` with a session report in `reports/`.

Mirrors `.github/prompts/triage.prompt.md`.
