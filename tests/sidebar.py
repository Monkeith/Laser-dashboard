import dash
from dash import State, Input, Output, html, dcc, dash, ctx, callback
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd


app = dash.Dash(__name__)

sidebar = html.Div([
    dbc.Col([
    dbc.Button(id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
           children=[
                html.Div([
                    dbc.RadioItems(
                        id='radios',
                        className='btn-group',
                        inputClassName='btn-check',
                        labelClassName='btn btn-outline-primary',
                        labelCheckedClassName='active',
                        options=[
                            {'label': '220 Hz', 'value': 200},
                            {'label': '330 Hz', 'value': 330},
                            {'label': '460 Hz', 'value': 460},
                            {'label': '590 Hz', 'value': 590},
                            {'label': '720 Hz', 'value': 720},
                            {'label': '850 Hz', 'value': 850},
                            {'label': '980 Hz', 'value': 980},
                            {'label': '1110 Hz', 'value': 1110},
                            {'label': '1240 Hz', 'value': 1240},
                            {'label': '1370 Hz', 'value': 1370},
                            {'label': '1500 Hz', 'value': 1500},
                            {'label': '1630', 'value': 1630},
                            {'label': '1760 Hz', 'value': 1760},
                            {'label': '1890 Hz', 'value': 1890},
                            {'label': '2020 Hz', 'value': 2020},
                        ],
                        value=1,
                    ),
                    html.Div(id='Output'),
                ],
                    className='radio-group',
                )
            ],
            id="offcanvas",
            title="Geluiden",
            is_open= False,
        ),]),
])

app.layout = dbc.Container([
    sidebar
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


@app.callback(Output("Output", "children"), [Input("radios", "value")])
def display_value(value):
    return f"Selected value: {value}"


if __name__ == "__main__":
    app.run_server(debug=True)