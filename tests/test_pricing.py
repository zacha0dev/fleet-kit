import pytest
from sample_app.pricing import Line, subtotal, total

LINES = [Line("a", 10.0, 2), Line("b", 5.5, 1)]


def test_subtotal():
    assert subtotal(LINES) == 25.5


def test_flat_discount():
    assert total(LINES, discount=5.5, discount_kind="flat") == 20.0


def test_discount_never_negative():
    assert total(LINES, discount=100, discount_kind="flat") == 0.0


@pytest.mark.xfail(strict=True, reason="KI-1: seeded bug for the triage demo. Remove this marker in the fix PR.")
def test_percent_discount():
    # 10% off 25.50 is 22.95 — KI-1 makes this fail on purpose
    assert total(LINES, discount=10, discount_kind="percent") == 22.95
