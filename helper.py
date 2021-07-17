import numpy as np

from scipy.signal import butter as butter
from scipy.signal import filtfilt as filtfilt
def upsample(X):
    ind = np.arange(1, len(X), 1)
    X = np.insert(X, ind, 0)
    return X

def LPF(X, fs):
    w = (fs / 2) / (fs)
    b, a = butter(5, w, 'low')
    X = filtfilt(b, a, X)
    return X

def complToReal(IQ, Fs):
    IQ = upsample(IQ)
    IQ = IQ * np.exp(1j * 2 * np.pi * Fs / 4)
    IQ = np.real(IQ)
    IQ = LPF(IQ, Fs)
    return IQ

