# File: services/text_to_speech.py
# import pyttsx3

# engine = pyttsx3.init()
# engine.setProperty('rate', 160)
# engine.setProperty('volume', 1.0)

# def speak(text):
#     print(f"Assistant: {text}")
#     engine.say(text)
#     engine.runAndWait()

import pyttsx3
import subprocess

engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"Assistant: {text}")
    # Save speech to a .wav file
    filename = "output.wav"
    engine.save_to_file(text, filename)
    engine.runAndWait()
    
    # Use aplay to play the wav file on the correct device
    subprocess.run(["aplay", "-D", "plughw:2,0", filename])