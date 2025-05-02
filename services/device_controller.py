# File: services/device_controller.py
import requests

def execute_device_action(intent, parameters):
    # In production: connect with Home Assistant REST API or MQTT
    try:
        if intent == "turn_on_light":
            room = parameters.get("room", "default")
            return f"Turning on the light in {room}."

        elif intent == "turn_off_light":
            room = parameters.get("room", "default")
            return f"Turning off the light in {room}."

        elif intent == "set_thermostat":
            temp = parameters.get("temperature")
            return f"Setting thermostat to {temp} degrees."

        elif intent == "turn_on_plug":
            device = parameters.get("device", "plug")
            return f"Turning on {device}."

        elif intent == "turn_off_plug":
            device = parameters.get("device", "plug")
            return f"Turning off {device}."

        elif intent == "set_reminder":
            message = parameters.get("message", "")
            time = parameters.get("time", "soon")
            return f"Reminder set: '{message}' at {time}."
            # from services.reminders import set_reminder_from_parameters
            # return set_reminder_from_parameters(parameters)

        else:
            return "Intent not yet supported."
    except Exception as e:
        return f"Error executing action: {str(e)}"