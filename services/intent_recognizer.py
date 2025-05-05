# File: services/intent_recognizer.py
import os
#import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def detect_intent(user_input):
    prompt = f"""
You are a smart home assistant. Interpret the following command and extract the intent and any relevant parameters.

Command: "{user_input}"

Return a JSON with this format:
{{
  "intent": "intent_name",
  "parameters": {{ "key": "value" }}
}}

Valid intents: turn_on_light, turn_off_light, set_thermostat, turn_on_plug, turn_off_plug, set_reminder
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        result = response.choices[0].message.content
        #print("Intent recognition result:", result)
        import json
        parsed = json.loads(result)
        return parsed.get("intent"), parsed.get("parameters")
    except Exception as e:
        print("Intent recognition error:", str(e))
        return None, None