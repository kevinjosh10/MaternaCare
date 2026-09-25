# MaternaCare: Multilingual Voice-to-Voice Pipeline

This folder contains the core machine learning and API pipelines for the **MaternaCare Voice Assistant**. It handles dynamic multilingual speech recognition, translations, medical reasoning (Mock), and text-to-speech generation.

## Overview of Models

* **Model 1 (Language Translation):** Translates between 50+ native languages and English. Uses robust fallback logic (`translators` package wrapping Google & Bing) to prevent rate limits.
* **Model 2 (Voice Processing):** 
  * **STT (Speech-to-Text):** Upgraded from local Whisper AI to **Google Cloud Speech API** (`speech_recognition`) for instantaneous, highly accurate phonetic recognition of regional languages (Tamil, Hindi, Telugu, etc.) with zero local CPU load.
  * **TTS (Text-to-Speech):** Utilizes `gTTS` to generate native audio responses.
  * **VAD (Voice Activity Detection):** Uses smart RMS thresholding (`sounddevice` + `numpy`) to detect when the user stops speaking and trims silence automatically.
* **Model 4 (Medical Brain):** A dynamic mock engine that simulates an LLM. It parses the translated English query for medical keywords (stomach, fever, headache) and generates context-aware medical advice.

## Invisible Audio Pipeline
To provide a seamless conversational experience without cluttering the project or popping up media players:
- Audio is recorded to hidden system `Temp` folders.
- The MP3 response is played natively in the background using Windows `ctypes.windll.winmm` (MCI API).
- All temporary audio files are immediately deleted from disk after playback.

## Requirements
```bash
pip install numpy sounddevice wavio gTTS translators SpeechRecognition
```

## Usage
Run the main orchestrator script:
```bash
python models_1_and_2.py
```
1. Select your language from the 50-language menu.
2. Wait for the `MICROPHONE ACTIVE` prompt.
3. Speak your symptoms clearly. The system will auto-detect silence and pause recording.
4. The system will transcribe, translate, generate medical advice, translate it back to your language, and speak the response aloud.
