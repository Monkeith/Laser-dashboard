import dash
from dash import State, Input, Output, html, dcc
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import time

SAMPLE_RATE = 44100
SAMPLE_TIME = 1/SAMPLE_RATE

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

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
                    html.Div([
                        dcc.Graph(id='sine-wave'),
                        dcc.Interval(
                            id='update-interval',
                            interval=100,
                            n_intervals=0
                        )
                    ])
                ], width=3),
                dbc.Col([
                    drawFigure()
                ], width=3 ),
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    html.Div([
                    dcc.Dropdown(['FIR','IIR','Bandpass'], 'FIR', id='dropdown', clearable=False),
                    ]),
                ]),
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
                dbc.Label("Kies gewenste frequentie"),
               html.Div([
                    dcc.RadioItems(
                        id='radios',
                        className='btn-group',
                        inputClassName='btn-group',
                        labelClassName='btn btn-outline-primary',
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
                            {'label': '1630 Hz', 'value': 1630},
                            {'label': '1760 Hz', 'value': 1760},
                            {'label': '1890 Hz', 'value': 1890},
                            {'label': '2020 Hz', 'value': 2020},
                        ],
                        value=1,
                    ),
                    html.Div(id='Output'),
                ],
                    className='radio-group',
                ),
            ],
            id="offcanvas",
            title="Geluiden",
            is_open=False,
        ),  
    ]),
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

@app.callback(
    Output('filter-type','children'),
    Input('dropdown','value')
)

def update_filter(value):
    return f'You have selected {value}'

@app.callback(
    Output('sine-wave', 'figure'),
    Input('update-interval', 'n_intervals'),
    Input('radios', 'value')
)
def update_sine_wave(n, frequency):
    t_values = np.arange(0,0.1,SAMPLE_TIME)

    current_time = time.time()
    sine_wave = np.sin(2 * np.pi * frequency * (t_values - current_time))

    figure = {
        'data': [
            {'x': t_values, 'y': sine_wave, 'type': 'line', 'name': 'Sine Wave'},
        ],
        'layout': {
            'title': f'Real-Time Sine Wave (Frequency: {frequency} Hz)',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Amplitude'},
            'plot_bgcolor':'#000000',
            'paper_bgcolor':'#83939A'
        }
    }

    return figure

if __name__ == "__main__":
    app.run_server(debug=False)
