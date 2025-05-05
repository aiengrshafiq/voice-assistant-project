# File: services/confirmation.py
from services.vosk_stt import listen_yes_no
from services.text_to_speech import speak

def confirm_action():
    speak("Please say yes to confirm or no to cancel.")
    for _ in range(3):
        response = listen_yes_no()
        print(f"Your confirmation word is {response}")
        if response:
            if any(word in response for word in ["yes", "confirm", "sure"]):
                return True
            elif any(word in response for word in ["no", "cancel", "stop"]):
                return False
        speak("Sorry, please say yes or no.")
    return False
