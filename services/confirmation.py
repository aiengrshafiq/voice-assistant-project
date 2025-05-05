# File: services/confirmation.py
from services.speech_to_text import listen_command
from services.text_to_speech import speak
import time

def confirm_action():
    speak("Please say yes to confirm or no to cancel.")
    for _ in range(3):
        time.sleep(1)  # Wait for TTS to finish
        response = listen_command()
        print(f"Your confirmation word is {response}")
        if response:
            if any(word in response for word in ["yes", "confirm", "sure"]):
                return True
            elif any(word in response for word in ["no", "cancel", "stop"]):
                return False
        speak("Sorry, please say yes or no.")
    return False
