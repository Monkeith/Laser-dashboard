import dash
from dash import State, Input, Output, html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

sidebar = html.Div([
    dbc.Button(id="open-offcanvas", n_clicks=0),
    dbc.Offcanvas(
        children=[
            html.H2("Geluiden"),
            dbc.ListGroup([
                dbc.ListGroupItem("300Hz", id="300Hz", n_clicks=0, action=True),
                dbc.ListGroupItem("400Hz", id="400Hz", n_clicks=0, action=True),
                dbc.ListGroupItem("500Hz", id="500Hz", n_clicks=0, action=True),
                dbc.ListGroupItem("600Hz", id="600Hz", n_clicks=0, action=True),
                dbc.ListGroupItem("700Hz", id="700Hz", n_clicks=0, action=True),
                dbc.ListGroupItem("800Hz", id="800Hz", n_clicks=0, action=True),
            ]),
        ],
        id="offcanvas",
        title="Title",
        is_open=False,
    ),
])

content = html.Div([
    dbc.Col(),
    dbc.Col()
])
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Lasermicrofoon", style={'fontSize': 40, 'textAlign': 'center'}))
    ]),

    html.Hr(),  # Horizontal line

    content,sidebar
])

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run_server(debug=False)
