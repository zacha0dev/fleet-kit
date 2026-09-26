#!/usr/bin/env bash
# Run one agent, once, with a caller identity. This is what a trigger invokes.
#
#   FLEET_CALLER_ID=someone@example.com FLEET_RESOURCE_GROUP=my-group \
#     ./deploy/run-once.sh triager "reproduce the failing pricing test"
#
# A template. The point of the script is the order of operations, not the CLI
# it happens to use. It refuses to run while any required value is unset or
# still REPLACE_ME.
set -euo pipefail

# Work from the repository root wherever the script is called from.
cd "$(dirname "$0")/.."

AGENT="${1:?usage: run-once.sh <agent> <task>}"
TASK="${2:?usage: run-once.sh <agent> <task>}"

# 1. Establish the caller. No identity, no run — this is the fail-closed rule
#    from mcp-hosted.json, enforced before anything is contacted.
require() {
  local name="$1" value="${!1:-}"
  if [ -z "$value" ] || [ "$value" = "REPLACE_ME" ]; then
    echo "refusing to run: $name is not set" >&2
    exit 1
  fi
}
require FLEET_CALLER_ID
require FLEET_RESOURCE_GROUP

# 2. Check the agent is one we actually deploy, so a typo cannot silently
#    start something arbitrary.
PYTHON=""
for candidate in python3 python; do
  if "$candidate" -c "" >/dev/null 2>&1; then PYTHON="$candidate"; break; fi
done
[ -n "$PYTHON" ] || { echo "refusing to run: no python found" >&2; exit 1; }
"$PYTHON" - "$AGENT" <<'PY'
import json, sys
roster = {a["name"] for a in json.load(open("deploy/agents.json", encoding="utf-8"))["agents"]}
if sys.argv[1] not in roster:
    sys.exit(f"refusing to run: {sys.argv[1]} is not in deploy/agents.json")
PY

# 3. Name the run and its report the way reports/README.md does:
#    YYYY-MM-DD-<agent>-<slug>.md
DATE="$(date -u +%Y-%m-%d)"
SLUG="$(printf '%s' "$TASK" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//; s/-$//' | cut -c1-40)"
RUN_ID="${DATE}-${AGENT}-${SLUG:-task}"

# 4. Dispatch to that agent's container app job. One agent, one task, one run id.
echo "run ${RUN_ID} · agent ${AGENT} · caller ${FLEET_CALLER_ID}"
az containerapp job start \
  --name "fleet-${AGENT}" \
  --resource-group "${FLEET_RESOURCE_GROUP}" \
  --env-vars "FLEET_AGENT=${AGENT}" "FLEET_CALLER_ID=${FLEET_CALLER_ID}" \
             "FLEET_TASK=${TASK}" "FLEET_RUN_ID=${RUN_ID}"

# 5. The run writes its own session report. Nothing is considered finished
#    without one — same rule as on a workstation, same fixed shape.
echo "report expected at reports/${RUN_ID}.md"
