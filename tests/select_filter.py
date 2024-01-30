from dash import State, Input, Output, html, dcc, dash, callback
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd

app = dash.Dash(__name__)

dropdown = html.Div([
    dcc.Dropdown(['FIR','IIR','Bandpass','...'], 'FIR',id='dropdown', clearable=False),
])

app.layout = html.Div([
    dropdown,
    html.Div(id='filter-type'),
])

@callback(
    Output('filter-type','children'),
    Input('dropdown','value')
)

def update_filter(value):
    return f'You have selected {value}'

if __name__ == '__main__':
    app.run_server(debug=True)