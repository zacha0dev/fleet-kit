# Known issues

| Id | Symptom | Where | Status | Source |
|----|---------|-------|--------|--------|
| KI-1 | `pricing.total()` applies a percentage discount as a flat amount when `discount_kind="percent"`: 10% off 25.50 returns 15.5, not 22.95 | `sample_app/pricing.py:22` | open, seeded for the triage demo | `python -m pytest -q --runxfail tests/test_pricing.py` → `1 failed, 3 passed` (`assert 15.5 == 22.95`). The test is marked `xfail(strict=True)`, so the plain run reports `3 passed, 1 xfailed` and CI stays green; the fix removes the marker. Measured 2026-09-26. |
