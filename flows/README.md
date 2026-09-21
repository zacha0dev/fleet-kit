# Flows

A **flow** is a path that worked, written down. One or more agents and their skills, in the order that gets a piece of work done, with the handoff at the end naming what comes next.

A flow is the unit that makes the fleet repeatable. An agent knows its role and a skill knows its procedure, but neither of them knows the shape of a whole job. The flow does.

## How a flow is used

1. An engineer prompts, and the work happens through agents and skills as usual.
2. When the path taken was the right one, it is written down here as a flow.
3. The next time that job comes up, the flow runs it — nobody retypes the prompt.
4. When an engineer corrects something, the correction is written into the flow or into the agent that should have known it, so the next run starts from the better version.
5. Flows chain. One flow's handoff is the next flow's trigger, and a chain of them finishes a complete job without anyone driving each step.

That chaining is what we mean by **loop engineering**: capture how the work is actually done, give it bounds, run it, and strengthen it every time it runs.

## Writing one

Each flow is a Markdown file with frontmatter and numbered steps. Every step names the agent, the skill it calls, and the tool that skill reaches. The last line names the handoff.

```markdown
---
name: triage-a-failing-test
description: Reproduce a reported failure, classify it, and hand it to the implementer.
handoff: flows/fix-with-a-test.md
---

1. **Reproduce the failure** — `triager` · `triage-issue` · shell
2. **Classify it** — `triager` · `triage-issue`
3. **Locate the smallest function the evidence points to** — `triager` · `triage-issue`
4. **Write the session report** — `triager` · `session-report`

→ hands off to `flows/fix-with-a-test.md`
```

## Rules

- A flow records what was done, not what someone hoped would be done. Write it after a run that worked, not before.
- Every step names its agent and skill. A step that names neither is a wish.
- A flow that never names a handoff is a leaf. That is fine, but say so.
- Flows are files, so changing one is a pull request, reviewed like code.
