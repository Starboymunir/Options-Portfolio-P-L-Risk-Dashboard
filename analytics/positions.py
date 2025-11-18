"""Portfolio level analytics functions."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Iterable, List

import pandas as pd

from .utils import calc_pnl, money, sum_decimals


@dataclass
class PositionMetric:
    symbol: str
    underlying: str
    quantity: int
    pnl: Decimal
    delta: Decimal
    gamma: Decimal
    theta: Decimal
    vega: Decimal


def dataframe_from_positions(positions: Iterable[Dict]) -> pd.DataFrame:
    rows = []
    for pos in positions:
        pnl = calc_pnl(pos["quantity"], pos.get("avg_price", 0), pos.get("mark_price", 0))
        rows.append(
            {
                "symbol": pos["symbol"],
                "underlying": pos["underlying"],
                "quantity": pos["quantity"],
                "pnl": pnl,
                "delta": money(pos.get("delta", 0)),
                "gamma": money(pos.get("gamma", 0)),
                "theta": money(pos.get("theta", 0)),
                "vega": money(pos.get("vega", 0)),
            }
        )
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=["symbol", "underlying", "quantity", "pnl", "delta", "gamma", "theta", "vega"])
    return df


def aggregate_portfolio(df: pd.DataFrame) -> Dict[str, Decimal]:
    if df.empty:
        zero = Decimal("0")
        return {"total_pnl": zero, "delta": zero, "gamma": zero, "theta": zero, "vega": zero}

    totals = {
        "total_pnl": sum_decimals(df["pnl"].tolist()),
        "delta": sum_decimals(df["delta"].tolist()),
        "gamma": sum_decimals(df["gamma"].tolist()),
        "theta": sum_decimals(df["theta"].tolist()),
        "vega": sum_decimals(df["vega"].tolist()),
    }
    return totals


def pnl_by_underlying(df: pd.DataFrame) -> List[Dict[str, Decimal]]:
    if df.empty:
        return []
    grouped = df.groupby("underlying")
    results = []
    for underlying, gdf in grouped:
        results.append({"underlying": underlying, "total_pnl": sum_decimals(gdf["pnl"].tolist())})
    return results
