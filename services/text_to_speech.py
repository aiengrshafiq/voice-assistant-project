# File: services/text_to_speech.py
import pyttsx3
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)


AUDIO_OUTPUT_DEVICE = os.getenv("AUDIO_OUTPUT_DEVICE")

# Optional: set output device if using SAPI5 on Windows or driver supports it
# engine.setProperty('outputDevice', AUDIO_OUTPUT_DEVICE)  # Only works on certain systems

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()
