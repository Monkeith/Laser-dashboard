import socketio
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import struct
import numpy as np

# Initialiseer de Dash-app
app = dash.Dash(__name__)

# Initialiseer de lijst om de ontvangen gegevens op te slaan
received_data = []

# Initialiseer de Socket.IO-client
sio = socketio.Client()

# Event handler voor wanneer de verbinding tot stand komt
@sio.event
def connect():
    print('Verbonden met de server')

# Event handler voor wanneer een bericht wordt ontvangen met het event "LIVE_CHUNK"
@sio.on("LIVE_CHUNK")
def live_chunk(data):
    # Formaat specifier voor de struct.unpack functie
    # 'B' staat voor unsigned char (1 byte)
    # format_specifier = 'B' * (len(data))
    #
    # # Unpacken van de byte-array naar een lijst van integers
    # data = struct.unpack(format_specifier, data)
    received_data.append(((bytearray(data))))

    if (len(received_data) > 10): received_data.pop(0)

    # Zet de gegevens om naar een NumPy-array en voeg ze toe aan de lijst
    # received_data.append(np.array(data, dtype=np.uint16))

# Event handler voor wanneer de verbinding wordt verbroken
@sio.event
def disconnect():
    print('Verbinding verbroken met de server')

# Verbind met de Socket.IO-server
sio.connect('http://192.168.2.8:5003')

# Definieer de layout van de Dash-app
app.layout = html.Div([
    html.H1("Live Data Dashboard"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=30,  # interval in milliseconds
        n_intervals=0
    )
])

# Callback om de grafiek bij te werken met de ontvangen gegevens
@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]  # Dit interval wordt gebruikt om de grafiek periodiek bij te werken
)
def update_graph(n):

    # if len(received_data) < 1: return go.Figure(data=go.Scatter(x=[], y=[], mode='lines'))
    # Bepaal de lengte van de x-waarden
    x_length = 16384*2

    # Maak een lijst met x-waarden en y-waarden van de ontvangen gegevens
    # x_values = [i for i in range(x_length)]
    x_values = np.linspace(0, x_length/ (1/44000), num=x_length)
    y_values = []
    for y in received_data:
        for x in y:
            y_values.append((x))


    # y_values = [datum for gegevens in received_data for datum in gegevens]

    # Als de lengte van de x-waarden groter is dan 1000, houd dan alleen de laatste 1000 waarden
    if x_length > 1000:
        x_values = x_values[-1000::]
        y_values = y_values[-1000::]

    # Maak een lijnplot van de gegevens
    fig = go.Figure(data=go.Scatter(x=x_values, y=y_values, mode='lines'))

    # Zet de y-as vast tussen 0 en 256
    fig.update_yaxes(range=[-30, 300])

    # Voeg titels en labels toe
    fig.update_layout(title="Live Data Plot", xaxis_title="Tijd", yaxis_title="Waarde")
    # received_data.pop(0)
    return fig

# Start de Dash-applicatie
if __name__ == '__main__':
    app.run_server(debug=True)
