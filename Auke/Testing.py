import dash
from dash import html
import base64

app = dash.Dash(__name__)

# Audio-bestand
audio_file = "C:/Users/Auke de Haan/Desktop/sample-6s.wav"

# Inhoud van het audiobestand omzetten naar base64
encoded_audio = base64.b64encode(open(audio_file, "rb").read()).decode()

app.layout = html.Div([
    html.H1("Audio afspelen"),
    html.Audio(src=f"data:audio/wav;base64,{encoded_audio}", controls=True)
])

if __name__ == "__main__":
    app.run_server(debug=True)
