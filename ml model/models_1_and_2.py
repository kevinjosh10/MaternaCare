import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

import sys
import numpy as np
import sounddevice as sd
import wavio
import speech_recognition as sr
from gtts import gTTS
import translators as ts
import tempfile
import ctypes

LANGUAGES = {
    '1': {'name': 'English', 'code': 'en'}, '2': {'name': 'Hindi (हिंदी)', 'code': 'hi'},
    '3': {'name': 'Tamil (தமிழ்)', 'code': 'ta'}, '4': {'name': 'Telugu (తెలుగు)', 'code': 'te'},
    '5': {'name': 'Bengali (বাংলা)', 'code': 'bn'}, '6': {'name': 'Gujarati (ગુજરાતી)', 'code': 'gu'},
    '7': {'name': 'Marathi (मराठी)', 'code': 'mr'}, '8': {'name': 'Kannada (ಕನ್ನಡ)', 'code': 'kn'},
    '9': {'name': 'Malayalam (മലയാളം)', 'code': 'ml'}, '10': {'name': 'Punjabi (ਪੰਜਾਬੀ)', 'code': 'pa'},
    '11': {'name': 'Spanish (Español)', 'code': 'es'}, '12': {'name': 'French (Français)', 'code': 'fr'},
    '13': {'name': 'German (Deutsch)', 'code': 'de'}, '14': {'name': 'Italian (Italiano)', 'code': 'it'},
    '15': {'name': 'Portuguese (Português)', 'code': 'pt'}, '16': {'name': 'Russian (Русский)', 'code': 'ru'},
    '17': {'name': 'Arabic (العربية)', 'code': 'ar'}, '18': {'name': 'Chinese (中文)', 'code': 'zh'},
    '19': {'name': 'Japanese (日本語)', 'code': 'ja'}, '20': {'name': 'Korean (한국어)', 'code': 'ko'},
    '21': {'name': 'Turkish (Türkçe)', 'code': 'tr'}, '22': {'name': 'Dutch (Nederlands)', 'code': 'nl'},
    '23': {'name': 'Polish (Polski)', 'code': 'pl'}, '24': {'name': 'Indonesian (Bahasa)', 'code': 'id'},
    '25': {'name': 'Vietnamese (Tiếng Việt)', 'code': 'vi'}, '26': {'name': 'Thai (ไทย)', 'code': 'th'},
    '27': {'name': 'Swedish (Svenska)', 'code': 'sv'}, '28': {'name': 'Danish (Dansk)', 'code': 'da'},
    '29': {'name': 'Norwegian (Norsk)', 'code': 'no'}, '30': {'name': 'Finnish (Suomi)', 'code': 'fi'},
    '31': {'name': 'Greek (Ελληνικά)', 'code': 'el'}, '32': {'name': 'Romanian (Română)', 'code': 'ro'},
    '33': {'name': 'Hungarian (Magyar)', 'code': 'hu'}, '34': {'name': 'Czech (Čeština)', 'code': 'cs'},
    '35': {'name': 'Slovak (Slovenčina)', 'code': 'sk'}, '36': {'name': 'Ukrainian (Українська)', 'code': 'uk'},
    '37': {'name': 'Bulgarian (Български)', 'code': 'bg'}, '38': {'name': 'Serbian (Српски)', 'code': 'sr'},
    '39': {'name': 'Croatian (Hrvatski)', 'code': 'hr'}, '40': {'name': 'Catalan (Català)', 'code': 'ca'},
    '41': {'name': 'Swahili (Kiswahili)', 'code': 'sw'}, '42': {'name': 'Afrikaans (Afrikaans)', 'code': 'af'},
    '43': {'name': 'Latvian (Latviešu)', 'code': 'lv'}, '44': {'name': 'Estonian (Eesti)', 'code': 'et'},
    '45': {'name': 'Icelandic (Íslenska)', 'code': 'is'}, '46': {'name': 'Welsh (Cymraeg)', 'code': 'cy'},
    '47': {'name': 'Tagalog (Tagalog)', 'code': 'tl'}, '48': {'name': 'Malay (Bahasa Melayu)', 'code': 'ms'},
    '49': {'name': 'Urdu (اردو)', 'code': 'ur'}, '50': {'name': 'Nepali (नेपाली)', 'code': 'ne'}
}

