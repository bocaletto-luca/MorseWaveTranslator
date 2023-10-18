# Software Name: Morse Wave Translator
# Author: Bocaletto Luca
# Descrizione: Questo software è un'applicazione che consente di registrare segnali audio e decodificarli in codice Morse.

# Import the sys module for accessing command line arguments.
import sys
# Import the PyQt5 module for creating a graphical interface.
import PyQt5.QtWidgets as QtWidgets
# Import the sounddevice module for audio recording.
import sounddevice as sd
# Import the numpy module for audio data handling.
import numpy as np
# Import the soundfile module for reading and writing audio files.
import soundfile as sf
# Import the os module for system operations.
import os
# Import the pygame module for audio playback.
import pygame
# Morse code dictionary mapping letters and numbers to Morse code representations.
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----'
}
# Class for Morse code decoding.
class MorseDecoder:
    def __init__(self):
		# Initialize the sample rate for audio.
        self.sample_rate = 44100
        # Initialize an empty list to store audio data.
        self.audio = []
        # Initialize the pygame mixer for audio playback.
        pygame.mixer.init()

    def decode(self, audio_data):
		# Initialize an empty string to store the decoded Morse code.
        decoded_text = ""
        # Implement Morse code decoding here.
        # Iterate through the audio data.
        for signal in audio_data:
            if signal > 0.5:  # Example: Check if the signal crosses a threshold.
                decoded_text += "-" # Append a dash for a "long" signal.
            else:
                decoded_text += "." # Append a dot for a "short" signal.
		# Initialize an empty string to store the complete decoded message.
        decoded_message = ""
        # Split the decoded text into individual Morse code signals.
        signal_list = decoded_text.split(" ")
        # Iterate through the list of Morse code signals.
        for signal in signal_list:
            if signal == "":
                decoded_message += " "  # Add a space to represent a word break.
            else:
				 # Find the corresponding character in the Morse code dictionary.
                char = next((char for char, code in MORSE_CODE_DICT.items() if code == signal), None)
                if char:
                    decoded_message += char # Append the decoded character to the message.
                else:
                    decoded_message += "?" # If the signal is not recognized, use "?" as a placeholder.
		# Return the complete decoded message.
        return decoded_message

    def record_audio(self, duration, input_device_index=None):
		# Record audio using the sounddevice library.
        # The audio is captured for the specified duration in seconds.
		# Calculate the number of samples to record based on the sample rate and duration.
        num_samples = int(self.sample_rate * duration)
		# Use sounddevice to record audio with the specified parameters.
        self.audio = sd.rec(int(self.sample_rate * duration), samplerate=self.sample_rate, channels=1, dtype='float32',
                            device=input_device_index)
        # Wait for the recording to complete.
        sd.wait()

    def save_audio(self, filename):
		# Save recorded audio to a file using the soundfile library.
        # The audio is saved with the specified filename and sample rate.
        # Use soundfile library to write the recorded audio data to a file.
        sf.write(filename, self.audio, self.sample_rate)

    def decode_audio_file(self, audio_file):
		# Read audio data from a file using the soundfile library.
        # Then, decode the audio data and return the decoded text.
        # Use soundfile library to read audio data from the specified file.
        audio_data, _ = sf.read(audio_file)
        # Decode the audio data using the MorseDecoder's decode method.
        decoded_text = self.decode(audio_data)
        # Return the decoded text.
        return decoded_text

    def play_audio(self, audio_data):
		# Play audio using the pygame mixer.
        # Use the pygame mixer to play the specified audio data.
        pygame.mixer.Sound(audio_data).play()

