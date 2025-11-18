"""Dash callbacks for interactive components."""
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from typing import List

import pandas as pd
import plotly.express as px
from dash import Input, Output, dash_table, html

from analytics.positions import aggregate_portfolio, dataframe_from_positions, pnl_by_underlying
from tasty_client import TastyClient


# In a production app you'd use dependency injection or caching.
CLIENT = None


def get_client() -> TastyClient:
    global CLIENT
    if CLIENT is None:
        CLIENT = TastyClient()
    return CLIENT


def _mock_positions() -> List[dict]:
    """Used if the API is unavailable so the Dash app can still render."""
    return [
        {
            "symbol": "AAPL",
            "underlying": "AAPL",
            "quantity": 2,
            "avg_price": Decimal("145.15"),
            "mark_price": Decimal("150.05"),
            "delta": Decimal("0.45"),
            "gamma": Decimal("0.02"),
            "theta": Decimal("-0.01"),
            "vega": Decimal("0.12"),
        },
        {
            "symbol": "SPY",
            "underlying": "SPY",
            "quantity": -1,
            "avg_price": Decimal("430.00"),
            "mark_price": Decimal("425.50"),
            "delta": Decimal("-0.50"),
            "gamma": Decimal("0.01"),
            "theta": Decimal("0.03"),
            "vega": Decimal("-0.05"),
        },
    ]


def register_callbacks(app):
    @app.callback(
        Output("kpi-total-pnl", "children"),
        Output("kpi-delta", "children"),
        Output("kpi-gamma", "children"),
        Output("kpi-theta", "children"),
        Output("kpi-vega", "children"),
        Output("equity-curve", "figure"),
        Output("pnl-by-underlying", "figure"),
        Output("positions-table", "children"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("underlying-filter", "value"),
    )
    def update_dashboard(start_date, end_date, underlying_filter):  # pragma: no cover - Dash callback
        del end_date  # not used yet but part of API
        try:
            client = get_client()
            positions = client.get_positions()
        except Exception:
            positions = _mock_positions()

        if underlying_filter:
            positions = [pos for pos in positions if pos["underlying"] == underlying_filter]

        df = dataframe_from_positions(positions)
        totals = aggregate_portfolio(df)
        pnl_underlying = pnl_by_underlying(df)

        if df.empty:
            equity_fig = px.line(title="Equity Curve", labels={"value": "P&L"})
            pnl_fig = px.bar(title="P&L by Underlying")
            table = html.Div("No positions available")
        else:
            df_equity = pd.DataFrame(
                {
                    "date": [date.today() - timedelta(days=i) for i in range(len(df))],
                    "equity": [float(totals["total_pnl"]) for _ in range(len(df))],
                }
            )
            equity_fig = px.line(df_equity, x="date", y="equity", title="Equity Curve")
            pnl_fig = px.bar(pnl_underlying, x="underlying", y="total_pnl", title="P&L by Underlying")
            table = dash_table.DataTable(
                columns=[{"name": col, "id": col} for col in df.columns],
                data=df.to_dict("records"),
                filter_action="native",
                sort_action="native",
                style_table={"overflowX": "auto"},
            )

        return (
            f"${totals['total_pnl']}",
            str(totals["delta"]),
            str(totals["gamma"]),
            str(totals["theta"]),
            str(totals["vega"]),
            equity_fig,
            pnl_fig,
            table,
        )
