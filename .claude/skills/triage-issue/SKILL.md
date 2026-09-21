---
name: triage-issue
description: Reproduce, classify, and locate a reported problem before anyone fixes it. Use for bug reports, failing tests, and vague 'it's broken' requests.
---
# Triage an issue

## Steps
1. **Reproduce.** Run the exact command or test from the report. Paste the output verbatim. No reproduction, no triage.
2. **Classify.** One of: `bug` (wrong output), `regression` (was right before — name the commit), `expectation` (the report expects behavior the code never promised), `environment` (only fails here).
3. **Locate.** The smallest function the evidence points to, as `path:line`. Read it. Say in one sentence why the evidence points there.
4. **Hand on.** To `implementer` (bug, regression) or `docs-writer` (expectation) with steps 1–3 attached.

## Rules
- Do not fix. Triage that edits code has become implementation without a test.
- If reproduction fails, that is the finding. Report it as `environment` or `cannot reproduce` with what you ran.
