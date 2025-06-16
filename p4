import tkinter as tk
from tkinter import filedialog, ttk
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MusicVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎶 Music Visualizer")

        # Variables
        self.audio_source_var = tk.StringVar(value='File')
        self.cmap_var = tk.StringVar(value='viridis')
        self.scale_var = tk.StringVar(value='Logarithmic')
        self.view_var = tk.StringVar(value='Spectrogram')

        self.y = None
        self.sr = None
        self.canvas = None

        # Layout
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Audio Source").pack()
        ttk.Combobox(self.root, textvariable=self.audio_source_var, values=['File', 'Microphone']).pack(pady=2)

        ttk.Button(self.root, text="Load Audio", command=self.load_audio).pack(pady=5)

        ttk.Label(self.root, text="Color Map").pack()
        ttk.Combobox(self.root, textvariable=self.cmap_var, values=plt.colormaps()).pack(pady=2)

        ttk.Label(self.root, text="Scale").pack()
        ttk.Combobox(self.root, textvariable=self.scale_var, values=['Logarithmic', 'Linear']).pack(pady=2)

        ttk.Label(self.root, text="View").pack()
        ttk.Combobox(self.root, textvariable=self.view_var, values=['Spectrogram', 'Waveform']).pack(pady=2)

        ttk.Button(self.root, text="Refresh View", command=self.refresh_visualization).pack(pady=5)
        ttk.Button(self.root, text="Play Audio", command=self.play_audio).pack(pady=5)

        self.duration_label = ttk.Label(self.root, text="Duration: N/A")
        self.duration_label.pack(pady=5)

    def load_audio(self):
        audio_source = self.audio_source_var.get()

        if audio_source == 'File':
            audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.flac")])
            if audio_path:
                self.y, self.sr = librosa.load(audio_path)
                duration = librosa.get_duration(y=self.y, sr=self.sr)
                self.duration_label.config(text=f"Duration: {duration:.2f} seconds")
                self.refresh_visualization()
        elif audio_source == 'Microphone':
            self.y, self.sr = self.capture_microphone_audio()
            if self.y is not None:
                self.refresh_visualization()

    def capture_microphone_audio(self):
        print("🎤 Microphone capture is not implemented yet.")
        return None, None

    def refresh_visualization(self):
        if self.y is None:
            return

        fig, ax = plt.subplots(figsize=(10, 4))

        if self.view_var.get() == 'Spectrogram':
            mel_spec = librosa.feature.melspectrogram(y=self.y, sr=self.sr)
            data = librosa.power_to_db(mel_spec, ref=np.max) if self.scale_var.get() == 'Logarithmic' else mel_spec
            img = librosa.display.specshow(data, sr=self.sr, x_axis='time', y_axis='mel', ax=ax, cmap=self.cmap_var.get())
            fig.colorbar(img, ax=ax, format='%+2.0f dB')
            ax.set_title(f'Mel Spectrogram ({self.scale_var.get()})')

        elif self.view_var.get() == 'Waveform':
            librosa.display.waveshow(self.y, sr=self.sr, ax=ax)
            ax.set_title("Waveform")

        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def play_audio(self):
        if self.y is not None:
            sd.stop()  # Stop any ongoing playback
            sd.play(self.y, self.sr)

# Run the App
root = tk.Tk()
app = MusicVisualizerApp(root)
root.mainloop()
