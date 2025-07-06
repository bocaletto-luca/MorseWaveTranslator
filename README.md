# Morse Wave Translator

**Author:** Bocaletto Luca

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge&logo=gnu)](LICENSE) [![Language: Python](https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python)](https://www.python.org/) [![Linux-Compatible](https://img.shields.io/badge/Linux-Compatible-blue?style=for-the-badge&logo=linux)](https://www.kernel.org/) [![Status: Complete](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)](https://github.com/bocaletto-luca/Directory-Monitor)

## Description

The "Morse Wave Translator" software is an application designed to record audio signals and subsequently decode them into Morse code. The application leverages several Python libraries for this task, including PyQt5 for the creation of the graphical interface, sounddevice for audio recording, soundfile for reading and writing audio files, pygame for audio playback, and numpy for audio data manipulation.

![Screenshot 2023-10-18 120557](https://github.com/elektronoide/MorseWaveTranslator/assets/134635227/4657fda1-dba0-495e-9687-651f173317ff)

### Key Components

The software is divided into two main classes:

1. **MorseDecoder:** This class is responsible for decoding the recorded audio signals into Morse code. It uses a dictionary that maps letters and numbers to their respective Morse code symbols. Decoding is based on reading the amplitude of audio signals: peaks above a threshold are considered "dashes," while values below this threshold are considered "dots." The class records audio signals, saves them in an audio file, and extracts the decoded Morse message.

2. **MorseDecoderApp:** This class manages the application's graphical interface. It allows the user to select the audio input device, specify the recording duration, record audio, decode the recorded Morse signal, open existing audio files for decoding, and play back the recorded audio. The application also provides a user guide.

### User Interface

The application features a comprehensive user interface with various elements, including:

- Buttons for audio capture and decoding.
- Input fields for specifying the recording duration.
- A dropdown list for selecting the input device.
- A text area to display decoding results and recording information.

## Utility

In summary, "Morse Wave Translator" offers a simple way to record and decode audio signals into Morse code. Users can also open existing audio files for decoding and play back the recorded audio. This application is particularly useful for Morse code enthusiasts, amateur radio operators, or anyone interested in deciphering Morse signals from audio recordings.

---

**Maintainer Update**

All legacy projects from the old `@Elektronoide` GitHub account are now officially maintained by **@bocaletto-luca**. Please direct any issues, pull requests, and stars to **@bocaletto-luca** for all future updates.

---
