import numpy as np
import os
from play import create_signal
import pyaudio
import wave
import subprocess
import sys
import time
import matplotlib.pyplot as plt

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3

def shift(data):
    data_array = np.frombuffer(data, dtype='<i2')
    return np.array(data_array, dtype=np.float64) / ((2**15) - 1.0)

def record():
  p = pyaudio.PyAudio()

  stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

  data = np.array([])
  while len(data) < (RATE * RECORD_SECONDS):
    data = np.append(data, shift(stream.read(CHUNK)))
  stream.stop_stream()
  stream.close()
  p.terminate()
  return data[10000:]

def zoom(data):
  idx = np.argmax(data)
  buffer = int(RATE * 0.010)
  return data[idx - buffer: idx + buffer]

def corr(data):
  expected_signal = create_signal()
  corr = np.correlate(data, expected_signal)
  return corr
 
def main():
  subprocess.call("python play.py &", shell=True)
  data = record()
  plt.plot(data)
  plt.show()

  data = zoom(data)
  plt.plot(data)
  plt.show()

  c = corr(data)
  m = np.argmax(c)
  plt.plot(c)
  c_copy = c.copy()
  l = len(create_signal())
  c_copy[m - round(l/2):m+round(l/2)] = 0.0
  m2 = np.argmax(c_copy)
  plt.plot(c_copy)
  plt.show()
  
  print(m, m2)
  print(((m2 - m) / (RATE * 1.0)) * 343 / 2.0)

if __name__ == '__main__':
    main()
