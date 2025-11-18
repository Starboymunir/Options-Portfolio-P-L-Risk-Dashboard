"""Dash layout definition for the tasty portfolio dashboard."""
from __future__ import annotations

from dash import dcc, html


def kpi_card(card_id: str, title: str, value: str = "--"):
    return html.Div(
        className="kpi-card",
        children=[html.Div(title, className="kpi-title"), html.Div(value, id=card_id, className="kpi-value")],
    )


layout = html.Div(
    className="app-container",
    children=[
        html.H1("Options Portfolio Dashboard"),
        html.Div(
            className="kpi-row",
            children=[
                kpi_card("kpi-total-pnl", "Total P&L"),
                kpi_card("kpi-delta", "Delta"),
                kpi_card("kpi-gamma", "Gamma"),
                kpi_card("kpi-theta", "Theta"),
                kpi_card("kpi-vega", "Vega"),
            ],
        ),
        html.Div(
            className="filters",
            children=[
                dcc.DatePickerRange(id="date-range"),
                dcc.Dropdown(id="underlying-filter", placeholder="Filter by underlying"),
            ],
        ),
        dcc.Graph(id="equity-curve"),
        dcc.Graph(id="pnl-by-underlying"),
        html.Div(id="positions-table"),
    ],
)
