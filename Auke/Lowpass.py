from scipy.signal import butter, filtfilt

class LowpassFilter:
    def __init__(self, sampling_time, cutoff_frequency):
        self.sampling_time = sampling_time
        self.cutoff_frequency = cutoff_frequency

    def apply(self, data):
        sampling_frequency = 1 / self.sampling_time
        nyquist_frequency = 0.5 * sampling_frequency
        normalized_cutoff_frequency = self.cutoff_frequency / nyquist_frequency
        order = 5  # Orde van de filter (kan worden aangepast)

        # Controleer of de genormaliseerde afsnijfrequentie binnen het bereik [0, 1] ligt
        if normalized_cutoff_frequency >= 1:
            raise ValueError("Cutoff frequency must be less than half the sampling frequency.")

        # Bereken de filtercoëfficiënten
        b, a = butter(order, normalized_cutoff_frequency, btype='low', analog=False)

        # Filter de gegevens
        filtered_data = filtfilt(b, a, data)

        return filtered_data
