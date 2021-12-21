import scipy
from scipy import signal
from scipy.io import wavfile
import os
from os.path import isfile
from pathlib import Path
import numpy as np

sampleRate = 44100

scipy.signal.butter(3, [500, 5000], btype='bandpass', fs=sampleRate)

dataPath = Path('./data')
folderPath = Path(dataPath, 'exhale')
filteredPath = Path(dataPath, 'filtered', 'exhale')
for wavFile in Path.iterdir(folderPath):
    if wavFile.name[0] == '.':
        continue
    print(wavFile.resolve())
    fs, data_wav = wavfile.read(wavFile.resolve())
    if data_wav.ndim == 1:
        leftDataWav = data_wav
    else:
        leftDataWav = data_wav[:, 0]
    b, a = scipy.signal.butter(3, [500, 5000], btype='bandpass', fs=sampleRate)
    
    filtered = scipy.signal.filtfilt(b, a, leftDataWav)

    filteredData = np.asarray(filtered, dtype=np.int16)
    filteredWavPath = Path(filteredPath, wavFile.stem + '-filtered.wav')
    wavfile.write(filteredWavPath.resolve(), fs, filteredData)