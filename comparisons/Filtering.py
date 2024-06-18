import numpy as np
from scipy.signal import butter, filtfilt
def comp_LFP(raw_data, fs):
    nyquist = 0.5 * fs
    low = 300 / nyquist
    b, a = butter(3, low, btype='low')
    return filtfilt(b, a, raw_data)