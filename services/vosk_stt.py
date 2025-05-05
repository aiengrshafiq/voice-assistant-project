# File: services/vosk_stt.py
import os
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

model_path = "models/vosk/vosk-model-small-en-us-0.15"
model = Model(model_path)
samplerate = 16000
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen_yes_no():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)
        print("Listening (Vosk)...")
        for _ in range(100):  # Max 5 seconds (100 x 50ms)
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                print("Vosk recognized:", text)
                if text in ["yes", "confirm", "sure","no", "cancel", "stop"]:
                    return text
        return None
