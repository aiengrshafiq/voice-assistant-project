import os

import pygame
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
import tinytuya
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configuration for Tuya devicecls

DEVICE_ID = os.getenv("DEVICE_ID")
IP_ADDRESS = os.getenv("IP_ADDRESS")
LOCAL_KEY = os.getenv("LOCAL_KEY")

# Initialize the Tuya device
d = tinytuya.Device(DEVICE_ID, IP_ADDRESS, LOCAL_KEY, version=3.4)

# Configuration for voice activation
KEY_PHRASE = os.getenv("KEY_PHRASE")

# OpenAI API configuration
GPT_MODEL = os.getenv("GPT_MODEL")  # Define the GPT model to use
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "response.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait until playback is finished
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Unload music to release the file
    pygame.mixer.music.unload()

    # Now it's safe to delete the file
    os.remove(filename)

def recognize_speech_from_mic(recognizer, microphone):
    """Capture and recognize speech from the microphone."""
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.RequestError:
        return "API unavailable"
    except sr.UnknownValueError:
        return "Unable to recognize speech"
    
def send_to_chatgpt(prompt):
    """Send a prompt to ChatGPT and return the response."""
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def main_loop():
    """Main loop to listen for commands and interact with ChatGPT and Tuya device."""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(sample_rate=44100)

    while True:
        print("Listening for activation...")
        spoken_text = recognize_speech_from_mic(recognizer, microphone)
        if KEY_PHRASE.lower() in spoken_text.lower():
            print("Activated!")
            speak("Hello! How can I assist you?")
            
            while True:
                command = recognize_speech_from_mic(recognizer, microphone)
                speak(f"Shafiq you said {command.lower()}")
                if "stop" in command.lower():
                    speak("Goodbye!")
                    return

                if "turn on light" in command.lower():
                    speak("Shafiq I am turning the light ON.")
                    d.turn_on()
                    speak("Light turned on successfully.")
                    #continue
                elif "turn off light" in command.lower():
                    speak("Shafiq I am turning the light OFF.")
                    d.turn_off()
                    speak("Light turned off Successfully.")
                    #continue
                else:
                    response = send_to_chatgpt(command)
                    speak(response)

if __name__ == "__main__":
    main_loop()
