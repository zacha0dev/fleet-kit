#!/usr/bin/env bash
# Run one agent, once, with a caller identity. This is what a trigger invokes.
#
#   ./run-once.sh triager "reproduce the failing pricing test"
#
# A template: REPLACE_ME values are yours. The point of the script is the
# order of operations, not the CLI it happens to use.
set -euo pipefail

AGENT="${1:?usage: run-once.sh <agent> <task>}"
TASK="${2:?usage: run-once.sh <agent> <task>}"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-${AGENT}"

# 1. Establish the caller. No identity, no run — this is the fail-closed rule
#    from mcp-hosted.json, enforced before anything is contacted.
CALLER_ID="${FLEET_CALLER_ID:-}"
if [ -z "$CALLER_ID" ]; then
  echo "refusing to run: no caller identity supplied" >&2
  exit 1
fi

# 2. Check the agent is one we actually deploy, so a typo cannot silently
#    start something arbitrary.
python - "$AGENT" <<'PY'
import json, sys
roster = {a["name"] for a in json.load(open("deploy/agents.json"))["agents"]}
if sys.argv[1] not in roster:
    sys.exit(f"refusing to run: {sys.argv[1]} is not in deploy/agents.json")
PY

# 3. Dispatch to that agent's container app. One agent, one task, one run id.
echo "run ${RUN_ID} · agent ${AGENT} · caller ${CALLER_ID}"
az containerapp job start \
  --name "fleet-${AGENT}" \
  --resource-group REPLACE_ME \
  --env-vars "FLEET_AGENT=${AGENT}" "FLEET_CALLER_ID=${CALLER_ID}" \
             "FLEET_TASK=${TASK}" "FLEET_RUN_ID=${RUN_ID}"

# 4. The run writes its own session report. Nothing is considered finished
#    without one — same rule as v1, same fixed shape.
echo "report will be written to reports/${RUN_ID}.md"
