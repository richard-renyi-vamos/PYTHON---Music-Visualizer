import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load the audio file
audio_path = 'path_to_your_audio_file.mp3'
y, sr = librosa.load(audio_path)

# Compute the mel spectrogram
mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)

# Convert to decibels
mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

# Create a figure and axes
plt.figure(figsize=(12, 8))

# Display the mel spectrogram
librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')

# Add a colorbar
plt.colorbar(format='%+2.0f dB')

# Set the title
plt.title('Mel Spectrogram')

# Show the plot
plt.show()
