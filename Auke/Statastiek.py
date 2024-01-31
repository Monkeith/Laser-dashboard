import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class WavFileAnalyzer:
    def __init__(self, wav_file):
        self.wav_file = wav_file

    def analyze(self):
        sample_rate, data = wavfile.read(self.wav_file)

        # FFT uitvoeren
        fft_result = np.fft.fft(data)
        frequencies = np.fft.fftfreq(len(data), 1 / sample_rate)
        magnitude = np.abs(fft_result)

        # Definieer limieten voor ruis
        tolerance_frequency = 50  # Tolerantie van 50 Hz aan beide kanten van de doelfrequentie
        target_frequency = 200  # Voorbeeldfrequentie

        lower_limit = target_frequency - tolerance_frequency
        upper_limit = target_frequency + tolerance_frequency

        # Bereken ruis door totale magnitude te verminderen met signaalmagnitude
        frequency_index = np.abs(frequencies - target_frequency).argmin()
        total_power = np.sum(magnitude[(frequencies >= lower_limit) & (frequencies <= upper_limit)])
        noise_power = total_power - magnitude[frequency_index]
        noise_percentage = (noise_power / total_power) * 100

        return frequencies, magnitude, noise_percentage

    def plot_analysis(self):
        frequencies, magnitude, noise_percentage = self.analyze()

        # Grafiek plotten
        plt.figure(figsize=(12, 6))
        plt.plot(frequencies[:len(frequencies)//2], 20 * np.log10(magnitude[:len(magnitude)//2]))  # Omzetting naar dB-schaal
        plt.title('Noise-analyse van het WAV-bestand')
        plt.xlabel('Frequentie (Hz)')
        plt.ylabel('Magnitude (dB)')
        plt.grid(True)

        # Definieer limieten voor ruis
        tolerance_frequency = 50  # Tolerantie van 50 Hz aan beide kanten van de doelfrequentie
        target_frequency = 200  # Voorbeeldfrequentie

        lower_limit = target_frequency - tolerance_frequency
        upper_limit = target_frequency + tolerance_frequency

        # Teken het achtergrondgebied voor ruis
        plt.axvspan(lower_limit, upper_limit, color='gray', alpha=0.3, label=f'Frequentie tolerantie: {lower_limit} - {upper_limit} Hz')

        # Ingevoerde frequentie markeren op de grafiek
        frequency_index = np.abs(frequencies - target_frequency).argmin()
        plt.axvline(x=target_frequency, color='r', linestyle='--', label=f'Ingevoerde frequentie: {target_frequency} Hz', zorder=0)

        plt.text(0.1, 0.85, f"Percentage ruis: {noise_percentage:.2f}%", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

        plt.legend()
        plt.show()

# Gebruik van de class:
wav_file = r"C:\Users\Julian\Desktop\test.wav"
analyzer = WavFileAnalyzer(wav_file)
analyzer.plot_analysis()
