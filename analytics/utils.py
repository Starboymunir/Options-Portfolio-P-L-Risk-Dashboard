"""Utility helpers for financial calculations using Decimal."""
from __future__ import annotations

from decimal import Decimal, getcontext
from typing import Iterable

getcontext().prec = 28


def money(value) -> Decimal:
    """Convert numeric/str to Decimal without introducing float error."""
    if value is None:
        return Decimal("0")
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def calc_pnl(quantity, avg_price, mark_price) -> Decimal:
    q = Decimal(quantity)
    ap = money(avg_price)
    mp = money(mark_price)
    return q * (mp - ap)


def sum_decimals(values: Iterable[Decimal]) -> Decimal:
    total = Decimal("0")
    for value in values:
        total += money(value)
    return total
