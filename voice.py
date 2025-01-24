import pyaudio
import numpy as np
import pygame

# Constants
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Format for audio input
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate
BLOW_THRESHOLD = 3000  # Threshold for detecting blowing noise

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the microphone stream
stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Blow Detector")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

running = True
blowing_detected = False


def detect_blow(data):
    """Detect blowing by analyzing the frequency spectrum."""
    # Convert raw audio data to NumPy array
    audio_data = np.frombuffer(data, dtype=np.int16)

    # Compute the Fast Fourier Transform (FFT)
    fft_data = np.fft.fft(audio_data)
    magnitude = np.abs(fft_data)

    # Analyze low frequencies
    low_frequency_energy = np.sum(magnitude[:100])

    print(low_frequency_energy)
    # Check if energy exceeds the threshold
    return low_frequency_energy > BLOW_THRESHOLD


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read audio data from the microphone
    data = stream.read(CHUNK, exception_on_overflow=False)
    blowing_detected = detect_blow(data)

    # Update the screen
    screen.fill((0, 0, 0))
    status_text = "Blowing Detected!" if blowing_detected else "No Blowing Detected."
    text = font.render(status_text, True, (255, 255, 255))
    screen.blit(text, (50, 130))
    pygame.display.flip()

    clock.tick(30)

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()
pygame.quit()
