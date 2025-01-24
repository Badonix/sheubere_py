import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


BLOW_NUMBER = 80000


def detect_blow():
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            amplitude = np.linalg.norm(audio_data)

            # We check if current amplitude > Blow's amplitude
            if amplitude > BLOW_NUMBER:
                print("Blow detected! Amplitude:", amplitude)
    except KeyboardInterrupt:
        # Exit gracefully on Ctrl+C
        print("Exiting...")
    finally:
        # Close the audio stream
        stream.stop_stream()
        stream.close()
        p.terminate()


detect_blow()
