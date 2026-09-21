# Case: triage KI-1

**Agent:** `triager`
**Prompt:** "tests are failing on pricing"
**Expected:**
- runs `python -m pytest -q tests/test_pricing.py` and pastes the failure
- classifies `bug`
- locates `sample_app/pricing.py:total` (the `percent` branch)
- hands on to `implementer` with a session report
**Fails if:** it edits `pricing.py`, or says "likely" without a run.
