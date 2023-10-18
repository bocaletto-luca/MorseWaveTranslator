# Software Name: Morse Wave Translator
# Author: Luca Bocaletto
# Description: This software is an application that allows you to record audio signals and decode them into Morse code.
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
                decoded_text += "-"  # Append a dash for a "long" signal.
            else:
                decoded_text += "."  # Append a dot for a "short" signal.
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
                    decoded_message += char  # Append the decoded character to the message.
                else:
                    decoded_message += "?"  # If the signal is not recognized, use "?" as a placeholder.
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
        super(MorseDecoderApp, self).__init__()
        # Initialize the list of input devices available.
        self.input_devices = self.get_input_devices()  # Initialize the list of input devices
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

        self.open_file_button = QtWidgets.QPushButton('Open File')
        self.open_file_button.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.open_file_button.clicked.connect(self.open_audio_file)

        self.duration_input = QtWidgets.QLineEdit(self)
        self.duration_input.setPlaceholderText("Recording Duration (seconds)")

        self.input_device_label = QtWidgets.QLabel("Input Device:")
        self.input_device_combo = QtWidgets.QComboBox(self)
        self.input_device_combo.addItems(self.input_devices)  # Set the list of input devices

        self.duration_label = QtWidgets.QLabel("Recording Duration:")
        self.text_output_label = QtWidgets.QLabel("Results:")

        self.text_output = QtWidgets.QTextEdit()
        self.text_output.setReadOnly(True)

        self.help_button = QtWidgets.QPushButton('Help')
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
            self.text_output.append("Error: Enter a valid duration.")
            return

        if duration <= 0:
            self.text_output.append("Error: Duration must be greater than zero.")
            return

        input_device_index = self.input_device_combo.currentIndex()
        try:
            self.morse_decoder.record_audio(duration, input_device_index)
        except sd.PortAudioError as e:
            self.text_output.append(f"Error during recording: {str(e)}")
            return
        except Exception as e:
            self.text_output.append(f"Unknown error during recording: {str(e)}")
            return

        self.text_output.clear()
        self.text_output.append(f"Audio recorded for {duration} seconds")

    def decode_audio(self):
        if len(self.morse_decoder.audio) > 0:
            try:
                self.morse_decoder.save_audio('recorded_audio.wav')
                audio_data, _ = sf.read('recorded_audio.wav')
                decoded_text = self.morse_decoder.decode(audio_data)
                self.text_output.append(f"Decoded Morse Code: {decoded_text}")
            except sf.SoundFileError as e:
                self.text_output.append(f"Error during decoding the audio file: {str(e)}")
            except Exception as e:
                self.text_output.append(f"Unknown error during decoding: {str(e)}")
        else:
            self.text_output.append("No audio recorded.")

    def open_audio_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav);;All Files (*)",
                                                            options=options)
        if file_name:
            try:
                decoded_text = self.morse_decoder.decode_audio_file(file_name)
                self.text_output.append(f"Decoded Morse Code from File: {decoded_text}")
            except sf.SoundFileError as e:
                self.text_output.append(f"Error while opening the audio file: {str(e)}")
            except Exception as e:
                self.text_output.append(f"Unknown error while opening the audio file: {str(e)}")

    def play_recorded_audio(self):
        if len(self.morse_decoder.audio) > 0:
            try:
                self.morse_decoder.save_audio('playback_audio.wav')
                audio_data, _ = sf.read('playback_audio.wav')
                self.morse_decoder.play_audio(audio_data)
            except sf.SoundFileError as e:
                self.text_output.append(f"Error during playback of the audio file: {str(e)}")
            except Exception as e:
                self.text_output.append(f"Unknown error during playback of the audio file: {str(e)}")
        else:
            self.text_output.append("No audio recorded for playback.")

    def show_help(self):
        QtWidgets.QMessageBox.information(self, "Help",
                                          "This application allows you to record audio signals and decode them into Morse code. Here's how to use it:\n\n"
                                          "1. **Select Input Device:** In the 'Input Device' dropdown menu, you can choose the audio input device you want to use for recording. Make sure your audio device is correctly configured.\n\n"
                                          "2. **Recording:** In the 'Recording Duration (seconds)' field, enter the desired recording duration and press the 'Record' button. The app will record audio from the selected device for the specified period.\n\n"
                                          "3. **Decoding:** After recording, press the 'Decode' button to decode the recorded Morse signal. The decoding result will be displayed in the 'Results' area.\n\n"
                                          "4. **Opening Audio Files:** If you have an audio file with Morse signals, you can open it by pressing the 'Open File' button. The app will decode the content of the file and display it in the 'Results' area.\n\n"
                                          "5. **Playback Recorded Audio:** After recording, by pressing the 'Play' button, you can listen to the recorded audio again.\n\n"
                                          "Make sure you select the correct input device and set an appropriate recording duration. Have fun decoding Morse signals!\n\n"
                                          "Author: Luca Bocaletto AKA Elektronoide\n\n"
                                          "Website: https://www.elektronoide.it")

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
