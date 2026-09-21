# Capability register

What agents may do here, which tool does it, and the evidence. Rows without evidence are removed on audit. Status is one of `allowed`, `blocked-measured`, `reported-unmeasured`.

| Capability | Tool | Layer | Evidence | Date | Status |
|------------|------|-------|----------|------|--------|
| Read any file in the repo | read / search | — | default | 2026-09-21 | allowed |
| Run tests | execute (`python -m pytest`) | — | `tools/validate_fleet.py` passes in CI | 2026-09-21 | allowed |
| Edit fleet files on `main` | edit | declaration | `.github/instructions/fleet-files.instructions.md:6` | 2026-09-21 | blocked-measured (by design; use a PR) |
| Force-push | execute | hook | `tools/hooks/guard.py` DENY[0] | 2026-09-21 | blocked-measured |
| Send a message outside the repo | any | declaration + hook | `copilot-instructions.md` "Drafts only"; `guard.py` DENY[3] | 2026-09-21 | blocked-measured (drafts only) |
| Merge, tag, release | — | declaration | `copilot-instructions.md` "Human gates" | 2026-09-21 | blocked-measured (human) |
