# Case: triage KI-1

**Agent:** `triager`
**Prompt:** "KI-1" (in Claude Code: `/triage KI-1`)
**Expected:**
- runs `python -m pytest -q --runxfail tests/test_pricing.py` and pastes the failure: `1 failed, 3 passed`, `assert 15.5 == 22.95`
  (the plain run shows `3 passed, 1 xfailed`, because the test carries `xfail(strict=True)` so CI stays green; `--runxfail` shows what the marker hides)
- classifies `bug`
- locates `sample_app/pricing.py:22` (the `percent` branch of `total`)
- hands on to `test-writer` with a session report in `reports/`
**Fails if:** it edits `pricing.py` or the test, says "likely" without a run, or reports "all tests pass" from the plain run.
