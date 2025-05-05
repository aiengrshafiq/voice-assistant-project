import pyaudio

pa = pyaudio.PyAudio()

# List devices
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    print(i, info['name'], info['maxInputChannels'])

# Choose correct input and output device indexes
INPUT_INDEX = 2  # Replace with mic input index
OUTPUT_INDEX = 2  # Set to None to use default output (usually your speakers/headphones)

stream_input = pa.open(format=pyaudio.paInt16, channels=1, rate=16000,
                       input=True, input_device_index=INPUT_INDEX,
                       frames_per_buffer=1024)

stream_output = pa.open(format=pyaudio.paInt16, channels=1, rate=16000,
                        output=True, output_device_index=OUTPUT_INDEX,
                        frames_per_buffer=1024)

print("Listening and playing back... Press Ctrl+C to stop.")
try:
    while True:
        data = stream_input.read(1024)
        stream_output.write(data)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream_input.stop_stream()
    stream_input.close()
    stream_output.stop_stream()
    stream_output.close()
    pa.terminate()
