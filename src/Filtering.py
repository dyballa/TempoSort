import numpy as np
from scipy import signal

def moving_average_filter(x, cutoff_freq, sampling_rate):
    filter_length = int(np.ceil(sampling_rate / cutoff_freq))
    b = (np.ones(filter_length)) / filter_length
    return(signal.convolve(x, b, mode='same'))

def filter_every_channel(x, cutoff_freq, sampling_rate):
    return(np.apply_along_axis(moving_average_filter, axis=1, arr=x, cutoff_freq=cutoff_freq, sampling_rate=sampling_rate))

def capture_LFP(x, sampling_rate):
    return(filter_every_channel(x, 300, sampling_rate))