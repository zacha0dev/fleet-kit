---
name: release-checklist
description: Prepare a release as an unchecked checklist with exact commands for a human to run. Use when asked to cut, prepare, or plan a release.
---
# Release checklist

Produce this, with every box unchecked and the real values filled in:

```
Release vX.Y.Z — prepared <date>
[ ] Tests green on main:            <command>   → <paste summary>
[ ] CHANGELOG has an [X.Y.Z] block: <path>
[ ] Version bumped:                 <file:line>
[ ] Tag:                            git tag -a vX.Y.Z -m "vX.Y.Z"
[ ] Push tag:                       git push origin vX.Y.Z
[ ] Release notes drafted:          <path to draft>
```

## Rules
- The agent prepares; the human runs the tag and push lines.
- Version comes from the changelog: any `Removed` or breaking `Changed` → major; `Added` → minor; only `Fixed` → patch.
