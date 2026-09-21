---
name: review-a-change
description: Review a diff for correctness, scope and coverage, and report findings by severity.
handoff: none — the human decides
---

1. **Read the description and the whole diff** — `reviewer` · `review-pr`
2. **Run the tests** — `reviewer` · `review-pr` · shell
3. **Report findings by severity** — `reviewer` · `review-pr`
   must fix · should fix · nit, each with `path:line`.
4. **Scan the diff for secrets and unsafe patterns** — `security-scanner` · shell
5. **Report** — `reviewer` · `session-report`

→ no handoff. A human approves and merges. Agents never do.
