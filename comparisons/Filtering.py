import numpy as np
from scipy.signal import butter, filtfilt
import spikeinterface as si
import spikeinterface.preprocessing as spre

def butter_lowpass(lowcut, fs, order=3):
    nyquist = 0.5 * fs
    low = 300 / nyquist
    b, a = butter(3, low, btype='low')
    return b,a

def butter_lowpass_filter(data, lowcut, fs, order=3):
    b,a  = butter_lowpass(lowcut, fs, order=3)
    y = filtfilt(b,a, data)
    return y

def butter_bandpass(lowcut, highcut, fs, order=3):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def spikeinterface_LFP(sp_recording):
    return(spre.gaussian_filter(recording=sp_recording, freq_min=None, freq_max=300))

def spikeinterface_bp(sp_recording):
    return (spre.bandpass_filter(sp_recording, freq_min=300, freq_max=6000, dtype=np.float32))