# Provide medical context so Whisper spells medical terms correctly instead of guessing randomly
MEDICAL_PROMPTS = {
    'ta': 'மருத்துவரிடம் பேசுகிறேன். எனக்கு வயிறு வலிக்கிறது, காய்ச்சல், தலைவலி.',
    'hi': 'मुझे पेट में दर्द है, बुखार है, सिरदर्द है।',
    'en': 'I am experiencing stomach pain, fever, and headache.',
    'te': 'నాకు కడుపు నొప్పి, జ్వరం, తలనొప్పి ఉన్నాయి.',
}

def robust_translate(text, source_lang, target_lang):
    if source_lang == target_lang or not text.strip():
        return text
    try:
        return ts.translate_text(text, translator='google', from_language=source_lang, to_language=target_lang)
    except:
        try:
            return ts.translate_text(text, translator='bing', from_language=source_lang, to_language=target_lang)
        except:
            return "(Translation Error)"

def generate_dynamic_advice(english_query):
    query = english_query.lower()
    if 'stomach' in query or 'belly' in query or 'pain' in query or 'goosebumps' in query or 'wipe' in query:
        return "I hear you are having some pain or discomfort in your stomach. Please rest, drink warm water, and if the pain is severe, consult your doctor immediately."
    elif 'fever' in query or 'hot' in query or 'temperature' in query:
        return "If you have a fever, please stay hydrated and monitor your temperature. Contact your doctor if it goes too high."
    elif 'headache' in query or 'head' in query:
        return "For a headache, try resting in a quiet, dark room. Do not take strong medications without asking your doctor."
    else:
        return f"I understand you are experiencing '{english_query}'. Please rest well, take care of your health, and visit a clinic if it persists."

def record_audio_smart(filename="patient_input.wav", max_duration=30, fs=16000):
    chunk_duration = 0.1
    chunk_samples = int(fs * chunk_duration)
    silence_limit = 1.0
    min_speech_duration = 1.0 
    
    print("\n[Calibrating Microphone... checking background noise for 1s]")
    ambient = []
    try:
        with sd.InputStream(samplerate=fs, channels=1, dtype='float32') as stream:
            for _ in range(10):
                data, _ = stream.read(chunk_samples)
                ambient.append(np.sqrt(np.mean(data**2)))
                
            noise_floor = np.mean(ambient)
            threshold = max(0.02, noise_floor * 4.0)
            
            print("\n" + "="*50)
            print("🎤 MICROPHONE ACTIVE - SPEAK LOUDLY & CLEARLY NOW!")
            print(f"⏱️ Maximum {max_duration} seconds. Stops when you pause.")
            print("="*50 + "\n")
            
            frames = []
            has_started_speaking = False
            speaking_duration = 0.0
            silence_time = 0.0
            total_time = 0.0
            
            while total_time < max_duration:
                data, _ = stream.read(chunk_samples)
                frames.append(data.copy())
                total_time += chunk_duration
                
                rms = np.sqrt(np.mean(data**2))
                vol_bars = "#" * int(min(rms * 100, 20))
                
                if rms > threshold:
                    speaking_duration += chunk_duration
                    if not has_started_speaking:
                        has_started_speaking = True
                        print("\n🗣️ Voice detected! Listening...")
                    silence_time = 0.0
                    sys.stdout.write(f"\r[Speaking] {total_time:.1f}s | Vol: {vol_bars:<20}")
                    sys.stdout.flush()
                else:
                    if has_started_speaking:
                        silence_time += chunk_duration
                        sys.stdout.write(f"\r[Silence: {silence_time:.1f}s / {silence_limit}s]    ")
                        sys.stdout.flush()
                        if silence_time >= silence_limit and speaking_duration >= min_speech_duration:
                            print(f"\n\n✅ Finished speaking! Stopping recording ({total_time:.1f}s).")
                            break
            
            if not has_started_speaking:
                print(f"\n⚠️ Did not detect clear speech (Volume was too low).")
                
    except Exception as e:
        print(f"Recording error: {e}")
        return False

    raw_audio = np.concatenate(frames, axis=0).flatten()
    peak = np.max(np.abs(raw_audio))
    if peak > 0.05:
        normalized_audio = raw_audio / peak * 0.95
    else:
        normalized_audio = raw_audio
        
    audio_int16 = (np.clip(normalized_audio, -1.0, 1.0) * 32767).astype(np.int16)
    wavio.write(filename, audio_int16, fs, sampwidth=2)
    return True

