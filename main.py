# File: main.py
import time
from services.speech_to_text import listen_command
from services.text_to_speech import speak
from services.intent_recognizer import detect_intent
from services.confirmation import confirm_action
from services.device_controller import execute_device_action


def run_voice_assistant():
    speak("Voice assistant initialized. How can I help you today?")
    while True:
        try:
            command = listen_command()
            if not command:
                continue

            speak(f"You said: {command}")
            intent, parameters = detect_intent(command)

            if intent == "unsupported":
                speak("I'm your smart home assistant. I can help with lights, plugs, thermostat, or reminders.")
            elif intent:
                speak(f"I understood you want to: {intent}. Shall I proceed?")
                if confirm_action():
                    result = execute_device_action(intent, parameters)
                    speak(result)
                else:
                    speak("Okay, cancelled.")
            else:
                speak("Sorry, I did not understand your request.")

        except KeyboardInterrupt:
            speak("Shutting down. Goodbye!")
            break


if __name__ == '__main__':
    run_voice_assistant()