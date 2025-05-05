# File: services/intent_handler.py
from services.ha_control import turn_on_device, turn_off_device

DEVICE_MAP = {
    "speaker": "media_player.office",
    "tv": "media_player.living_room_tv"
}

def handle_intent(intent, parameters):
    device = parameters.get("device", "speaker")
    entity_id = DEVICE_MAP.get(device)

    if not entity_id:
        return f"Unknown device: {device}"
        

    if intent == "turn_on_speaker":
        print(f"Handling intent: {intent} with entity_id: {entity_id}")
        success = turn_on_device(entity_id)
        return f"{device.capitalize()} turned on." if success else f"Failed to turn on {device}."

    elif intent == "turn_off_speaker":
        print(f"Handling intent: {intent} with entity_id: {entity_id}")
        success = turn_off_device(entity_id)
        return f"{device.capitalize()} turned off." if success else f"Failed to turn off {device}."

    return "Intent not recognized."
