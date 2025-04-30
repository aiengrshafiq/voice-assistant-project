import pyttsx3
import subprocess

def synthesize_speech_to_wav(text, filename="test_output.wav"):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()
    print(f"Saved speech to {filename}")

def play_wav_aplay(filename, card=2, device=0):
    print(f"Playing {filename} using aplay on plughw:{card},{device}...")
    subprocess.run(["aplay", "-D", f"plughw:{card},{device}", filename])
    print("Done.")

if __name__ == "__main__":
    synthesize_speech_to_wav("This is a test of your Raspberry Pi voice assistant.")
    play_wav_aplay("test_output.wav", card=2, device=0)
