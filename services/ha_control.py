# File: services/ha_control.py
import requests,os
from dotenv import load_dotenv
load_dotenv()

HOME_ASSISTANT_URL = os.getenv('HOME_ASSISTANT_URL')
HOME_ASSISTANT_TOKEN = os.getenv('HOME_ASSISTANT_TOKEN')

HEADERS = {
    "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
    "Content-Type": "application/json"
}

def call_service(domain, service, entity_id):
    url = f"{HOME_ASSISTANT_URL}/api/services/{domain}/{service}"
    payload = {"entity_id": entity_id}
    response = requests.post(url, headers=HEADERS, json=payload)
    print(f"Calling: {url} with {payload}")
    print(f"Response: {response.status_code} - {response.text}")
    return response.status_code == 200

def extract_domain(entity_id):
    return entity_id.split(".")[0]

def turn_on_device(entity_id):
    domain = extract_domain(entity_id)
    print(f" domain extracted is: {domain}")
    return call_service(domain, "turn_on", entity_id)

def turn_off_device(entity_id):
    domain = extract_domain(entity_id)
    print(f" domain extracted is: {domain}")
    if domain == "media_player":
        return call_service(domain, "media_stop", entity_id)
    return call_service(domain, "turn_off", entity_id)
