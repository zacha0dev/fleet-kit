---
name: capability-register
description: Record what each agent may do, which tool does it, and whether a reported block was measured. Use when an agent reports it cannot do something, or when adding a capability.
---
# Capability register

`fleet/registers/capabilities.md` is the fleet's answer to "can we?". It is only useful if every row was measured.

## When an agent reports a block
1. Find the layer:
   - **Declaration** — a line in this repo (`copilot-instructions.md`, an `*.instructions.md`, an agent's Bounds). Editable. Cite `path:line`.
   - **Runtime** — the tool's own policy. Cite the exact error text and the call.
   - **Conflict** — two declarations disagree. Cite both lines.
2. Record it: capability · tool · layer · evidence · date · status (`allowed`, `blocked-measured`, `reported-unmeasured`).
3. If the layer is a declaration and the block is unwanted, the fix is a pull request to that file, not a workaround.

## Rules
- Reading is not sending. A rule about outbound messages never blocks a read.
- A row without evidence is deleted on the next audit.
