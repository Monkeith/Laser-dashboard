import dash
import secrets
from dash import dcc, html
from dash.dependencies import Input, Output
import psycopg2
import pandas as pd
from datetime import timedelta

# Verbindingsgegevens


# Functie om de laatste 100 datapunten uit de database te halen
def get_last_100_data_points():
    try:
        # Maak verbinding met de database
        conn = psycopg2.connect(
            dbname=secrets.DATABASE_NAME,
            user=secrets.DATABASE_USER,
            password=secrets.DATABASE_PASSWORD,
            host=secrets.DATABASE_HOST,
            port=secrets.DATABASE_PORT,
        )

        # Voer een SQL-query uit om de laatste 100 datapunten op te halen
        cur = conn.cursor()
        cur.execute("SELECT * FROM your_table_name ORDER BY timestamp_column DESC LIMIT 100;")  # Laatste 100 rijen ophalen
        rows = cur.fetchall()

        # Maak een DataFrame van de resultaten
        df = pd.DataFrame(rows, columns=['timestamp', 'sound_level'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])  # Zet timestamp om naar datetime object
        return df

    except psycopg2.Error as e:
        print("Error:", e)
        return pd.DataFrame()

    finally:
        # Sluit de cursor en de verbinding
        cur.close()
        conn.close()

# Initialiseer de Dash app
app = dash.Dash(__name__)

# Layout van de app
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 500,  # Update elke halve seconde
        n_intervals=0
    )
])

# Callback functie om de grafiek te updaten met nieuwe gegevens
@app.callback(Output('live-graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph(n):
    # Haal de laatste 100 datapunten op uit de database
    df = get_last_100_data_points()

    # Verschuif de x-waarden van de datapunten
    shifted_timestamps = [df['timestamp'].max() - timedelta(seconds=i*10) for i in range(100)]

    # Maak de lijngrafiek
    fig = {
        'data': [{
            'x': shifted_timestamps,
            'y': df['sound_level'],
            'type': 'line'
        }],
        'layout': {
            'title': 'Sound Level Over Time (Last 100 Data Points)',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Sound Level'}
        }
    }
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

#Test

