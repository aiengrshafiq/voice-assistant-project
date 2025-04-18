import os
import pygame
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI
import tuya_controller

# Load .env variables
load_dotenv()

KEY_PHRASE = os.getenv("KEY_PHRASE", "hello assistant")
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-3.5-turbo")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DeviceID = os.getenv("DeviceID")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

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
    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "API unavailable."

def send_to_chatgpt(prompt):
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def main_loop():
    devices = tuya_controller.openapi.get("/v1.0/iot-03/devices")
    print(devices)
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Say the keyword to activate assistant...")
    while True:
        text = recognize_speech_from_mic(recognizer, mic)
        print("You said:", text)
        if KEY_PHRASE.lower() in text.lower():
            speak("Hello! How can I help you?")
            while True:
                command = recognize_speech_from_mic(recognizer, mic)
                print("You said:", command.lower())
                if "stop" in command.lower():
                    speak("Goodbye!")
                    return

                if "turn on light" in command.lower():
                    tuya_controller.turn_on(DeviceID)
                    speak("Light turned on.")
                elif "turn off light" in command.lower():
                    tuya_controller.turn_off(DeviceID)
                    speak("Light turned off.")
                else:
                    response = send_to_chatgpt(command)
                    speak(response)
                

if __name__ == "__main__":
    main_loop()
