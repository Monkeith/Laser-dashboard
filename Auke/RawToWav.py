from scipy.io import wavfile

# Specify the parameters of the .raw file
raw_file = 'input.raw'
sample_rate = 44100  # Example: 44.1 kHz
num_channels = 1  # 1 = Mono, 2 = Stereo

# Read the raw file
raw_data = open(raw_file, 'rb').read()

# Convert raw data to numpy array
import numpy as np
data = np.frombuffer(raw_data, dtype=np.int16)

# Reshape the data to stereo if necessary
data = data.reshape((-1, num_channels))

# Save as .wav file
output_wav = 'output.wav'
wavfile.write(output_wav, sample_rate, data)
