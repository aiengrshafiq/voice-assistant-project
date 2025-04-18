from dotenv import load_dotenv
import os
from tuya_iot import TuyaOpenAPI

load_dotenv()

ACCESS_ID = os.getenv("TUYA_ACCESS_ID")
ACCESS_KEY = os.getenv("TUYA_ACCESS_KEY")
API_REGION = os.getenv("TUYA_API_REGION", "us")
USERNAME = os.getenv("TUYA_USERNAME")
PASSWORD = os.getenv("TUYA_PASSWORD")

# Initialize Tuya OpenAPI
REGION_URLS = {
    "us": "openapi.tuyaus.com",
    "eu": "openapi.tuyaeu.com",
    "cn": "openapi.tuyacn.com",
    "in": "openapi.tuyain.com"
}
openapi = TuyaOpenAPI(f"https://{REGION_URLS[API_REGION]}", ACCESS_ID, ACCESS_KEY)
openapi.connect(USERNAME, PASSWORD)

def turn_on(device_id):
    openapi.post(f'/v1.0/iot-03/devices/{device_id}/commands', {
        "commands": [{"code": "switch_led", "value": True}]
    })

def turn_off(device_id):
    openapi.post(f'/v1.0/iot-03/devices/{device_id}/commands', {
        "commands": [{"code": "switch_led", "value": False}]
    })
