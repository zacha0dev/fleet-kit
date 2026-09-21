"""Order pricing — the small, real thing the fleet works on."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Line:
    sku: str
    unit_price: float
    qty: int


def subtotal(lines: list[Line]) -> float:
    return round(sum(l.unit_price * l.qty for l in lines), 2)


def total(lines: list[Line], discount: float = 0.0, discount_kind: str = "flat") -> float:
    """Apply a discount to the subtotal.

    discount_kind is "flat" (subtract the amount) or "percent" (subtract that percentage).
    """
    base = subtotal(lines)
    if discount_kind == "percent":
        # KI-1: this subtracts the number instead of the percentage. Seeded for the triage demo.
        return round(max(base - discount, 0.0), 2)
    return round(max(base - discount, 0.0), 2)
