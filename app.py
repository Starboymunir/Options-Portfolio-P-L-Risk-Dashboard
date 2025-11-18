"""Dash entrypoint for the tasty-portfolio-dashboard application."""
from dash import Dash

from dashboard.layout import layout
from dashboard.callbacks import register_callbacks


app = Dash(__name__, suppress_callback_exceptions=True, title="Tasty Portfolio Dashboard")
app.layout = layout
register_callbacks(app)


if __name__ == "__main__":
    app.run_server(debug=True)
