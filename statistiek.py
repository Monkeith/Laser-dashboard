import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def analyze_audio_chunk(sample_rate, chunk, frequencies, ondergrens, bovengrens, target_frequency, tolerance_frequency):
    # FFT uitvoeren
    fft_result = np.fft.fft(chunk)
    magnitude = np.abs(fft_result)

    # Bepaal de index van de laagste frequentie die groter is dan 100 Hz
    lower_limit_index = np.argmax(frequencies > ondergrens)

    # Bepaal de index van de hoogste frequentie die kleiner is dan 20000 Hz
    upper_limit_index = np.argmax(frequencies > bovengrens)

    # Maak een nieuwe plot en plot de grafiek voor het huidige chunk
    plt.clf()
    plt.plot(frequencies[lower_limit_index:upper_limit_index], 20 * np.log10(magnitude[lower_limit_index:upper_limit_index]))  # Omzetting naar dB-schaal

    # Definieer limieten voor ruis
    lower_limit = target_frequency - tolerance_frequency
    upper_limit = target_frequency + tolerance_frequency

    # Teken het achtergrondgebied voor ruis
    plt.axvspan(lower_limit, upper_limit, color='gray', alpha=0.3, label=f'Frequentie tolerantie: {lower_limit} - {upper_limit} Hz')

    # Ingevoerde frequentie markeren op de grafiek
    frequency_index = np.abs(frequencies - target_frequency).argmin()
    plt.axvline(x=target_frequency, color='r', linestyle='--', label=f'Ingevoerde frequentie: {target_frequency} Hz', zorder=0)

    # Bereken ruis door totale magnitude te verminderen met signaalmagnitude binnen het frequentiebereik
    total_power = np.sum(magnitude[lower_limit_index:upper_limit_index])
    noise_power = total_power - np.sum(magnitude[(frequencies >= lower_limit) & (frequencies <= upper_limit)])
    noise_percentage = (noise_power / total_power) * 100

    plt.text(0.1, 0.85, f"Percentage ruis: {noise_percentage:.2f}%", transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

    plt.legend()
    plt.title('Noise-analyse van het WAV-bestand')
    plt.xlabel('Frequentie (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True)
    plt.draw()
    plt.pause(0.1)

def read_audio_in_chunks(wav_file, chunk_size):
    sample_rate, data = wavfile.read(wav_file)
    num_chunks = len(data) // chunk_size

    for i in range(num_chunks):
        yield sample_rate, data[i * chunk_size : (i + 1) * chunk_size]

def main():
    # Invoer WAV-bestand
    wav_file = r"untitled.wav"

    # Parameters voor het lezen in chunks
    chunk_size = 44100

    # Maak een generator voor het lezen van audio in chunks
    audio_generator = read_audio_in_chunks(wav_file, chunk_size)

    # Inlezen van het eerste chunk
    sample_rate, first_chunk = next(audio_generator)

    # FFT uitvoeren voor het eerste chunk
    frequencies = np.fft.fftfreq(len(first_chunk), 1 / sample_rate)

    ondergrens = 100
    bovengrens = 20000

    # Definieer limieten voor ruis
    tolerance_frequency = 100  # Tolerantie van 50 Hz aan beide kanten van de doelfrequentie
    target_frequency = 200  # Voorbeeldfrequentie

    # Analyseer het eerste chunk
    analyze_audio_chunk(sample_rate, first_chunk, frequencies, ondergrens, bovengrens, target_frequency, tolerance_frequency)

    # Maak een animatie
    for sample_rate, audio_chunk in audio_generator:
        analyze_audio_chunk(sample_rate, audio_chunk, frequencies, ondergrens, bovengrens, target_frequency, tolerance_frequency)

    plt.ioff()  # Turn off interactive mode after the loop
    plt.show()

main()
