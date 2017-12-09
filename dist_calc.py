import numpy as np
import pyaudio
import wave
from play import sound_array, to_bytes, create_signal
import matplotlib.pyplot as plt

with wave.open('r_10.wav') as w:
    framerate = w.getframerate()
    frames = w.getnframes()
    channels = w.getnchannels()
    width = w.getsampwidth()

    data = w.readframes(frames)

raw_signal = np.frombuffer(data, dtype='<i2').reshape(-1, channels)[:,0]

r_sig = raw_signal/max(raw_signal)

expected_signal = create_signal()

#expected_signal = sound_array(6000)

corr = np.correlate(r_sig, expected_signal)
m = np.argmax(corr)

corr_cpy = corr.copy()
corr_cpy[m - round(len(expected_signal)/2):m+round(len(expected_signal)/2)] = 0.0
m2 = np.argmax(corr_cpy)

print(m, m2, len(expected_signal))
print(((m2 - m) / framerate) * 343 / 2.0)

plt.plot(corr[m - 1000:m + 2000])
plt.plot(corr_cpy[m - 1000:m + 2000])
plt.show()
#plt.plot(corr)
#plt.show()

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=framerate,
                output=True)

print('breakpoint')