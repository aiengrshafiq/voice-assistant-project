# File: services/speech_to_text.py
import os
import speech_recognition as sr
from dotenv import load_dotenv
load_dotenv()

device_index = int(os.getenv("MIC_DEVICE_INDEX", 2))  # Default to 2

def listen_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=device_index)

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return None

    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