class MorseDecoderApp(QtWidgets.QWidget):
    def __init__(self):
		# Constructor for the MorseDecoderApp class.
        # Call the constructor of the parent class (QtWidgets.QWidget).
        super().__init__()
        # Initialize the list of input devices available.
        self.input_devices = self.get_input_devices()  # Inizializza la lista di periferiche di input
        # Initialize the user interface (UI) for the application.
        self.init_ui()
        # Create an instance of the MorseDecoder class for Morse code processing.
        self.morse_decoder = MorseDecoder()

    def init_ui(self):
		# Initialize the user interface (UI) elements of the application.
        # Set the title of the application window.
        self.setWindowTitle('Morse Wave Translator')
        # Set the initial position and size of the application window.
        self.setGeometry(100, 100, 600, 300)
		# Create a QPushButton widget with the label "Record."
        self.record_button = QtWidgets.QPushButton('Record')
        # Set an icon for the "Record" button, using the standard media play icon from the QApplication style.
        self.record_button.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        # Connect the "clicked" signal of the "Record" button to the "record_audio" method.
        self.record_button.clicked.connect(self.record_audio)
				
        self.decode_button = QtWidgets.QPushButton('Decode')
        self.decode_button.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekForward))
        self.decode_button.clicked.connect(self.decode_audio)

        self.open_file_button = QtWidgets.QPushButton('Apri File')
        self.open_file_button.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.open_file_button.clicked.connect(self.open_audio_file)

        self.duration_input = QtWidgets.QLineEdit(self)
        self.duration_input.setPlaceholderText("Durata della registrazione (secondi)")

        self.input_device_label = QtWidgets.QLabel("Dispositivo di Input:")
        self.input_device_combo = QtWidgets.QComboBox(self)
        self.input_device_combo.addItems(self.input_devices)  # Imposta la lista di periferiche di input

        self.duration_label = QtWidgets.QLabel("Durata della registrazione:")
        self.text_output_label = QtWidgets.QLabel("Risultati:")

        self.text_output = QtWidgets.QTextEdit()
        self.text_output.setReadOnly(True)

        self.help_button = QtWidgets.QPushButton('Guida')
        self.help_button.clicked.connect(self.show_help)

        self.play_button = QtWidgets.QPushButton('Play')
        self.play_button.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_recorded_audio)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.input_device_label)
        layout.addWidget(self.input_device_combo)
        layout.addWidget(self.duration_label)
        layout.addWidget(self.duration_input)
        layout.addWidget(self.record_button)
        layout.addWidget(self.decode_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.open_file_button)
        layout.addWidget(self.text_output_label)
        layout.addWidget(self.text_output)
        layout.addWidget(self.help_button)

        self.setLayout(layout)

    def record_audio(self):
        duration_str = self.duration_input.text()
        try:
            duration = float(duration_str)
        except ValueError:
            self.text_output.append("Errore: Inserisci una durata valida.")
            return

        if duration <= 0:
            self.text_output.append("Errore: La durata deve essere maggiore di zero.")
            return

        input_device_index = self.input_device_combo.currentIndex()
        try:
            self.morse_decoder.record_audio(duration, input_device_index)
        except sd.PortAudioError as e:
            self.text_output.append(f"Errore durante la registrazione: {str(e)}")
            return
        except Exception as e:
            self.text_output.append(f"Errore sconosciuto durante la registrazione: {str(e)}")
            return

        self.text_output.clear()
        self.text_output.append(f"Audio registrato per {duration} secondi")

    def decode_audio(self):
        if len(self.morse_decoder.audio) > 0:
            try:
                self.morse_decoder.save_audio('recorded_audio.wav')
                audio_data, _ = sf.read('recorded_audio.wav')
                decoded_text = self.morse_decoder.decode(audio_data)
                self.text_output.append(f"Decoded Morse Code: {decoded_text}")
            except sf.SoundFileError as e:
                self.text_output.append(f"Errore durante la decodifica del file audio: {str(e)}")
            except Exception as e:
                self.text_output.append(f"Errore sconosciuto durante la decodifica: {str(e)}")
        else:
            self.text_output.append("Nessun audio registrato.")

    def open_audio_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Apri File Audio", "", "File Audio (*.wav);;Tutti i Files (*)", options=options)
        if file_name:
            try:
                decoded_text = self.morse_decoder.decode_audio_file(file_name)
                self.text_output.append(f"Decoded Morse Code from File: {decoded_text}")
            except sf.SoundFileError as e:
                self.text_output.append(f"Errore durante l'apertura del file audio: {str(e)}")
            except Exception as e:
                self.text_output.append(f"Errore sconosciuto durante l'apertura del file audio: {str(e)}")

    def play_recorded_audio(self):
        if len(self.morse_decoder.audio) > 0:
            try:
                self.morse_decoder.save_audio('playback_audio.wav')
                audio_data, _ = sf.read('playback_audio.wav')
                self.morse_decoder.play_audio(audio_data)
            except sf.SoundFileError as e:
                self.text_output.append(f"Errore durante la riproduzione del file audio: {str(e)}")
            except Exception as e:
                self.text_output.append(f"Errore sconosciuto durante la riproduzione del file audio: {str(e)}")
        else:
            self.text_output.append("Nessun audio registrato per la riproduzione.")

    def show_help(self):
        QtWidgets.QMessageBox.information(self, "Guida",
        "Questa applicazione consente di registrare segnali audio e decodificarli in codice Morse. Ecco come utilizzarla:\n\n"
        "1. **Selezione del Dispositivo di Input:** Nel menu a discesa 'Dispositivo di Input', puoi selezionare il dispositivo audio di input che desideri utilizzare per la registrazione. Assicurati che il tuo dispositivo audio sia correttamente configurato.\n\n"
        "2. **Registrazione:** Nel campo 'Durata della registrazione (secondi)', inserisci la durata desiderata per la registrazione e premi il pulsante 'Record'. L'app registrerà l'audio dal dispositivo selezionato per il periodo specificato.\n\n"
        "3. **Decodifica:** Dopo la registrazione, premi il pulsante 'Decode' per decodificare il segnale Morse registrato. Il risultato della decodifica verrà mostrato nell'area 'Risultati'.\n\n"
        "4. **Apertura di File Audio:** Se hai un file audio con segnali Morse, puoi aprirlo premendo il pulsante 'Apri File'. L'app decodificherà il contenuto del file e lo mostrerà nell'area 'Risultati'.\n\n"
        "5. **Riproduzione Audio Registrato:** Dopo la registrazione, premendo il pulsante 'Play', puoi ascoltare nuovamente l'audio registrato.\n\n"
        "Assicurati di aver selezionato il dispositivo di input corretto e di impostare una durata di registrazione adeguata. Buon divertimento decodificando segnali Morse!\n\n"
        "Autore: Bocaletto Luca Aka Elektronoide\n\n"
        "Sito Web: https://www.elektronoide.it")
        
    def get_input_devices(self):
        input_devices = []
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if 'input' in device['name'].lower():
                input_devices.append(f"{i}: {device['name']}")
        return input_devices

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MorseDecoderApp()
    window.show()
    sys.exit(app.exec_())
