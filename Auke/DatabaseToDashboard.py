import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import psycopg2
import pandas as pd

# Connect to the database
def connect_to_db():
    conn = psycopg2.connect(
        dbname="tsdb",
        user="tsdbadmin",
        password="1uG?RrmOV7x.62",
        host="ox6uce6ozv.nddn3dnk87.tsdb.cloud.timescale.com",
        port="33993"
    )
    return conn

# Fetch sound data from database
def fetch_sound_data(conn):
    query = "SELECT timestamp_column, sound_level FROM your_table_name;"
    df = pd.read_sql(query, conn)
    return df

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Connect to the database
conn = connect_to_db()

# Define layout of the dashboard
app.layout = html.Div([
    html.H1("Sound Data Dashboard"),
    dcc.Graph(id='sound-time-series'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Update every 5 seconds
        n_intervals=0
    )
])

# Callback to update graph with new data
@app.callback(
    Output('sound-time-series', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # Fetch sound data from the database
    df = fetch_sound_data(conn)

    # Update the graph with new data
    figure = {
        'data': [
            {'x': df['timestamp_column'], 'y': df['sound_level'], 'type': 'line', 'name': 'Sound Level'}
        ],
        'layout': {
            'title': 'Sound Level Over Time'
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
