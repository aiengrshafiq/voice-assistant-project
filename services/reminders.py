import uuid
import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from services.text_to_speech import speak
import dateparser
import os

REMINDERS_FILE = "reminders.json"
scheduler = BackgroundScheduler()
scheduler.start()

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f)

def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    with open(REMINDERS_FILE, "r") as f:
        return json.load(f)

def announce_reminder(message):
    speak(f"⏰ Reminder: {message}")

def schedule_reminder(message, remind_time):
    job_id = str(uuid.uuid4())
    scheduler.add_job(announce_reminder, 'date', run_date=remind_time, args=[message], id=job_id)

    # Save for persistence
    reminders = load_reminders()
    reminders.append({
        "id": job_id,
        "message": message,
        "time": remind_time.strftime("%Y-%m-%d %H:%M:%S"),
        "spoken": False
    })
    save_reminders(reminders)
    return job_id

def set_reminder_from_parameters(parameters):
    message = parameters.get("message", "")
    time_str = parameters.get("time", "")
    remind_time = dateparser.parse(time_str)

    if not remind_time:
        return "Sorry, I couldn't understand the time for the reminder."

    schedule_reminder(message, remind_time)
    return f"Reminder set for {remind_time.strftime('%I:%M %p')}: {message}"
