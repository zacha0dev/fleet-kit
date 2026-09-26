# Security

Please report a security problem privately, through GitHub's private vulnerability reporting: the **Security** tab of this repository, then **Report a vulnerability**. Do not open a public issue for it.

Useful to include: the file and line, what an agent or hook could be made to do, and the steps to show it.

In scope: anything that lets an agent get past `tools/hooks/guard.py`, the tools allowlist in an agent file, or the drafts-only rule; and anything in `deploy/` that would weaken the identity or network rules it describes. The guard matches command lines and is documented as not stopping every workaround; a bypass is still worth reporting if it looks like an ordinary command.

This is a personal project maintained in spare time. Reports are read, but there is no response-time commitment.
