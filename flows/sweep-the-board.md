---
name: sweep-the-board
description: Run one prompt across every open item and rebuild the board from the session reports.
handoff: none — returns to the engineer
---

1. **List the open items** — `lead` · `master-sweep`
   Open issues, failing checks, waiting pull requests, anything open in `fleet/board.md`.
2. **Dispatch one agent per item, in parallel** — `lead` · `master-sweep` · agent
   The item's type picks the agent: `triager` for problems, `reviewer` for pull requests.
3. **Collect every session report** — `lead` · `master-sweep`
   A session without a report is a failed session, not a skipped one.
4. **Rebuild the board** — `lead` · `master-sweep` · edit
   One row per item: item, owner, state, next action, evidence.

→ no handoff. The last line of the board is the one thing a human should do next.
