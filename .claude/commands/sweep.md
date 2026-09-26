---
description: Run the master sweep across every open item and rebuild the board.
---
Use the `lead` subagent. Run the `master-sweep` skill: dispatch one agent per open item in parallel, collect every session report, and rewrite `fleet/board.md`. End with the one thing a human should do next.

Mirrors `.github/prompts/sweep.prompt.md`.
