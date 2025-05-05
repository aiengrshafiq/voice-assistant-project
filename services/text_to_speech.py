# # File: services/text_to_speech.py
# import pyttsx3
# import subprocess
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Initialize TTS engine
# engine = pyttsx3.init()
# engine.setProperty('rate', 160)
# engine.setProperty('volume', 1.0)

# # Get output device from .env or default to system default
# AUDIO_OUTPUT_DEVICE = os.getenv("AUDIO_OUTPUT_DEVICE", "default")  # e.g., "plughw:1,0" or "bluealsa:HCI=hci0,DEV=XX:XX:XX:XX:XX:XX,PROFILE=a2dp"

# def speak(text):
#     print(f"Assistant: {text}")
#     filename = "output.wav"
    
#     # Generate the speech to file
#     engine.save_to_file(text, filename)
#     engine.runAndWait()
    
#     # Play using aplay with specified output device
#     try:
#         subprocess.run(["aplay", "-D", AUDIO_OUTPUT_DEVICE, filename], check=True)
        
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to play audio: {e}")

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
