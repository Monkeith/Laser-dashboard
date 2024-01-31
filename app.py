import dash
from dash import State, Input, Output, html, dcc
import base64
import wave
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import time
import dash_daq as daq
import plotly.graph_objects as go

SAMPLE_RATE = 44100
SAMPLE_TIME = 1 / SAMPLE_RATE

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Audio-bestand
audio_file = "C:/Users/Auke de Haan/Desktop/sample-6s.wav"

# Inhoud van het audiobestand omzetten naar base64
encoded_audio = base64.b64encode(open(audio_file, "rb").read()).decode()

# Functie om audio te lezen en golfvormgegevens te verkrijgen
def read_audio_waveform(file_path):
    with wave.open(file_path, 'rb') as wf:
        # Aantal frames in het audiobestand
        num_frames = wf.getnframes()

        # Lees de audiogegevens als een reeks frames
        audio_data = wf.readframes(num_frames)

        # Converteer de ruwe binair gecodeerde audio naar een numpy-array van integers
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # Bepaal de tijd-as (in seconden) voor de golfvormgegevens
        sample_rate = wf.getframerate()
        duration = num_frames / sample_rate
        time_axis = np.linspace(0, duration, num=len(audio_array))

        return time_axis, audio_array, sample_rate


# Golfvormgegevens van het audiobestand verkrijgen
time_values, audio_values, sample_rate = read_audio_waveform(audio_file)

# Golfvormgrafiek maken
waveform_figure = go.Figure()
waveform_figure.add_trace(go.Scatter(x=time_values, y=audio_values, mode='lines'))
waveform_figure.update_layout(title="Waveform van het audiobestand",
                              xaxis_title="Tijd (s)",
                              yaxis_title="Amplitude")

# Functie om het frequentiespectrum te berekenen met behulp van de FFT
def calculate_frequency_spectrum(audio_data, sample_rate):
    n = len(audio_data)
    fft_result = np.fft.fft(audio_data)
    magnitude = np.abs(fft_result)
    frequencies = np.fft.fftfreq(n, d=1/sample_rate)
    return frequencies[:n//2], magnitude[:n//2]

# Bereken het frequentiespectrum van de audiogegevens
frequencies, magnitude = calculate_frequency_spectrum(audio_values, sample_rate)

# Grafiek voor het frequentiespectrum maken
spectrum_figure = go.Figure()
spectrum_figure.add_trace(go.Scatter(x=frequencies, y=magnitude, mode='lines'))
spectrum_figure.update_layout(title="Frequentiespectrum van het audiobestand",
                              xaxis_title="Frequentie (Hz)",
                              yaxis_title="Magnitude")


def drawFigure():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)',
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
                html.H1('Lasermicrofoon', style={'fontsize': 40, 'textAlign': 'center'})
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
                ], width=3),
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    html.Div([
                        dcc.Dropdown(
                            id='Filter1',
                            options=[
                                {'label': 'Bandpass', 'value': 'Bandpass'},
                                {'label': 'Bandstop', 'value': 'Bandstop'},
                                {'label': 'Highpass', 'value': 'Highpass'},
                                {'label': 'Lowpass', 'value': 'Lowpass'}
                            ],
                            placeholder="Selecteer de filter",
                            style=dict(width='60%', display='inline-block', verticalAlign="middle")
                        ),
                        html.Div(id='cutoff-input1')
                    ]),
                    html.Div([
                        daq.ToggleSwitch(
                            id='my-toggle-switch1',
                            value=False
                        ),
                        html.Div(id='my-toggle-switch-output1')
                    ]),
                ]),
            ]),

            html.Div([
                    html.H1("Audio Visualisatie"),
                    html.Div([
                dcc.Graph(figure=waveform_figure)
                    ]),
                    html.Div([
            dcc.Graph(figure=spectrum_figure)
                    ]),
                html.H1("Audio afspelen"),
            html.Audio(src=f"data:audio/wav;base64,{encoded_audio}", controls=True)
                ]),
                dbc.Col([
                    html.Div([
                        dcc.Dropdown(
                            id='Filter2',
                            options=[
                                {'label': 'Bandpass', 'value': 'Bandpass'},
                                {'label': 'Bandstop', 'value': 'Bandstop'},
                                {'label': 'Highpass', 'value': 'Highpass'},
                                {'label': 'Lowpass', 'value': 'Lowpass'}
                            ],
                            placeholder="Selecteer de filter",
                            style=dict(width='60%', display='inline-block', verticalAlign="middle")
                        ),
                        html.Div(id='cutoff-input2')
                    ]),
                    html.Div([
                        daq.ToggleSwitch(
                            id='my-toggle-switch2',
                            value=False
                        ),
                        html.Div(id='my-toggle-switch-output2')
                    ]),
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
    Output('sine-wave', 'figure'),
    Input('update-interval', 'n_intervals'),
    Input('radios', 'value')
)
def update_sine_wave(n, frequency):
    t_values = np.arange(0, 0.1, SAMPLE_TIME)

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
            'plot_bgcolor': '#000000',
            'paper_bgcolor': '#83939A'
        }
    }

    return figure

@app.callback(
    Output('cutoff-input1', 'children'),
    Input('Filter1', 'value')
)
def update_cutoff_input1(filter_value):
    if filter_value in ['Highpass', 'Lowpass']:
        return html.Div([
            dcc.Input(
                id='Cutoff1',
                type='number',
                placeholder="Voer de cut-off frequentie in",
                style=dict(width='60%', display='inline-block', verticalAlign="middle")
            )
        ])
    else:
        return html.Div([
            dcc.Input(
                id='Input1',
                type='number',
                placeholder="Voer waarde 1 in",
                style=dict(width='60%', display='inline-block', verticalAlign="middle")
            ),
            dcc.Input(
                id='Input2',
                type='number',
                placeholder="Voer waarde 2 in",
                style=dict(width='60%', display='inline-block', verticalAlign="middle")
            )
        ])

@app.callback(
    Output('my-toggle-switch-output1', 'children'),
    Input('my-toggle-switch1', 'value')
)
def update_output1(value):
    status = "aan" if value else "uit"
    return f'Filter is: {status}'

@app.callback(
    Output('cutoff-input2', 'children'),
    Input('Filter2', 'value')
)
def update_cutoff_input2(filter_value):
    if filter_value in ['Highpass', 'Lowpass']:
        return html.Div([
            dcc.Input(
                id='Cutoff2',
                type='number',
                placeholder="Voer de cut-off frequentie in",
                style=dict(width='60%', display='inline-block', verticalAlign="middle")
            )
        ])
    else:
        return html.Div([
            dcc.Input(
                id='Input3',
                type='number',
                placeholder="Voer waarde 1 in",
                style=dict(width='60%', display='inline-block', verticalAlign="middle")
            ),
            dcc.Input(
                id='Input4',
                type='number',
                placeholder="Voer waarde 2 in",
                style=dict(width='60%', display='inline-block', verticalAlign="middle")
            )
        ])

@app.callback(
    Output('my-toggle-switch-output2', 'children'),
    Input('my-toggle-switch2', 'value')
)
def update_output2(value):
    status = "aan" if value else "uit"
    return f'Filter is: {status}'



if __name__ == "__main__":
    app.run_server(debug=True)
