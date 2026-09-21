import pytest
from sample_app.inventory import Inventory, OutOfStock


def test_add_and_level():
    inv = Inventory(); inv.add("a", 3)
    assert inv.level("a") == 3


def test_reserve_reduces_level():
    inv = Inventory(); inv.add("a", 3)
    assert inv.reserve("a", 2) == 1


def test_reserve_more_than_stock_raises():
    inv = Inventory(); inv.add("a", 1)
    with pytest.raises(OutOfStock):
        inv.reserve("a", 2)
