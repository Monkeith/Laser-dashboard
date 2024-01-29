import dash
import secrets
from dash import Input, Output, html
import dash_bootstrap_components as dbc
import psycopg2
import pandas as pd
import requests

# Functie om geluidsgegevens van de ESP32 te ontvangen
def receive_sound_data_from_esp32():
    try:
        response = requests.get("http://esp32_ip_address:port/sound_data")  # Vervang esp32_ip_address en port door de juiste waarden
        data = response.json()
        return data
    except Exception as e:
        print("Error while receiving sound data from ESP32:", e)
        return None

# Functie om geluidsgegevens in de database op te slaan
def save_sound_data_to_database(sound_data):
    try:
        conn = psycopg2.connect(
            dbname=secrets.DATABASE_NAME,
            user=secrets.DATABASE_USER,
            password=secrets.DATABASE_PASSWORD,
            host=secrets.DATABASE_HOST,
            port=secrets.DATABASE_PORT,
        )
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO sound_data_table (timestamp_column, sound_level)
            VALUES (%s, %s);
        """, (sound_data['timestamp'], sound_data['sound_level']))

        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print("Error while saving sound data to database:", e)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Define layout of the dashboard
app.layout = html.Div([
    html.H1("Sound Data Dashboard"),
    html.Div(id='live-update-text'),
])

# Callback function to update the dashboard with live sound data
@app.callback(Output('live-update-text', 'children'), Input('interval-component', 'n_intervals'))
def update_dashboard(n):
    sound_data = receive_sound_data_from_esp32()
    if sound_data:
        save_sound_data_to_database(sound_data)
        return f"Received sound data from ESP32: {sound_data}"
    else:
        return "Failed to receive sound data from ESP32"

if __name__ == '__main__':
    app.run_server(debug=True)
