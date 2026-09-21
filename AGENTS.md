# Agent instructions

Read by GitHub Copilot, Copilot CLI, and Claude Code. The full rules are in `.github/copilot-instructions.md`; this file carries the ones that apply to every agent in every tool.

1. End every session with a session report in the fixed shape.
2. Write the failing test before the code.
3. Outbound communication is drafts only; reads are never restricted.
4. Name the measurement before claiming an absence or a block.
5. Fleet changes ship as pull requests, never directly to the default branch.
6. One next action, one owner.
