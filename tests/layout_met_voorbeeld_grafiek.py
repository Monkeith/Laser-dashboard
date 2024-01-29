import dash
from dash import State, Input, Output, html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])

# Text field
def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

# Data
df = px.data.iris()

app.layout = html.Div([
     dbc.Card(
         dbc.CardBody([
             dbc.Row(
                 html.H1('Lasermicrofoon', style={'fontsize': 40, 'textAlign':'center'})
             ),
             html.Hr(),
             dbc.Row([
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    drawFigure()
                ], width=3 ),
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    dbc.DropdownMenu([
                        dbc.DropdownMenuItem('FIR'),
                        dbc.DropdownMenuItem('IIR'),
                        dbc.DropdownMenuItem('...'),
                    ])
                ])
             ]),
             html.Hr(),
             
             dbc.Row([
                 dbc.Col([
                     drawFigure()
                 ], width=6),
                 dbc.Col([
                    drawFigure()
                 ], width=6),
             ]),
         ]),
     ),
    html.Div([
        dbc.Button(id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            children=[
                dbc.Label("Voer gewenste frequentie in:"),
                dbc.Input(
                    id= 'frequency-input',
                    type='number',
                    value=330,
                    min=1,
                    max=20000,
                    step=1,
                    placeholder='Frequentie'
                    ),

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
            title="Geluiden",
            is_open=False,
        ),  
    ])
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
