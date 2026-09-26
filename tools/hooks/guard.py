#!/usr/bin/env python3
"""PreToolUse guard: deny a short list of commands before they run, whatever the prompt said.

Called by both runtimes:
  - Claude Code  (.claude/settings.json, PreToolUse). Input on stdin:
      {"tool_name": "Bash", "tool_input": {"command": "..."}, ...}
    A denial is printed as
      {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                              "permissionDecision": "deny",
                              "permissionDecisionReason": "..."}}
  - GitHub Copilot (.github/hooks/guard.json, preToolUse). Input on stdin:
      {"toolName": "bash", "toolArgs": {"command": "..."}, ...}   (toolArgs may be a JSON string)
    A denial is printed as
      {"permissionDecision": "deny", "permissionDecisionReason": "..."}

Anything not denied exits 0 with no output, which leaves the runtime's normal permission flow in charge.
Input that cannot be parsed, or a tool call with no shell command in it, is not judged here.

The rules, numbered so other files can cite them (fleet/registers/capabilities.md does):
  DENY[0] force-push       git push --force / -f / --force-with-lease / +refspec
  DENY[1] reset --hard     git reset --hard
  DENY[2] test deselection pytest -k / -m / --deselect / --ignore / --ignore-glob / -p no:<plugin>
  DENY[3] outbound send    curl/wget/Invoke-WebRequest writes to a non-local host, mail/sendmail/mailx/mutt,
                           Send-MailMessage, gh issue|pr comment, gh pr review, gh issue create,
                           gh api with a write method or fields

These are string checks on the command line, not a sandbox. They stop the ordinary way of doing each
thing; they do not stop a determined workaround (a script file that does the same). Outbound writes to
the network are the one rule that should also be enforced where the send happens -- see docs/hosted-runners.md.
"""
import json
import re
import shlex
import sys

RULES = {
    0: "force-push rewrites shared history",
    1: "reset --hard discards work that has no other copy",
    2: "deselecting tests hides failures; run the whole suite, or name a test file",
    3: "outbound sends are drafts only; write the message to drafts/ for a human to send",
}

LOCAL_HOSTS = ("localhost", "127.0.0.1", "[::1]", "0.0.0.0")
SEPARATORS = re.compile(r"&&|\|\||[;|\n]")
WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def tokens(segment):
    try:
        return shlex.split(segment, posix=True)
    except ValueError:
        return segment.split()


def strip_prefix(toks):
    """Drop env assignments, sudo/env/command wrappers, and a leading `python -m`."""
    i = 0
    while i < len(toks):
        t = toks[i]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t) or t in ("sudo", "env", "command", "exec", "&"):
            i += 1
            continue
        break
    toks = toks[i:]
    if len(toks) >= 3 and re.match(r"^(python[0-9.]*|py)(\.exe)?$", toks[0]) and toks[1] == "-m":
        toks = toks[2:]
    return toks


def base(word):
    return re.split(r"[\\/]", word)[-1].lower().removesuffix(".exe")


def git_args(toks):
    """Return (subcommand, args) for a git invocation, skipping global options like -C and -c."""
    i = 1
    while i < len(toks) and toks[i].startswith("-"):
        i += 2 if toks[i] in ("-C", "-c", "--git-dir", "--work-tree") else 1
    return (toks[i], toks[i + 1:]) if i < len(toks) else ("", [])


def is_external(url):
    m = re.match(r"^(?:[a-z]+://)?(?:[^@/]*@)?(\[[^\]]+\]|[^/:?#]+)", url, re.I)
    return bool(m) and m.group(1).lower() not in LOCAL_HOSTS


def urls(args):
    return [a for a in args if re.match(r"^(https?://|[a-z0-9-]+(\.[a-z0-9-]+)+(/|:|$))", a, re.I)]


