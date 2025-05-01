# File: services/automated_announcements.py

import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from services.text_to_speech import speak

ANNOUNCEMENTS_FILE = "data/announcements.yaml"
scheduler = BackgroundScheduler()
scheduler.start()


def announce(message):
    speak(f"📢 Announcement: {message}")


def load_announcements():
    with open(ANNOUNCEMENTS_FILE, 'r') as file:
        data = yaml.safe_load(file)
    return data.get("announcements", [])


def schedule_announcements():
    announcements = load_announcements()

    for i, item in enumerate(announcements):
        msg = item.get("message")
        schedule_type = item.get("schedule")

        if schedule_type == "interval":
            scheduler.add_job(
                announce,
                "interval",
                minutes=item.get("minutes", 60),
                args=[msg],
                id=f"announcement_{i}"
            )
        elif schedule_type == "cron":
            scheduler.add_job(
                announce,
                "cron",
                day_of_week=item.get("day_of_week"),
                hour=item.get("hour"),
                minute=item.get("minute"),
                args=[msg],
                id=f"announcement_{i}"
            )


def start_automated_announcements():
    try:
        schedule_announcements()
        print("✅ Automated announcements scheduled.")
    except Exception as e:
        print(f"❌ Error scheduling announcements: {e}")
