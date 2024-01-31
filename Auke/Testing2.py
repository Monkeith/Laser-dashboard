import dash_core_components as dcc
import dash
from dash import html
import base64
import wave
import numpy as np
import plotly.graph_objects as go

app = dash.Dash(__name__)

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

app.layout = html.Div([
    html.H1("Audio Visualisatie"),
    html.Div([
        dcc.Graph(figure=waveform_figure)
    ]),
    html.Div([
        dcc.Graph(figure=spectrum_figure)
    ]),
    html.H1("Audio afspelen"),
    html.Audio(src=f"data:audio/wav;base64,{encoded_audio}", controls=True)
])

if __name__ == "__main__":
    app.run_server(debug=True)
