# One image, every agent. The agent is selected at start by FLEET_AGENT,
# so N agents are N container apps from one build rather than N images.
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /fleet

# The fleet is files. Copy the definitions, not a runtime.
COPY .github/agents/      .github/agents/
COPY .github/instructions/ .github/instructions/
COPY .github/hooks/       .github/hooks/
COPY .claude/skills/      .claude/skills/
COPY flows/               flows/
COPY tools/               tools/
COPY AGENTS.md CLAUDE.md  ./
COPY deploy/mcp-hosted.json /fleet/mcp.json

RUN pip install --no-cache-dir pytest

# Which agent this container is. Set per container app; no default on purpose,
# so a misconfigured app fails loudly instead of running something arbitrary.
ENV FLEET_AGENT=""
# Identity is supplied at call time by the platform, never baked in.
ENV FLEET_IDENTITY_MODE="caller"

# Fail closed: refuse to start without an agent name, and verify the fleet
# definitions are structurally valid before accepting any work.
ENTRYPOINT ["/bin/sh", "-c", "test -n \"$FLEET_AGENT\" || { echo 'FLEET_AGENT is not set; refusing to start' >&2; exit 1; }; python tools/validate_fleet.py && exec python -m tools.runner --agent \"$FLEET_AGENT\""]
