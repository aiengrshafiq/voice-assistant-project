# File: start.py
#from pvporcupine import create
import pvporcupine
import pyaudio
import struct
from main import run_voice_assistant
import os
from dotenv import load_dotenv

load_dotenv()

access_key = os.getenv("PORCUPINE_ACCESS_KEY")
device_index = int(os.getenv("MIC_DEVICE_INDEX", 2))


def listen_for_wake_word():
    
    #porcupine = create(access_key=access_key, keywords=["jarvis"])
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=[os.path.join(os.path.dirname(__file__), "models/porcupine/jarvis_raspberry-pi.ppn")]
    )
    pa = pyaudio.PyAudio()
    print(f"device_index: {device_index}")
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        input_device_index=2,
        frames_per_buffer=porcupine.frame_length,
    )

    print("Listening for wake word 'Jarvis'...")
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)

            if result >= 0:
                print("Wake word detected! Starting assistant...")
                run_voice_assistant()
                print("Listening for wake word 'Jarvis'...")

    except KeyboardInterrupt:
        print("Exiting wake word listener.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()


if __name__ == "__main__":
    # from services.automated_announcements import start_automated_announcements
    # start_automated_announcements()
    listen_for_wake_word()