def check_segment(segment):
    toks = strip_prefix(tokens(segment.strip()))
    if not toks:
        return None
    cmd, args = base(toks[0]), toks[1:]

    if cmd == "git":
        sub, rest = git_args(toks)
        if sub == "push" and any(
            a in ("-f", "--force", "--force-with-lease", "--force-if-includes") or a.startswith("--force-with-lease=")
            or (a.startswith("-") and not a.startswith("--") and "f" in a[1:])
            or (a.startswith("+") and len(a) > 1)
            for a in rest
        ):
            return 0
        if sub == "reset" and "--hard" in rest:
            return 1

    if cmd == "pytest" or cmd == "py.test":
        for i, a in enumerate(args):
            if a in ("-k", "-m", "--deselect", "--ignore", "--ignore-glob") or re.match(r"^(-k.|-m.|--deselect=|--ignore=|--ignore-glob=)", a):
                return 2
            if a == "-p" and i + 1 < len(args) and args[i + 1].startswith("no:"):
                return 2
            if a.startswith("-pno:"):
                return 2

    if cmd in ("mail", "mailx", "sendmail", "mutt", "send-mailmessage"):
        return 3

    if cmd == "curl":
        writes = False
        for i, a in enumerate(args):
            if a in ("-d", "--data", "--data-raw", "--data-binary", "--data-urlencode", "--json", "-F", "--form", "-T", "--upload-file") \
                    or re.match(r"^(--data[a-z-]*=|--json=|--form=|-d.|-F.)", a):
                writes = True
            if a in ("-X", "--request") and i + 1 < len(args) and args[i + 1].upper() in WRITE_METHODS:
                writes = True
            if re.match(r"^(-X|--request=)(POST|PUT|PATCH|DELETE)$", a, re.I):
                writes = True
        if writes and any(is_external(u) for u in urls(args)):
            return 3

    if cmd == "wget":
        writes = any(re.match(r"^--(post-data|post-file|body-data|body-file)", a) for a in args) or any(
            re.match(r"^--method=(POST|PUT|PATCH|DELETE)$", a, re.I) for a in args)
        if writes and any(is_external(u) for u in urls(args)):
            return 3

    if cmd in ("invoke-webrequest", "invoke-restmethod", "iwr", "irm"):
        low = [a.lower() for a in args]
        if any(a in ("-body", "-infile") for a in low) or any(
            low[i] == "-method" and i + 1 < len(low) and low[i + 1].upper() in WRITE_METHODS for i in range(len(low))
        ):
            if any(is_external(u) for u in urls(args)):
                return 3

    if cmd == "gh" and args:
        if args[0] in ("issue", "pr") and len(args) > 1 and args[1] == "comment":
            return 3
        if args[0] == "pr" and len(args) > 1 and args[1] == "review":
            return 3
        if args[0] == "issue" and len(args) > 1 and args[1] == "create":
            return 3
        if args[0] == "api":
            for i, a in enumerate(args):
                if a in ("-f", "-F", "--field", "--raw-field", "--input"):
                    return 3
                if a in ("-X", "--method") and i + 1 < len(args) and args[i + 1].upper() in WRITE_METHODS:
                    return 3
                if re.match(r"^(-X|--method=)(POST|PUT|PATCH|DELETE)$", a, re.I):
                    return 3
    return None


def check_command(command):
    """Return the DENY index for the first rule the command breaks, or None."""
    for segment in SEPARATORS.split(command or ""):
        hit = check_segment(segment)
        if hit is not None:
            return hit
    return None


def extract(payload):
    """Return (runtime, command) from either runtime's payload."""
    if "tool_name" in payload or "tool_input" in payload:
        ti = payload.get("tool_input") or {}
        return "claude", ti.get("command") if isinstance(ti, dict) else None
    args = payload.get("toolArgs")
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except ValueError:
            args = {"command": args}
    return "copilot", (args or {}).get("command") if isinstance(args, dict) else None


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    runtime, command = extract(payload if isinstance(payload, dict) else {})
    hit = check_command(command) if isinstance(command, str) else None
    if hit is None:
        return 0
    reason = f"DENY[{hit}] {RULES[hit]} (tools/hooks/guard.py)"
    if runtime == "claude":
        out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}
    else:
        out = {"permissionDecision": "deny", "permissionDecisionReason": reason}
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
