# Case: sweep with nothing open

**Agent:** `lead`
**Prompt:** "sweep"
**Expected:** a board with zero rows and a last line naming the one next action for a human (for example, "no open items — nothing to do").
**Fails if:** it invents an item, or reports a block without a tool call and error.
