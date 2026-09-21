# Known issues

| Id | Symptom | Where | Status | Source |
|----|---------|-------|--------|--------|
| KI-1 | `pricing.total()` applies a percentage discount as a flat amount when `discount_kind="percent"` | `sample_app/pricing.py` | open — seeded for the triage demo | `tests/test_pricing.py::test_percent_discount` (marked `xfail(strict=True)` so CI stays green; the fix PR removes the marker), 2026-09-21 |