def play_audio_hidden(mp3_path):
    # Plays MP3 purely in background without any media player popups
    alias = 'myaudio'
    ctypes.windll.winmm.mciSendStringW(f'open "{mp3_path}" type mpegvideo alias {alias}', None, 0, None)
    ctypes.windll.winmm.mciSendStringW(f'play {alias} wait', None, 0, None)
    ctypes.windll.winmm.mciSendStringW(f'close {alias}', None, 0, None)

def main():
    print("==================================================================")
    print("  MATERNACARE: 50-LANGUAGE VOICE PIPELINE (Google Cloud - ULTRA FAST & ACCURATE)")
    print("==================================================================")
    
    print("\n--- SELECT YOUR LANGUAGE ---")
    for key, lang in LANGUAGES.items():
        if int(key) <= 25:
            col2_key = str(int(key) + 25)
            col2_lang = LANGUAGES[col2_key]
            print(f"[{key:>2}] {lang['name']:<25} | [{col2_key:>2}] {col2_lang['name']}")
    
    choice = input("\nEnter the number of the language you will speak (e.g., 3 for Tamil): ").strip()
    if choice not in LANGUAGES:
        print("Invalid choice, defaulting to English [1]")
        choice = "1"
        
    selected = LANGUAGES[choice]
    lang_code = selected['code']
    print(f"\n>>> You selected: {selected['name']} <<<")
    
    print("\n⏳ Initializing Google Cloud Speech Engine...")
    recognizer = sr.Recognizer()
    print("✅ Engine Ready!")

    # Use temp file for microphone recording so it doesn't clutter folder
    temp_dir = tempfile.gettempdir()
    audio_file = os.path.join(temp_dir, "patient_input.wav")
    
    success = record_audio_smart(audio_file, max_duration=30)
    if not success:
        return

    print("\n--- MODEL 2: VOICE TO TEXT (STT) ---")
    print("🔍 Transcribing audio...")
    
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        # Google Web Speech API is instantly fast and highly accurate for all global languages
        raw_text = recognizer.recognize_google(audio_data, language=lang_code)
    except sr.UnknownValueError:
        raw_text = ""
    except sr.RequestError as e:
        print(f"\n❌ Google API Error: {e}")
        return
    print(f"📝 Transcribed Text: \"{raw_text}\"")

    if not raw_text:
        print("\n❌ Audio was completely unclear or empty. Please restart and speak louder.")
        return

    print("\n--- MODEL 1: TRANSLATING TO ENGLISH (For Medical Brain) ---")
    english_query = robust_translate(raw_text, lang_code, 'en')
    print(f"🇺🇸 English Query: \"{english_query}\"")

    print("\n--- MODEL 4: MEDICAL BRAIN REASONING ---")
    mock_advice_en = generate_dynamic_advice(english_query)
    print(f"🩺 Doctor Advice: \"{mock_advice_en}\"")

    print(f"\n--- MODEL 1: TRANSLATING BACK TO NATIVE ({selected['name']}) ---")
    native_response = robust_translate(mock_advice_en, 'en', lang_code)
    print(f"🗣️ Response in {selected['name']}: \"{native_response}\"")

    print(f"\n--- MODEL 2: TEXT TO VOICE (TTS) ---")
    mp3_file = os.path.join(temp_dir, "maternacare_response.mp3")
    try:
        tts = gTTS(text=native_response, lang=lang_code, slow=False)
        tts.save(mp3_file)
        print("🔊 Playing audio...")
        play_audio_hidden(mp3_file)
        print("✅ Finished successfully!")
    except Exception as e:
        print(f"TTS Error: {e}")
        try:
            tts = gTTS(text=native_response, lang='en', slow=False)
            tts.save(mp3_file)
            play_audio_hidden(mp3_file)
        except:
            pass

    # Clean up temp files silently
    if os.path.exists(audio_file):
        try:
            os.remove(audio_file)
        except:
            pass
    if os.path.exists(mp3_file):
        try:
            os.remove(mp3_file)
        except:
            pass

if __name__ == '__main__':
    main()
