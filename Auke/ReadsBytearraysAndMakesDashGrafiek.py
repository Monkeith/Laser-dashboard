import dash
from dash import dcc, html
import psycopg2
import mysecrets
import plotly.graph_objs as go

# Functie om byte-array gegevens uit de database te lezen
def read_byte_arrays():
    byte_array_data = []  # Hier slaan we de byte-array gegevens op
    try:
        # Maak verbinding met de database
        conn = psycopg2.connect(
            dbname=mysecrets.DATABASE_NAME,
            user=mysecrets.DATABASE_USER,
            password=mysecrets.DATABASE_PASSWORD,
            host=mysecrets.DATABASE_HOST,
            port=mysecrets.DATABASE_PORT,
        )

        # Maak een cursor object
        cur = conn.cursor()

        # Voer een query uit om de byte-array gegevens uit de tabel te lezen
        cur.execute("SELECT byte_array FROM bytearray_table")

        # Haal de byte-array gegevens op en sla ze op
        byte_arrays = cur.fetchall()
        for row in byte_arrays:
            byte_array = row[0]
            byte_array_values = list(byte_array)
            byte_array_data.append(byte_array_values)

    except psycopg2.Error as e:
        print("Error connecting to database:", e)

    finally:
        # Sluit de cursor en de verbinding
        if cur:
            cur.close()
        if conn:
            conn.close()

    return byte_array_data

# Haal de byte-array gegevens op uit de database
byte_array_data = read_byte_arrays()

# Converteer byte-array gegevens naar een lijst van integers
byte_array_data_int = []
for byte_array_values in byte_array_data:
    byte_array_data_int.append(list(byte_array_values))

# Maak een lijngrafiek met behulp van Plotly
def create_line_chart(byte_array_data_int):
    fig = go.Figure()
    for i, byte_array_values in enumerate(byte_array_data_int):
        fig.add_trace(go.Scatter(
            x=list(range(len(byte_array_values))),
            y=byte_array_values,
            mode='lines',
            name=f'Byte Array {i+1}'
        ))
    fig.update_layout(
        title='Byte Array Grafiek',
        xaxis={'title': 'Index'},
        yaxis={'title': 'Waarde'}
    )
    return fig

# Initialiseer Dash app
app = dash.Dash(__name__)

# Layout van de Dash app
app.layout = html.Div([
    dcc.Graph(
        id='byte-array-graph',
        figure=create_line_chart(byte_array_data_int)
    )
])

# Start de Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
