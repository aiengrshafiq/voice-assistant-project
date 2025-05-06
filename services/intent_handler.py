# File: services/intent_handler.py
from services.ha_control import turn_on_device, turn_off_device, set_thermostat_temperature

DEVICE_MAP = {
    "speaker": "media_player.office",
    "tv": "media_player.living_room_tv"
}

THERMOSTAT_MAP = {
    "entertainment room": "climate.entertainment_room",
    "hall": "climate.hall",
    "left pathway": "climate.left_pathway",
    "meeting room": "climate.meeting_room",
    "pantry area": "climate.pantry_area"
}

def handle_intent(intent, parameters):
    if intent == "set_thermostat":
        room = parameters.get("room")
        temp = parameters.get("temperature")
        if not room or not temp:
            return "Please specify both room and temperature."

        entity_id = THERMOSTAT_MAP.get(room.lower())
        if not entity_id:
            return f"I couldn't find a thermostat in {room}."

        print(f"Setting {room} thermostat to {temp}°C")
        success = set_thermostat_temperature(entity_id, float(temp))
        return f"Set {room} thermostat to {temp}°C." if success else f"Failed to set thermostat in {room}."

    # Existing speaker logic
    device = parameters.get("device", "speaker")
    entity_id = DEVICE_MAP.get(device)

    if not entity_id:
        return f"Unknown device: {device}"
        
    if intent == "turn_on_speaker":
        success = turn_on_device(entity_id)
        return f"{device.capitalize()} turned on." if success else f"Failed to turn on {device}."

    elif intent == "turn_off_speaker":
        success = turn_off_device(entity_id)
        return f"{device.capitalize()} turned off." if success else f"Failed to turn off {device}."

    return "Intent not recognized."

