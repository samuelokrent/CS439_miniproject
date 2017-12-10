import numpy as np
import pyaudio
import wave
import sys
from time import sleep

RATE = 44100
DURATION = 0.0005

def sound_array(frequency):
    t = np.linspace(0, DURATION, num = RATE * DURATION, endpoint = False)
    return np.cos(2 * np.pi * frequency * t)

# arr is np array of floats between -1 and 1
def to_bytes(arr):
    shifted = np.array(arr * (2**15 - 1), dtype=np.int16)
    return shifted.tobytes()

def create_signal():
    s = []
    for i in range(5):
        s = np.append(sound_array(6000 + 1000*i), s)
    return s

def play():
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    output=True)

    s = create_signal()
    stream.write(to_bytes(s))
    #stream.write(to_bytes(sound_array(6000)))

    stream.stop_stream()
    stream.close()
    p.terminate()

def main():
  sleep(1)
  play()

if __name__ == '__main__':
    main()
