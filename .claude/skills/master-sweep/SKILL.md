---
name: master-sweep
description: Run one prompt across every open item and return one board. Use when asked to sweep, check everything, or 'what is the state of things'.
---
# Master sweep

One prompt fans out to one session per item; every session returns the same report shape; the lead merges them into one board.

## Steps
1. List the items: open issues, failing checks, pull requests waiting, and anything in `fleet/board.md` marked open.
2. For each item, dispatch the agent the item's type calls for (`triager` for problems, `reviewer` for pull requests, `release-manager` for a pending release). Run them in parallel.
3. Each session ends with a `session-report`. Do not accept a session without one.
4. Merge the reports into `fleet/board.md`: one row per item — item, owner, state, next action, evidence link.
5. The board's last line is the one thing a human should do next.

## Rules
- A sweep changes no code. It reads, it reports, it queues.
- A session that could not run says which tool call failed. "Skipped" without a measured reason is a failed session.
