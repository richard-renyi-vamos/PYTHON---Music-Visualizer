import tkinter as tk
from tkinter import filedialog, ttk
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MusicVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Visualizer")

        # Variable to store the selected color map
        self.cmap_var = tk.StringVar(value='viridis')

        # Variable to store the selected scale (log or linear)
        self.scale_var = tk.StringVar(value='Logarithmic')

        # Create a button to load the audio file
        self.load_button = tk.Button(root, text="Load Audio File", command=self.load_audio)
        self.load_button.pack(pady=10)

        # Create a label and combobox for color map selection
        self.cmap_label = tk.Label(root, text="Color Map")
        self.cmap_label.pack()
        self.cmap_combobox = ttk.Combobox(root, textvariable=self.cmap_var)
        self.cmap_combobox['values'] = plt.colormaps()  # Populate with available colormaps
        self.cmap_combobox.pack(pady=5)

        # Create a label and combobox for scale selection
        self.scale_label = tk.Label(root, text="Scale")
        self.scale_label.pack()
        self.scale_combobox = ttk.Combobox(root, textvariable=self.scale_var)
        self.scale_combobox['values'] = ['Logarithmic', 'Linear']
        self.scale_combobox.pack(pady=5)

        # Create a button to refresh the spectrogram with new settings
        self.refresh_button = tk.Button(root, text="Refresh Spectrogram", command=self.refresh_spectrogram)
        self.refresh_button.pack(pady=10)

        # Placeholder for audio data and canvas
        self.y = None
        self.sr = None
        self.canvas = None

    def load_audio(self):
        # Open a file dialog to select an audio file
        audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.flac")])
        
        if audio_path:
            # Load the audio file
            self.y, self.sr = librosa.load(audio_path)

            # Generate the initial spectrogram
            self.refresh_spectrogram()

    def refresh_spectrogram(self):
        if self.y is None:
            return  # Do nothing if no audio is loaded

        # Compute the mel spectrogram
        mel_spec = librosa.feature.melspectrogram(y=self.y, sr=self.sr)

        # Convert to decibels (logarithmic scale) or leave as power (linear scale)
        if self.scale_var.get() == 'Logarithmic':
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        else:
            mel_spec_db = mel_spec

        # Create a figure for the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Display the mel spectrogram with the selected color map
        img = librosa.display.specshow(mel_spec_db, sr=self.sr, x_axis='time', y_axis='mel', ax=ax, cmap=self.cmap_var.get())

        # Add a colorbar
        fig.colorbar(img, ax=ax, format='%+2.0f dB')

        # Set the title
        ax.set_title(f'Mel Spectrogram ({self.scale_var.get()} Scale)')

        # Remove the old canvas if it exists
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

        # Create a canvas to display the plot in the Tkinter window
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

# Create the Tkinter window
root = tk.Tk()

# Create the MusicVisualizerApp object
app = MusicVisualizerApp(root)

# Run the application
root.mainloop()
