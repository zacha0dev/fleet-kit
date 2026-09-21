---
name: measure-before-claiming
description: Verify a claim about the world outside the repo before stating it. Use when about to write 'there is no', 'we cannot', 'X is blocked', or 'X owns'.
---
# Measure before claiming

An unmeasured absence claim is the most expensive sentence an agent writes: the human stops, checks, and finds the tool was fine.

## Steps
1. Catch the claim. Trigger phrases: *there is no*, *we don't have*, *can't access*, *is blocked*, *probably*, *should be*.
2. Name the measurement: the exact command or tool call that would confirm it.
3. Run it if you can. Paste the result.
4. Write the claim with its status in the same sentence:
   - **measured** — "`gh pr list` returned 403 (`HTTP 403: Resource not accessible`), so pull requests cannot be listed from this session."
   - **inferred** — "I have not run it; I am inferring the API is rate-limited from the earlier 429."

## Rules
- A tool that failed once is retried once before it is called unavailable. Disconnects are transient.
- "The runtime blocks it" is a claim about a layer. Name the file and line if it is a declaration, or the exact error if it is the runtime.
