# Hosted runners — the same fleet, running without a laptop

**Status: design, not deployment.** Nothing in this document is running. It describes how the files in this repository are meant to move into containers, and what would have to be true for that to be safe. It is written down so the shape can be argued with before anyone builds it.

## What runs today

The fleet runs inside a Copilot session on a workstation. An engineer prompts, the orchestrator routes the task, agents load their skills, skills reach tools through MCP, and the result comes back. Every call runs as the engineer, using the access they already have.

Two things follow from that, and both are limits:

- **Work stops when the session does.** Close the laptop and nothing progresses.
- **Nothing starts on its own.** A person types, or nothing happens.

Parallelism today means many sessions on one machine. That is real, and it is also the ceiling.

## What hosting changes

The agent files, the skills, the flows and the limits do not change at all. What changes is *where they run* and *how each run proves who it is*.

| | On a workstation | As a hosted runner |
|---|---|---|
| Where it runs | one Copilot session | one container per agent |
| What starts it | a person typing | a prompt, a schedule, or an event |
| How it is reached | locally | over a private network |
| Identity | the session's signed-in user | verified by the container on every call |
| What is left behind | the session transcript | a per-run log, retained |
| When the laptop closes | it stops | it continues |

## The shape

```
  engineer ──prompt / schedule / event──▶  [ private network ]
                                                   │
                                    ┌──────────────┴──────────────┐
                                    │   container per agent       │
                                    │   scoper · triager · …      │
                                    │   each verifies identity    │
                                    │   and auth on every call    │
                                    └──────────────┬──────────────┘
                                                   │
                                        federated MCP connections
                                                   │
                                  ┌────────────────┴────────────────┐
                                  │  sources, each with its own     │
                                  │  governed connection            │
                                  └─────────────────────────────────┘
                                                   │
                                    results and drafts ──▶ engineer
```

One container per agent, rather than one container running everything, for three reasons:

1. **The tools allowlist becomes a boundary you can see.** An agent that may not run shell does not have shell in its image.
2. **A runaway agent is one container.** It can be stopped without stopping the fleet.
3. **The run log is per agent and per run**, so "which agent did this" has an answer that does not depend on reading a transcript.

## What would have to be true before this ships

These are the open questions, not solved problems. Listing them is the point.

- **Identity.** A hosted runner acts on someone's behalf. It must carry the requesting engineer's identity to every call and be refused when it cannot — not fall back to a service account. A service account that can read everything is the failure mode this design exists to avoid.
- **Egress.** Each connection is governed separately. The container reaches a named set of sources and nothing else, and that set is declared, not discovered at runtime.
- **The drafts-only rule.** On a workstation this is enforced by a hook before the tool runs. Any hosted mode that pre-approves tool calls weakens that, so the rule has to be enforced where the send would actually happen, not only where it is requested. This is the single most important thing to get right, and it is the thing most likely to break quietly.
- **Retention.** A run log is a record of what touched which data. How long it is kept, and who can read it, is a decision for whoever owns the data — not a default.
- **Cost.** A fleet that can trigger itself can also run all night. Triggers need a ceiling before they need a scheduler.

## Why the files do not change

This is the part worth testing. If hosting required rewriting the agents, the layout would be wrong — it would mean the fleet was coupled to the session it happened to start in.

Because an agent is a file that declares a role, its skills and its limits, and a skill is a written procedure, neither of them knows or cares whether a human typed the prompt. The orchestrator routes the same way. The flows chain the same way. Only the trigger and the identity check are different, and both sit outside the agent definitions.

If that turns out to be false in practice, the layout needs fixing before the hosting does.
