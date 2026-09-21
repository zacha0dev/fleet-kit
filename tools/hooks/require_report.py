#!/usr/bin/env python3
"""agentStop / Stop hook — remind the agent if no session report was written this session.

Both runtimes pass a payload on stdin; neither includes the transcript in a stable way,
so this hook checks the one durable artifact: fleet/board.md or reports/ got a new report today.
It never blocks; it injects a reminder as additional context.
"""
import datetime, glob, json, os, sys

def main():
    try: json.load(sys.stdin)
    except Exception: pass
    today = datetime.date.today().isoformat()
    fresh = [p for p in glob.glob("reports/*.md") if today in os.path.basename(p)]
    if not fresh:
        print(json.dumps({"additionalContext": "No session report was written to reports/ today. Write one in the fixed shape (session-report skill) before ending."}))

if __name__ == "__main__":
    main()
