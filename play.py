import numpy as np
import pyaudio
import wave
import sys

RATE = 44100
DURATION = 2.0

def sound_array():
    frequency = 440
    t = np.linspace(0, DURATION, num = RATE * DURATION, endpoint = False)
    return np.cos(2 * np.pi * frequency * t)

# arr is np array of floats between -1 and 1
def to_bytes(arr):
    shifted = np.array(arr * (2**15 - 1), dtype=np.int16)
    return shifted.tobytes()

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                output=True)

stream.write(to_bytes(sound_array()))
stream.stop_stream()
stream.close()

p.terminate()
