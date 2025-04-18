# virtual_assistant.py
import os
import re
import datetime
import pygame
import requests
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
import tinytuya
import dateparser
from apscheduler.schedulers.background import BackgroundScheduler
from openai import OpenAI
from rapidfuzz import fuzz

# Load environment variables
load_dotenv()

# Tuya configuration
DEVICE_ID = os.getenv("DEVICE_ID")
IP_ADDRESS = os.getenv("IP_ADDRESS")
LOCAL_KEY = os.getenv("LOCAL_KEY")
d = tinytuya.Device(DEVICE_ID, IP_ADDRESS, LOCAL_KEY, version=3.4)

# Voice configuration
KEY_PHRASE = os.getenv("KEY_PHRASE", "hey jarvis")

# OpenAI config
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-3.5-turbo")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI()

# Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "response.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove(filename)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception:
        return ""

def send_to_chatgpt(prompt):
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def control_home_assistant(entity_id, temperature):
    url = "http://localhost:8123/api/services/climate/set_temperature"  # Update to match your HA URL
    headers = {
        "Authorization": f"Bearer {os.getenv('HOME_ASSISTANT_TOKEN')}",
        "Content-Type": "application/json",
    }
    data = {
        "entity_id": entity_id,
        "temperature": temperature
    }
    try:
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        print("Failed to control Home Assistant device:", e)

def remind_me(task):
    speak(f"Reminder: {task}")

def handle_command(command):
    if "turn on" in command and "light" in command:
        d.turn_on()
        speak("Light turned on.")
    elif "turn off" in command and "light" in command:
        d.turn_off()
        speak("Light turned off.")
    elif match := re.search(r"remind me to (.+?) at (.+)", command):
        task, time_str = match.groups()
        run_time = dateparser.parse(time_str)
        if run_time:
            scheduler.add_job(remind_me, 'date', run_date=run_time, args=[task])
            speak(f"Reminder set for {task} at {run_time.strftime('%I:%M %p')}.")
        else:
            speak("Sorry, I couldn't understand the time.")
    elif match := re.search(r"set.*temperature.*(\d+)", command):
        temp = int(match.group(1))
        control_home_assistant("climate.nest_thermostat", temp)
        speak(f"Setting office temperature to {temp} degrees.")
    else:
        response = send_to_chatgpt(command)
        speak(response)

def main_loop():
    while True:
        print("Listening for wake word...")
        text = recognize_speech().lower()
        if fuzz.ratio(text, KEY_PHRASE.lower()) > 75:
            speak("Hello! How can I assist you?")
            while True:
                command = recognize_speech().lower()
                print("You said: ", command)
                if "stop" in command:
                    speak("Goodbye!")
                    return
                handle_command(command)

if __name__ == "__main__":
    main_loop()
