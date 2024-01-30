import dash
import mysecrets
from dash import dcc, html
from dash.dependencies import Input, Output
import psycopg2
import numpy as np
import wave
import struct

# Verbindingsgegevens


# Functie om audio uit de database te halen
def get_audio_from_database():
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

        # Voer een SQL-query uit om de audio op te halen
        cur.execute("SELECT audio_data FROM audio_table;")
        rows = cur.fetchall()

        # Haal de audio data op
        audio_data = b''.join([row[0] for row in rows])

        print("Audio succesvol opgehaald uit de database.")
        return audio_data

    except psycopg2.Error as e:
        print("Error:", e)
        return None

    finally:
        # Sluit de cursor en de verbinding
        cur.close()
        conn.close()

# Functie om audio op te slaan als .wav-bestand
def save_audio_from_database(audio_data, filename, sample_rate):
    if audio_data:
        wave_file = wave.open(filename, 'w')
        wave_file.setparams((1, 2, sample_rate, len(audio_data), 'NONE', 'not compressed'))
        wave_file.writeframes(audio_data)
        wave_file.close()

        print("Audio succesvol opgeslagen als", filename)
    else:
        print("Geen audio gevonden in de database.")

# Haal audio op uit de database
audio_from_db = get_audio_from_database()

# Sla de opgehaalde audio op als .wav-bestand
save_audio_from_database(audio_from_db, "../.venv/audio_from_db.wav", 44100)

# Initialiseer de Dash app
app = dash.Dash(__name__)

# Layout van de app
app.layout = html.Div([
    html.H1("Audiovisualisatie"),
    html.Audio(src='../.venv/audio_from_db.wav', controls=True),
])

if __name__ == '__main__':
    app.run_server(debug=True)
