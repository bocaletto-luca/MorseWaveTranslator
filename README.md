# Morse Wave Translator

**Author:** Luca Bocaletto

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

# Morse Wave Translator

**Autore:** Bocaletto Luca

## Descrizione

Il software "Morse Wave Translator" è un'applicazione progettata per registrare segnali audio e successivamente decodificarli in codice Morse. L'applicazione sfrutta alcune librerie Python per svolgere questa operazione, comprese PyQt5 per la creazione dell'interfaccia grafica, sounddevice per la registrazione audio, soundfile per la lettura e la scrittura dei file audio, pygame per la riproduzione audio e numpy per la manipolazione dei dati audio.

![Screenshot 2023-10-18 114601](https://github.com/elektronoide/MorseWaveTranslator/assets/134635227/9997c047-fda4-407c-af72-fda902e01197)

### Componenti Principali

Il software è suddiviso in due classi principali:

1. **MorseDecoder:** Questa classe si occupa di decodificare i segnali audio registrati in codice Morse. Utilizza un dizionario che associa lettere e numeri ai rispettivi simboli del codice Morse. La decodifica si basa sulla lettura dell'ampiezza dei segnali audio: i picchi al di sopra di una soglia vengono considerati come "tratti" (dash), mentre i valori inferiori a tale soglia vengono considerati come "punti" (dot). La classe registra i segnali audio, li salva in un file audio e ne estrae il messaggio Morse decodificato.

2. **MorseDecoderApp:** Questa classe gestisce l'interfaccia grafica dell'applicazione. Consente all'utente di selezionare il dispositivo audio di input, specificare la durata della registrazione, registrare audio, decodificare il segnale Morse registrato, aprire file audio esistenti per la decodifica e riprodurre l'audio registrato. L'applicazione fornisce anche una guida per l'utente.

### Interfaccia Utente

L'applicazione dispone di un'interfaccia utente completa, con vari elementi, tra cui:

- Bottoni per l'acquisizione e la decodifica audio.
- Campi di input per la durata della registrazione.
- Una lista a discesa per la selezione del dispositivo di input.
- Un'area di testo per visualizzare i risultati della decodifica e le informazioni sulla registrazione.

## Utilità

In sintesi, "Morse Wave Translator" offre un modo semplice per registrare e decodificare segnali audio in codice Morse. L'utente può anche aprire file audio esistenti per la decodifica e riprodurre l'audio registrato. Questa applicazione è particolarmente utile per gli appassionati di Morse, gli operatori radioamatoriali o chiunque sia interessato a decifrare segnali Morse da registrazioni audio.
