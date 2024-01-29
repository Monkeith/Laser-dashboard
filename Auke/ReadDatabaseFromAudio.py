import dash
import secrets
from dash import dcc, html
from dash.dependencies import Input, Output
import psycopg2
import numpy as np
import wave
import struct



# Functie om audio uit de database te halen
def get_audio_from_database():
    try:
        # Maak verbinding met de database
        conn = psycopg2.connect(
            dbname=secrets.DATABASE_NAME,
            user=secrets.DATABASE_USER,
            password=secrets.DATABASE_PASSWORD,
            host=secrets.DATABASE_HOST,
            port=secrets.DATABASE_PORT,
        )

        # Maak een cursor object
        cur = conn.cursor()

        # Voer een SQL-query uit om de audio op te halen
        cur.execute("SELECT audio_data FROM audio_table;")
        row = cur.fetchone()

        # Haal de audio data op
        audio_data = row[0]

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
    wave_file = wave.open(filename, 'w')
    wave_file.setparams((1, 2, sample_rate, 0, 'NONE', 'not compressed'))

    # Pak de audio data uit het byte-formaat en schrijf deze naar het .wav-bestand
    for byte_data in audio_data:
        wave_file.writeframes(struct.pack('<h', int.from_bytes(byte_data, byteorder='big', signed=True)))

    wave_file.close()

# Haal audio op uit de database
audio_from_db = get_audio_from_database()

# Sla de opgehaalde audio op als .wav-bestand
if audio_from_db:
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
