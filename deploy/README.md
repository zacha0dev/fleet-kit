# deploy — the v2 template

**Status: a template, not a deployment.** Nothing here is running anywhere. These files are the shape a hosted fleet would take, written out so it can be read, argued with and adapted before anyone provisions a thing. Every value you must supply is marked `REPLACE_ME`.

The design reasoning is in [`docs/hosted-runners.md`](../docs/hosted-runners.md). This directory is the mechanical half.

## What v2 changes, and what it does not

The agents, skills, flows and limits in this repository do not change. An agent is a file that declares a role, its skills and what it may never do; none of that knows whether a human typed the prompt. What changes is where it runs and how each run proves who it is.

| | v1 — a workstation | v2 — hosted runners |
|---|---|---|
| Unit | one session | one container per agent |
| Trigger | a person types | prompt, schedule or event |
| Reach | local | private network only |
| Identity | the signed-in session | verified per call, per container |
| Record | the transcript | a retained log per run |

## The files

| File | What it is |
|---|---|
| `Dockerfile` | One image for every agent. The agent is chosen at start by `FLEET_AGENT`, so eighteen agents are eighteen apps from one build, not eighteen images. |
| `agents.json` | The roster the deployment loops over: which agents get a runner, and how much each may consume. |
| `mcp-hosted.json` | **The centre of this directory.** The v2 MCP configuration: each source reached through its own governed connection, with the caller's identity forwarded per call rather than a stored credential, and each agent seeing only the servers its role needs. |
| `run-once.sh` | What a trigger actually invokes — one agent, one task, one log line. |

## How it fits together

```
trigger (schedule | event | prompt)
        │
        ▼
  run-once.sh  ──▶  container app for one agent
                          │  FLEET_AGENT=triager
                          │  managed identity, no public ingress
                          ▼
                    mcp-hosted.json
                          │  one governed connection per source
                          ▼
                    sources  ──▶  result + run log ──▶ engineer
```

## Using it

Start by reading `mcp-hosted.json`. It is the architecture; the rest is packaging.

```bash
# Build the image — one image, the agent chosen at start
docker build -t REPLACE_ME/fleet-kit:latest -f deploy/Dockerfile .

# Run one agent once, as a named caller
FLEET_CALLER_ID=someone@example.com ./deploy/run-once.sh triager "reproduce the failing pricing test"
```

The hosting platform is deliberately not prescribed beyond the one `az` line in `run-once.sh`. Azure Container Apps is what this was written against, but nothing in the design needs it — a container per agent, a private network, a per-call identity and a retained log is the whole requirement.

## Read this before you deploy it

- **No public ingress.** A runner that answers the open internet is not this design. Every source in `mcp-hosted.json` defaults to `"network": "private"`, and the one public exception says so explicitly rather than inheriting it quietly.
- **No service account that can read everything.** Each container carries the requesting user's identity to every call and must fail closed when it cannot. A shared credential with broad read is precisely the failure this shape exists to avoid.
- **The drafts-only rule has to hold here too.** On a workstation a `preToolUse` hook denies outbound sends before the command runs. Confirm your hosted mode actually runs those hooks — some pre-approve tool calls, which would silently weaken the one rule that matters most.
- **Put a ceiling on triggers before you add a scheduler.** A fleet that can start itself can also run all night.
- **Decide retention before the first run.** A run log records what touched which data. How long it lives, and who may read it, belongs to whoever owns that data.
