"""Inventory counts with a simple reservation model."""


class OutOfStock(Exception):
    pass


class Inventory:
    def __init__(self) -> None:
        self._stock: dict[str, int] = {}

    def add(self, sku: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._stock[sku] = self._stock.get(sku, 0) + qty

    def reserve(self, sku: str, qty: int) -> int:
        have = self._stock.get(sku, 0)
        if have < qty:
            raise OutOfStock(f"{sku}: have {have}, need {qty}")
        self._stock[sku] = have - qty
        return self._stock[sku]

    def level(self, sku: str) -> int:
        return self._stock.get(sku, 0)
