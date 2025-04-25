# virtual_assistant.py
import os
import re
import pygame
import requests
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
import tinytuya
import dateparser
from apscheduler.schedulers.background import BackgroundScheduler
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

# Configuration
DEVICE_ID = os.getenv("DEVICE_ID")
IP_ADDRESS = os.getenv("IP_ADDRESS")
LOCAL_KEY = os.getenv("LOCAL_KEY")
HA_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN")
HA_URL = os.getenv("HOME_ASSISTANT_URL", "http://localhost:8123")

# GPT configuration
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-3.5-turbo")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

# Tuya Smart Plug
d = tinytuya.Device(DEVICE_ID, IP_ADDRESS, LOCAL_KEY, version=3.4)

# Scheduler for reminders
scheduler = BackgroundScheduler()
scheduler.start()

# Text-to-speech function
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

# Speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        result = recognizer.recognize_google(audio)
        print(f" You said: {result}")
        return result
    except Exception:
        return ""

# GPT general assistant response
def general_gpt_response(command):
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": command}],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

# GPT intent extraction
def get_gpt_intent(command):
    prompt = f"""
    You are a smart office assistant. Identify intent from this command clearly in JSON format:

    Command: "{command}"

    Expected JSON format:
    {{"intent": "intent_name", "parameters": {{"param1": "value", ...}}}}

    Known intents: turn_light_on, turn_light_off, set_reminder, set_temperature
    If intent is not one of the above, respond with intent 'unknown'.
    """

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    try:
        return json.loads(response.choices[0].message.content.strip())
    except:
        return {"intent": "unknown", "parameters": {}}

# Confirmation before action
def confirm_action(command):
    speak(f"You asked: '{command}'. Do you want me to proceed?")
    response = recognize_speech().lower()
    print(f" confirm action is {response}")
    return "yes" in response or "sure" in response or "go ahead" in response

# Actions
def turn_light(on=True):
    if on:
        d.turn_on()
        speak("I've turned the lights on.")
    else:
        d.turn_off()
        speak("I've turned the lights off.")

def set_reminder(task, time_str):
    reminder_time = dateparser.parse(time_str)
    if reminder_time:
        scheduler.add_job(lambda: speak(f"Reminder: {task}"), 'date', run_date=reminder_time)
        speak(f"Reminder set for {task} at {reminder_time.strftime('%I:%M %p')}.")
    else:
        speak("I couldn't understand the reminder time.")

def set_temperature(temp):
    headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}
    data = {"entity_id": "climate.nest_thermostat", "temperature": temp}
    requests.post(f"{HA_URL}/api/services/climate/set_temperature", headers=headers, json=data)
    speak(f"The office temperature is set to {temp} degrees.")

# Main handler
def handle_command(command):
    intent_data = get_gpt_intent(command)
    intent = intent_data["intent"]
    params = intent_data.get("parameters", {})

    if intent == "turn_light_on":
        turn_light(on=True)
    elif intent == "turn_light_off":
        turn_light(on=False)
    elif intent == "set_reminder":
        set_reminder(params.get("task", "something"), params.get("time", ""))
    elif intent == "set_temperature":
        set_temperature(params.get("temperature", 22))
    else:
        speak("I'm not configured for this request, but here's a general response:")
        response = general_gpt_response(command)
        speak(response)

# Assistant interaction loop
def assistant_loop():
    while True:
        speak("Anything else I can help you with?")
        response = recognize_speech().lower()
        if "no" in response or "exit" in response or "stop" in response:
            speak("Okay, going to sleep. Call me anytime.")
            break
        elif response:
            if confirm_action(response):
                handle_command(response)
            else:
                speak("Action cancelled.")

# Main loop
def main_loop():
    speak("Assistant ready. Please say 'Hey Jarvis' to wake me.")
    while True:
        wake_word = recognize_speech().lower()
        if "hey jarvis" in wake_word:
            speak("Yes, how can I assist?")
            assistant_loop()

if __name__ == "__main__":
    main_loop()
